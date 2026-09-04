"""Puifin pose library — the approved toon puffin, parameterized.
Statics:  Blender --background --factory-startup --python puifin_poses.py -- --poses perch,wave --size 1024 --samples 192
Strips:   Blender --background --factory-startup --python puifin_poses.py -- --anim blink,wave,flap --size 320 --samples 96 --out panim
Outputs rua-<pose>.png / anim-<name>-NN.png so towebp.py and strips.py work unchanged.
"""
import bpy, math, sys, argparse
from mathutils import Matrix, Vector

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--poses", default="perch")
ap.add_argument("--anim", default="")
ap.add_argument("--size", type=int, default=640)
ap.add_argument("--samples", type=int, default=64)
ap.add_argument("--out", default="prenders")
A = ap.parse_args(argv)

def srgb(hexs):
    h = hexs.lstrip("#")
    c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    def lin(u): return u / 12.92 if u <= 0.04045 else ((u + 0.055) / 1.055) ** 2.4
    return (*[lin(u) for u in c], 1.0)

INK = srgb("#1A1208")

def toon_mat(name, col):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = col
    nt.links.new(em.outputs[0], out.inputs[0])
    return m

_outline = None
def outline_mat():
    global _outline
    if _outline: return _outline
    m = bpy.data.materials.new("outline")
    m.use_nodes = True
    nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs["Color"].default_value = INK
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(geo.outputs["Backfacing"], mix.inputs["Fac"])
    nt.links.new(em.outputs[0], mix.inputs[1])
    nt.links.new(tr.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs[0])
    _outline = m
    return m

def add_outline(obj, width=0.03):
    obj.data.materials.append(outline_mat())
    mod = obj.modifiers.new("outline", "SOLIDIFY")
    mod.thickness = width; mod.offset = 1.0
    mod.use_flip_normals = True
    mod.material_offset = len(obj.data.materials) - 1

def sphere(name, loc, scale, mat, rot=(0,0,0), seg=64, outline=True, ow=0.03):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg//2, location=loc)
    o = bpy.context.object; o.name = name
    o.scale = scale
    o.rotation_euler = [math.radians(r) for r in rot]
    o.data.materials.append(mat)
    bpy.ops.object.shade_smooth()
    if outline: add_outline(o, ow)
    return o

def wipe():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    global _outline
    _outline = None
    for coll in (bpy.data.meshes, bpy.data.materials):
        for x in list(coll):
            if x.users == 0: coll.remove(x)

def build(p):
    """p: dict of pose params."""
    m_black = toon_mat("black", srgb("#20242B"))
    m_white = toon_mat("white", srgb("#FDFDF8"))
    m_orange= toon_mat("orange", srgb("#F26B1F"))
    m_tip   = toon_mat("tip", srgb("#D9531A"))
    m_ink   = toon_mat("ink", INK)
    m_pure  = toon_mat("pure", (1,1,1,1))
    m_blush = toon_mat("blush", srgb("#F5A76B"))

    sphere("body", (0, 0.02, -0.26), (0.88, 0.84, 1.04), m_black)
    sphere("belly", (0, -0.30, -0.42), (0.66, 0.62, 0.76), m_white, outline=False)
    sphere("faceL", (-0.28, -0.46, 0.50), (0.37, 0.30, 0.42), m_white, outline=False, rot=(0, 0, 8))
    sphere("faceR", (0.31, -0.44, 0.52), (0.37, 0.30, 0.42), m_white, outline=False, rot=(0, 0, -10))
    sphere("blushL", (-0.46, -0.66, 0.30), (0.11, 0.05, 0.08), m_blush, outline=False)
    sphere("blushR", (0.49, -0.64, 0.32), (0.11, 0.05, 0.08), m_blush, outline=False)

    # beak
    bpy.ops.mesh.primitive_cone_add(vertices=48, radius1=0.30, radius2=0.014, depth=0.42, location=(0.02, -0.88, 0.20))
    bk = bpy.context.object; bk.name = "beak"
    bk.data.transform(Matrix.Scale(0.72, 4, (1.0,0.0,0.0)) @ Matrix.Scale(1.15, 4, (0.0,0.0,1.0)) @ Matrix.Rotation(math.radians(102), 4, "X"))
    bk.data.materials.append(m_orange)
    bpy.ops.object.shade_smooth(); add_outline(bk, 0.024)
    bpy.ops.mesh.primitive_cone_add(vertices=48, radius1=0.15, radius2=0.010, depth=0.18, location=(0.02, -1.04, 0.13))
    tp = bpy.context.object; tp.name = "beaktip"
    tp.data.transform(Matrix.Scale(0.70, 4, (1.0,0.0,0.0)) @ Matrix.Scale(1.1, 4, (0.0,0.0,1.0)) @ Matrix.Rotation(math.radians(104), 4, "X"))
    tp.data.materials.append(m_tip)
    bpy.ops.object.shade_smooth()

    # eyes
    sq = 1.0 - p.get("eye_squash", 0.0)
    edx = p.get("pupil_dx", 0.0); edz = p.get("pupil_dz", 0.0)
    if p.get("closed"):
        for sx, x in ((-1, -0.29), (1, 0.31)):
            bpy.ops.mesh.primitive_torus_add(location=(x, -0.70, 0.60), major_radius=0.10, minor_radius=0.018, major_segments=48, minor_segments=12)
            t = bpy.context.object; t.name = f"lid{sx}"
            t.rotation_euler = (math.radians(55), 0, 0)
            t.data.materials.append(m_ink)
            bpy.ops.object.shade_smooth()
    else:
        for sx, x, s in ((-1, -0.29, 1.03), (1, 0.31, 0.98)):
            sphere(f"sclera{sx}", (x, -0.72, 0.62), (0.155*s, 0.09, 0.185*s*sq), m_pure, outline=True, ow=0.018)
            sphere(f"pupil{sx}", (x - 0.02 + edx, -0.795, 0.61 + edz), (0.085*s, 0.05, 0.105*s*sq), m_ink, outline=False)
            if sq > 0.5:
                sphere(f"spark{sx}", (x + 0.025 + edx, -0.84, 0.655 + edz), (0.028, 0.02, 0.028*sq), m_pure, outline=False)

    # wings: params (loc, rot, scale) or default tucked
    wl = p.get("wingL", ((-0.78, 0.12, -0.36), (8, 14, 12), (0.24, 0.46, 0.64)))
    wr = p.get("wingR", ((0.80, 0.12, -0.36), (8, -14, -12), (0.24, 0.46, 0.64)))
    sphere("wingL", wl[0], wl[2], m_black, rot=wl[1])
    sphere("wingR", wr[0], wr[2], m_black, rot=wr[1])

    if p.get("feet", True):
        sphere("footL", (-0.32, -0.42, -1.28), (0.24, 0.34, 0.09), m_orange, rot=(0, 0, 12), outline=True, ow=0.02)
        sphere("footR", (0.34, -0.42, -1.28), (0.24, 0.34, 0.09), m_orange, rot=(0, 0, -14), outline=True, ow=0.02)

    if p.get("book"):
        for sx in (-1, 1):
            bpy.ops.mesh.primitive_cube_add(location=(sx*0.22, -0.90, -1.16))
            c = bpy.context.object; c.name = f"page{sx}"
            c.scale = (0.24, 0.17, 0.016)
            c.rotation_euler = (math.radians(8), math.radians(sx*-14), 0)
            c.data.materials.append(m_white); add_outline(c, 0.014)
        bpy.ops.mesh.primitive_cube_add(location=(0, -0.88, -1.20))
        c = bpy.context.object; c.name = "cover"
        c.scale = (0.50, 0.185, 0.014)
        c.rotation_euler = (math.radians(8), 0, 0)
        c.data.materials.append(m_orange); add_outline(c, 0.014)

    if p.get("ticks"):
        for (x, z, rz) in ((-0.95, 1.05, 30), (-0.15, 1.30, 0), (0.75, 1.10, -30)):
            bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.022, depth=0.18, location=(x, -0.2, z))
            t = bpy.context.object; t.name = f"tick{x}"
            t.rotation_euler = (0, math.radians(rz), 0)
            t.data.materials.append(m_ink)
            bpy.ops.object.shade_smooth()

    # gather + root tilt
    meshes = [o for o in bpy.data.objects if o.type == "MESH"]
    bpy.ops.object.empty_add(location=(0, 0, -0.26))
    root = bpy.context.object; root.name = "root"
    for o in meshes: o.parent = root
    rr = p.get("tilt", (0, 0, 0))
    root.rotation_euler = [math.radians(x) for x in rr]
    root.location.z += p.get("z_shift", 0.0)

POSES = {
    "perch": dict(),
    "wave":  dict(wingR=((0.98, -0.30, 0.46), (0, -30, -52), (0.19, 0.13, 0.52)), tilt=(0, 0, -6)),
    "cheer": dict(wingL=((-0.84, -0.10, 0.10), (0, 42, 40), (0.20, 0.13, 0.52)),
                  wingR=((0.86, -0.10, 0.10), (0, -42, -40), (0.20, 0.13, 0.52)),
                  tilt=(-8, 0, 0), ticks=True),
    "rest":  dict(closed=True, tilt=(6, 0, 5)),
    "think": dict(pupil_dx=-0.05, pupil_dz=0.05, tilt=(-4, 0, -5)),
    "read":  dict(pupil_dz=-0.075, tilt=(10, 0, 0), book=True),
    "point": dict(wingR=((0.94, -0.30, 0.02), (0, -78, -8), (0.18, 0.13, 0.52)), tilt=(0, 0, -7)),
    "fly":   dict(wingL=((-0.92, 0.02, 0.02), (0, 62, 18), (0.22, 0.14, 0.58)),
                  wingR=((0.94, 0.02, 0.02), (0, -62, -18), (0.22, 0.14, 0.58)),
                  feet=False, tilt=(-14, 0, 0)),
}

def anim_frames(name):
    import math as m
    if name == "blink":
        yield 0, dict()
        yield 1, dict(eye_squash=0.45)
        yield 2, dict(closed=True)
        yield 3, dict(eye_squash=0.45)
    elif name == "wave":
        angs = [0, 0.35, 0.75, 1.0, 0.85, 1.05, 0.82, 1.02, 0.88, 0.55, 0.25, 0]
        for i, t in enumerate(angs):
            yield i, dict(
                wingR=((0.80 + 0.18*t, 0.12 - 0.42*t, -0.36 + 0.82*t),
                       (8 - 8*t, -14 - 16*t, -12 - 40*t),
                       (0.24 - 0.05*t, 0.46 - 0.33*t, 0.64 - 0.12*t)),
                tilt=(0, 0, -6*t),
            )
    elif name == "flap":
        for i in range(8):
            ph = i / 8.0 * 2 * m.pi
            t = 0.5 + 0.5 * m.sin(ph)
            yield i, dict(
                wingL=((-0.92, 0.02, 0.02), (0, 40 + 44*t, 10 + 16*t), (0.22, 0.14, 0.58)),
                wingR=((0.94, 0.02, 0.02), (0, -40 - 44*t, -10 - 16*t), (0.22, 0.14, 0.58)),
                feet=False, tilt=(-14 + 3*m.sin(ph), 0, 0), z_shift=0.05*m.sin(ph),
            )
    else:
        raise ValueError(name)

def rig_and_render(outname):
    bpy.ops.object.camera_add(location=(0.45, -7.0, 0.55))
    cam = bpy.context.object
    cam.rotation_euler = (Vector((0.02, 0, -0.10)) - cam.location).to_track_quat("-Z", "Y").to_euler()
    cam.data.lens = 80
    bpy.context.scene.camera = cam
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.samples = A.samples
    sc.cycles.use_denoising = True
    try:
        prefs = bpy.context.preferences.addons["cycles"].preferences
        prefs.compute_device_type = "METAL"; prefs.get_devices()
        for d in prefs.devices: d.use = True
        sc.cycles.device = "GPU"
    except Exception:
        sc.cycles.device = "CPU"
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    sc.render.film_transparent = True
    sc.render.resolution_x = sc.render.resolution_y = A.size
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA"
    import os
    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), A.out)
    os.makedirs(outdir, exist_ok=True)
    sc.render.filepath = os.path.join(outdir, outname)
    bpy.ops.render.render(write_still=True)
    print(f"RENDERED {outname}")

if A.anim:
    for name in [x.strip() for x in A.anim.split(",") if x.strip()]:
        for i, params in anim_frames(name):
            wipe(); build(params)
            rig_and_render(f"anim-{name}-{i:02d}.png")
else:
    for pose in [x.strip() for x in A.poses.split(",") if x.strip()]:
        wipe(); build(POSES[pose])
        rig_and_render(f"rua-{pose}.png")
