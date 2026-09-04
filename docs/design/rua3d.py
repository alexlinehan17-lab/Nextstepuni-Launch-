"""Rua the Robin — 3D vinyl-toy build, Blender 4.5 headless.

Usage:
  Blender --background --factory-startup --python rua3d.py -- --poses perch,wave --size 1024 --samples 96
Builds the bird fresh per pose from a parameter dict, renders transparent PNGs.
Front of bird faces -Y; camera sits on -Y looking at the bird.
"""
import bpy, math, sys, argparse
from mathutils import Vector

# ---------- args ----------
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--poses", default="perch")
ap.add_argument("--size", type=int, default=1024)
ap.add_argument("--samples", type=int, default=96)
ap.add_argument("--out", default="renders")
ap.add_argument("--anim", default="")
A = ap.parse_args(argv)

def srgb(hexs):
    h = hexs.lstrip("#")
    c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    def lin(u): return u / 12.92 if u <= 0.04045 else ((u + 0.055) / 1.055) ** 2.4
    return (*[lin(u) for u in c], 1.0)

COL_TAUPE  = srgb("#9A8672")   # back / cap / wings
COL_TAUPE2 = srgb("#8A7663")   # tail, slightly deeper
COL_CREAM  = srgb("#F3EAD9")   # belly
COL_APRICOT= srgb("#F27E35")   # bib — brand warmth
COL_BEAK   = srgb("#D98F2B")
COL_EYE    = srgb("#221A14")
COL_LEG    = srgb("#6B5544")

def mat(name, col, rough=0.65, sss=0.0, coat=0.0, sheen=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = col
    b.inputs["Roughness"].default_value = rough
    if sss:
        b.inputs["Subsurface Weight"].default_value = sss
        b.inputs["Subsurface Radius"].default_value = (0.06, 0.04, 0.03)
    if coat: b.inputs["Coat Weight"].default_value = coat
    if sheen: b.inputs["Sheen Weight"].default_value = sheen
    return m

def sphere(name, loc, scale, material, rot=(0,0,0), seg=96, parent=None):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg//2, location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    o.rotation_euler = [math.radians(r) for r in rot]
    o.data.materials.append(material)
    bpy.ops.object.shade_smooth()
    if parent: o.parent = parent
    return o

def cone(name, loc, r, depth, material, rot=(0,0,0), parent=None):
    bpy.ops.mesh.primitive_cone_add(vertices=48, radius1=r, radius2=0.004, depth=depth, location=loc)
    o = bpy.context.object
    o.name = name
    o.rotation_euler = [math.radians(x) for x in rot]
    o.data.materials.append(material)
    bpy.ops.object.shade_smooth()
    if parent: o.parent = parent
    return o

def empty(name, loc, parent=None):
    bpy.ops.object.empty_add(location=loc)
    o = bpy.context.object
    o.name = name
    if parent: o.parent = parent
    return o

# ---------- pose parameters ----------
# wingL/wingR: (rx, ry, rz) degrees on shoulder empties. Neutral wings hug the body.
# root_rot: whole-bird tilt (rx=pitch fwd+, ry=lean, rz=turn)
POSES = {
    "perch": dict(),
    "wave":  dict(wingL=(0, 112, -35), root_rot=(0, 6, -8), eye_dz=0.01),
    "cheer": dict(wingL=(0, 130, -18), wingR=(0, -130, 18), root_rot=(-12, 0, 0), eye_dz=0.02),
    "rest":  dict(closed=True, legs=False, z_shift=-0.26, root_rot=(9, 0, 4)),
    "think": dict(root_rot=(-7, 0, -6), eye_dx=-0.035, eye_dz=0.045),
    "read":  dict(root_rot=(16, 0, 0), eye_dz=-0.05, book=True),
    "point": dict(wingR=(-30, -60, -30), root_rot=(0, -4, -10)),
    "fly":   dict(wingR=(0, -70, 0), wingL=(0, 70, 0), root_rot=(-18, 0, 0), legs=False, tail_up=34),
}


# ---------- animation sequences ----------
def _lerp(a, b, t): return a + (b - a) * t

def anim_frames(name):
    """Yield (frame_index, pose_param_dict) for a named animation."""
    import math as m
    if name == "blink":
        # 4 frames: open, half, closed, half — the CSS cycle holds frame 0 ~4s
        yield 0, dict()
        yield 1, dict(eye_squash=0.45)
        yield 2, dict(closed=True)
        yield 3, dict(eye_squash=0.45)
    elif name == "wave":
        # 12 frames: raise, three wags, lower, settle; last frame = rest pose
        wag = [112, 96, 118, 94, 116, 100]
        seq = [0, 55, 95] + wag + [60, 24, 0]
        for i, ang in enumerate(seq):
            t = ang / 112.0
            yield i, dict(
                wingL=(0, ang, -35 * t),
                root_rot=(0, 6 * t, -8 * t),
                eye_dz=0.01 * t,
            )
    elif name == "flap":
        # 8-frame flight loop: wings sine, body drifts, tail answers
        for i in range(8):
            ph = i / 8.0 * 2 * m.pi
            w = 70 + 38 * m.sin(ph)
            yield i, dict(
                wingR=(0, -w, 0), wingL=(0, w, 0),
                root_rot=(-18 + 2.5 * m.sin(ph), 0, 0),
                legs=False,
                tail_up=34 - 8 * m.sin(ph),
                z_shift=0.05 * m.sin(ph),
            )
    else:
        raise ValueError(f"unknown animation {name}")

def build(pose, override=None):
    p = POSES[pose] if override is None else override
    # wipe scene
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.lights, bpy.data.cameras):
        for x in list(coll):
            if x.users == 0: coll.remove(x)

    m_taupe  = mat("taupe",  COL_TAUPE,  rough=0.62, sss=0.10, sheen=0.35)
    m_taupe2 = mat("taupe2", COL_TAUPE2, rough=0.62, sss=0.08, sheen=0.3)
    m_cream  = mat("cream",  COL_CREAM,  rough=0.60, sss=0.12, sheen=0.35)
    m_apri   = mat("apricot",COL_APRICOT,rough=0.58, sss=0.12, sheen=0.35)
    m_beak   = mat("beak",   COL_BEAK,   rough=0.32, sss=0.06)
    m_eye    = mat("eye",    COL_EYE,    rough=0.06, coat=1.0)
    m_leg    = mat("leg",    COL_LEG,    rough=0.5)

    root = empty("RuaRoot", (0, 0, 0))

    # two-ball bird: big head over plump body, molded color parts
    sphere("body",  (0, 0.05, -0.35), (0.95, 0.90, 0.82), m_taupe, parent=root)
    sphere("head",  (0, -0.02, 0.40), (0.85, 0.80, 0.78), m_taupe, parent=root)
    sphere("belly", (0, -0.30, -0.44), (0.72, 0.70, 0.64), m_cream, parent=root)
    sphere("bib",   (0, -0.36, 0.10), (0.78, 0.62, 0.98), m_apri,  parent=root)

    # eyes
    edx = p.get("eye_dx", 0.0); edz = p.get("eye_dz", 0.0)
    if p.get("closed"):
        for sx in (-1, 1):
            bpy.ops.mesh.primitive_torus_add(location=(sx*0.25, -0.875, 0.46), major_radius=0.075, minor_radius=0.016, major_segments=64, minor_segments=16)
            t = bpy.context.object; t.name = f"lid{sx}"
            t.rotation_euler = (math.radians(55), 0, 0)
            t.scale = (1, 1, 1)
            t.data.materials.append(m_eye)
            bpy.ops.object.shade_smooth()
            t.parent = root
    else:
        for sx in (-1, 1):
            sq = 1.0 - p.get("eye_squash", 0.0)
            sphere(f"eye{sx}", (sx*0.25 + edx, -0.90, 0.45 + edz), (0.14, 0.125, 0.14 * sq), m_eye, parent=root)

    # beak — flat-shaded diamond pyramid, baked orientation
    from mathutils import Matrix
    bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.16, radius2=0.0, depth=0.52, location=(0, -1.07, 0.27))
    b = bpy.context.object; b.name = "beak"
    b.data.transform(Matrix.Scale(0.68, 4, (0.0, 0.0, 1.0)) @ Matrix.Rotation(math.radians(99), 4, "X") @ Matrix.Rotation(math.radians(45), 4, "Z"))
    b.data.materials.append(m_beak)
    b.parent = root

    # wings on the body
    for sx, key in ((-1, "wingL"), (1, "wingR")):
        sh = empty(f"shoulder{key}", (sx*0.64, 0.10, -0.10), parent=root)
        w = sphere(f"{key}", (sx*0.12, 0.04, -0.30), (0.22, 0.13, 0.44), m_taupe, rot=(18, sx*22, sx*-6), seg=64, parent=sh)
        rx, ry, rz = p.get(key, (0, 0, 0))
        sh.rotation_euler = [math.radians(x) for x in (rx, ry, rz)]

    # tail — fanned up-left so it breaks the silhouette at 3/4
    tup = p.get("tail_up", 58)
    sphere("tail", (0.26, 0.64, 0.10), (0.20, 0.72, 0.085), m_taupe2, rot=(tup, -30, -20), seg=48, parent=root)

    # legs
    if p.get("legs", True):
        for sx in (-1, 1):
            bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.038, depth=0.30, location=(sx*0.24, -0.10, -1.14))
            l = bpy.context.object; l.name = f"leg{sx}"
            l.data.materials.append(m_leg)
            bpy.ops.object.shade_smooth(); l.parent = root
            sphere(f"foot{sx}", (sx*0.24, -0.24, -1.33), (0.115, 0.185, 0.055), m_leg, parent=root)

    # book prop
    if p.get("book"):
        for sx in (-1, 1):
            bpy.ops.mesh.primitive_cube_add(location=(sx*0.22, -0.76, -1.24))
            c = bpy.context.object; c.name = f"page{sx}"
            c.scale = (0.22, 0.16, 0.015)
            c.rotation_euler = (math.radians(8), math.radians(sx*-14), 0)
            c.data.materials.append(m_cream); c.parent = root
        bpy.ops.mesh.primitive_cube_add(location=(0, -0.74, -1.28))
        c = bpy.context.object; c.name = "cover"
        c.scale = (0.45, 0.17, 0.012)
        c.rotation_euler = (math.radians(8), 0, 0)
        c.data.materials.append(m_apri); c.parent = root

    root.location = (0, 0, p.get("z_shift", 0.0))
    rr = p.get("root_rot", (0, 0, 0))
    yaw = p.get("yaw", 30)  # default 3/4 turn so beak, tail and wing read in silhouette
    pitch_base = p.get("pitch_base", 5)  # slight forward lean: lively, and lifts the tail into view
    root.rotation_euler = [math.radians(rr[0] + pitch_base), math.radians(rr[1]), math.radians(rr[2] + yaw)]
    return root

def rig_camera_lights():
    bpy.ops.object.camera_add(location=(0.55, -7.2, 1.15))
    cam = bpy.context.object
    target = Vector((0.05, 0, -0.08))
    cam.rotation_euler = (target - cam.location).to_track_quat("-Z", "Y").to_euler()
    cam.data.lens = 85
    bpy.context.scene.camera = cam

    def area(name, loc, rot, power, size, col=(1,1,1)):
        bpy.ops.object.light_add(type="AREA", location=loc, rotation=[math.radians(r) for r in rot])
        L = bpy.context.object; L.name = name
        L.data.energy = power; L.data.size = size; L.data.color = col
        return L
    area("key",  (-2.6, -3.4, 3.2), (52, -18, -32), 360, 5.5, (1.0, 0.975, 0.94))
    area("fill", ( 3.0, -3.0, 0.6), (78, 22, 42),   130, 5.0, (0.94, 0.965, 1.0))
    area("rim",  ( 0.6,  3.4, 2.6), (-118, 0, 8),   240, 4.0, (1.0, 0.98, 0.95))
    w = bpy.context.scene.world or bpy.data.worlds.new("World")
    bpy.context.scene.world = w
    w.use_nodes = True
    bg = w.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.92, 0.90, 0.88, 1.0)
    bg.inputs[1].default_value = 0.28

def render(path):
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.samples = A.samples
    sc.cycles.use_denoising = True
    try:
        prefs = bpy.context.preferences.addons["cycles"].preferences
        prefs.compute_device_type = "METAL"
        prefs.get_devices()
        for d in prefs.devices: d.use = True
        sc.cycles.device = "GPU"
    except Exception:
        sc.cycles.device = "CPU"
    sc.render.film_transparent = True
    sc.render.resolution_x = A.size
    sc.render.resolution_y = A.size
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA"
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)

import os
outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), A.out)
os.makedirs(outdir, exist_ok=True)
if A.anim:
    for name in [x.strip() for x in A.anim.split(",") if x.strip()]:
        for i, params in anim_frames(name):
            build("perch", override=params)
            rig_camera_lights()
            render(os.path.join(outdir, f"anim-{name}-{i:02d}.png"))
            print(f"RENDERED {name} frame {i}")
else:
    for pose in [x.strip() for x in A.poses.split(",") if x.strip()]:
        build(pose)
        rig_camera_lights()
        render(os.path.join(outdir, f"rua-{pose}.png"))
        print(f"RENDERED {pose}")

# Regenerating the app assets:
#   Blender --background --factory-startup --python rua3d.py -- \
#     --poses perch,wave,cheer,rest,think,read,point,fly --size 1024 --samples 192
#   Blender --background --factory-startup --python rua3d.py -- \
#     --anim blink,wave,flap --size 320 --samples 96 --out anim
# Stills convert to public/assets/rua/<pose>.webp at 768px; anim frames
# composite into horizontal strips (anim-<name>.webp) played by stepped
# CSS in components/ui/Rua.tsx. Convert with a Standard view transform —
# save_render applies the scene view transform, and the renders already
# carry the AgX look, so anything else double-tones them. No shadow
# catchers: they smear grey washes into transparent UI renders.
