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
    """Generate WAV for Challenge 1."""
    positions = [
        (2.72, 2.05, 1.80), (2.30, 2.50, 2.10), (2.77, 3.63, 2.80),
        (2.77, 3.63, 2.80), (2.50, 3.10, 2.30), (1.40, 1.20, 2.90),
        (2.10, 2.80, 1.60), (2.72, 2.05, 1.80), (2.90, 0.80, 3.00),
        (2.50, 3.10, 2.30), (2.77, 3.63, 2.80), (1.80, 1.50, 2.20),
        (2.30, 2.50, 2.10), (2.90, 0.80, 3.00), (2.50, 3.10, 2.30),
    ]
    audio = []
    for v, h, s in positions:
        note = synthesize_note(v, h, s, 0.5, volume=0.7)
        audio.extend(note)
    save_wav(os.path.join(CHALLENGE_DIR, 'hidden_message.wav'), audio)
    print("Generated hidden_message.wav")


def gen_anti_music_samples():
    """Generate 10 WAV files for Challenge 4."""
    # Music samples are near tradition landmarks; anti-music is maximally distant
    # Use positions that are clearly far from ALL traditions
    sample_positions = [
        (2.72, 2.05, 1.80),  # 1: western → music (score=1.0)
        (0.10, 0.15, 0.05),  # 2: anti-music (score~0.12)
        (2.30, 2.50, 2.10),  # 3: jazz → music (score=1.0)
        (0.05, 0.10, 0.10),  # 4: anti-music (score~0.13)
        (2.77, 3.63, 2.80),  # 5: carnatic → music (score=1.0)
        (0.15, 0.25, 0.05),  # 6: anti-music (score~0.14)
        (2.10, 2.80, 1.60),  # 7: blues → music (score=1.0)
        (0.08, 0.12, 0.03),  # 8: anti-music (score~0.12)
        (2.50, 3.10, 2.30),  # 9: arabic → music (score=1.0)
        (0.20, 0.05, 0.10),  # 10: anti-music (score~0.14)
    ]
    for i, (v, h, s) in enumerate(sample_positions, 1):
        # Generate 2 seconds of audio
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
