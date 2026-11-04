"""Make two quiet, original stereo cues for the 900 ms Light bloom transition."""
from pathlib import Path
import math
import random
import struct
import wave

ROOT = Path(__file__).resolve().parents[1] / 'public' / 'sounds'
SAMPLE_RATE = 44100
DURATION = 0.9


def smoothstep(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3.0 - 2.0 * x)


def render(pausing):
    rng = random.Random(672 if pausing else 673)
    count = round(SAMPLE_RATE * DURATION)
    channels = [[], []]
    filters = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
    notes = [(523.251, .13, .078), (783.991, .22, .046), (1046.502, .32, .021)] if pausing else [(392.0, .015, .062), (261.626, .075, .065), (523.251, .12, .019)]
    for i in range(count):
        t = i / SAMPLE_RATE
        x = t / DURATION
        # A rounded envelope and low-pass filters remove hiss and hard edges.
        air_envelope = math.sin(math.pi * x) ** (1.6 if pausing else 2.1)
        cutoff = 800 + 1700 * math.sin(math.pi * x) if pausing else 2100 - 1400 * x
        lp_alpha = 1.0 - math.exp(-2.0 * math.pi * cutoff / SAMPLE_RATE)
        low_alpha = 1.0 - math.exp(-2.0 * math.pi * 280 / SAMPLE_RATE)
        for ch in range(2):
            noise = rng.uniform(-1.0, 1.0)
            states = filters[ch]
            states[0] += lp_alpha * (noise - states[0])
            states[1] += lp_alpha * (states[0] - states[1])
            states[2] += low_alpha * (states[1] - states[2])
            value = (states[1] - states[2]) * air_envelope * (.25 if pausing else .19)
            for freq, onset, level in notes:
                age = t - onset
                if age < 0:
                    continue
                attack = smoothstep(age / .085)
                tail = math.exp(-age * (4.1 if pausing else 5.0))
                end_fade = smoothstep((DURATION - t) / .19)
                detune = 1.0006 if ch == 0 else .9994
                phase = 2 * math.pi * freq * detune * age
                note = math.sin(phase) * .92 + math.sin(phase * 2) * .08
                value += note * attack * tail * end_fade * level
            channels[ch].append(value)
    peak = max(abs(v) for channel in channels for v in channel)
    # Match perceived cue levels while keeping ample peak headroom.
    raw_rms = math.sqrt(sum(v*v for channel in channels for v in channel) / (count*2))
    scale = min(.3 / peak, (10 ** (-26.5 / 20)) / raw_rms)
    frames = bytearray()
    for left, right in zip(*channels):
        frames.extend(struct.pack('<hh', round(left * scale * 32767), round(right * scale * 32767)))
    name = 'study-bloom-pause.wav' if pausing else 'study-bloom-return.wav'
    with wave.open(str(ROOT / name), 'wb') as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(frames)
    rms = math.sqrt(sum(v*v for channel in channels for v in channel) / (count*2)) * scale
    print(f'{name}: {DURATION:.2f}s, peak {peak*scale:.3f}, RMS {20*math.log10(rms):.1f} dBFS')


ROOT.mkdir(exist_ok=True, parents=True)
render(True)
render(False)
