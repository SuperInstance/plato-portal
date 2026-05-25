#!/usr/bin/env python3
"""Generate WAV files for CTF audio challenges."""
import sys
import os
import math
import struct
import wave

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'dial_lang'))
from dial_interpreter import (
    consonance_score, position_to_freq, synthesize_note,
    TRADITIONS, SAMPLE_RATE
)

CHALLENGE_DIR = os.path.join(os.path.dirname(__file__), 'ctf_challenges')
AUDIO_DIR = os.path.join(CHALLENGE_DIR, 'audio_samples')
os.makedirs(AUDIO_DIR, exist_ok=True)


def save_wav(path, samples, sample_rate=SAMPLE_RATE):
    if not samples:
        return
    peak = max(abs(s) for s in samples) if samples else 1.0
    if peak == 0:
        peak = 1.0
    scale = 0.9 * 32767.0 / peak
    with wave.open(path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        for s in samples:
            val = int(max(-32767, min(32767, s * scale)))
            wf.writeframes(struct.pack('<h', val))


def gen_hidden_message_wav():
    """Generate WAV for Challenge 1 — encodes 'TONALITY'."""
    # Positions chosen so their consonance scores decode to ASCII via: score*95+32
    positions = [
        (2.392, 2.941, 0.050),  # score≈0.5474 → T
        (0.179, 1.205, 1.557),  # score≈0.4947 → O
        (0.259, 2.346, 1.791),  # score≈0.4842 → N
        (1.090, 0.219, 0.447),  # score≈0.3474 → A
        (2.959, 0.906, 0.329),  # score≈0.4632 → L
        (1.750, 0.100, 0.787),  # score≈0.4316 → I
        (1.944, 1.096, 0.675),  # score≈0.5474 → T
        (1.134, 2.773, 2.825),  # score≈0.6000 → Y
    ]
    audio = []
    for v, h, s in positions:
        sc = consonance_score(v, h, s)
        ch = chr(round(sc * 95) + 32)
        print(f"  ({v:.3f}, {h:.3f}, {s:.3f}) score={sc:.4f} → '{ch}'")
        note = synthesize_note(v, h, s, 0.6, volume=0.7)
        audio.extend(note)
    save_wav(os.path.join(CHALLENGE_DIR, 'hidden_message.wav'), audio)
    print("Generated hidden_message.wav")


def gen_anti_music_samples():
    """Generate 10 WAV files for Challenge 4."""
    sample_positions = [
        (2.72, 2.05, 1.80),  # 1: western → music
        (0.10, 0.15, 0.05),  # 2: anti-music
        (2.30, 2.50, 2.10),  # 3: jazz → music
        (0.05, 0.10, 0.10),  # 4: anti-music
        (2.77, 3.63, 2.80),  # 5: carnatic → music
        (0.15, 0.25, 0.05),  # 6: anti-music
        (2.10, 2.80, 1.60),  # 7: blues → music
        (0.08, 0.12, 0.03),  # 8: anti-music
        (2.50, 3.10, 2.30),  # 9: arabic → music
        (0.20, 0.05, 0.10),  # 10: anti-music
    ]
    for i, (v, h, s) in enumerate(sample_positions, 1):
        audio = synthesize_note(v, h, s, 2.0, volume=0.6)
        path = os.path.join(AUDIO_DIR, f'sample_{i:02d}.wav')
        save_wav(path, audio)
        score = consonance_score(v, h, s)
        label = "music" if score >= 0.15 else "ANTI-MUSIC"
        print(f"  sample_{i:02d}.wav: score={score:.4f} ({label})")

    print("Generated 10 audio samples")


if __name__ == '__main__':
    print("Generating CTF WAV files...")
    gen_hidden_message_wav()
    gen_anti_music_samples()
    print("Done!")
