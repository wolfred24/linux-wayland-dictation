#!/usr/bin/env python3
"""Time faster-whisper (CTranslate2) on a WAV file.

Requires: pip install faster-whisper

Example:
    python bench_faster_whisper.py sample.wav --model small --threads 6 --language es
"""
import argparse
import time
import wave

import numpy as np
from faster_whisper import WhisperModel


def load_wav(path: str) -> tuple[np.ndarray, int]:
    with wave.open(path) as w:
        sr, ch = w.getframerate(), w.getnchannels()
        raw = w.readframes(w.getnframes())
    audio = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    if ch > 1:
        audio = audio.reshape(-1, ch).mean(axis=1)
    return audio, sr


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("wav")
    p.add_argument("--model", default="small")
    p.add_argument("--threads", type=int, default=6)
    p.add_argument("--language", default="es")
    p.add_argument("--runs", type=int, default=3)
    p.add_argument("--beam-size", type=int, default=1)
    args = p.parse_args()

    audio, sr = load_wav(args.wav)
    duration = len(audio) / sr

    model = WhisperModel(
        args.model,
        device="cpu",
        compute_type="int8",
        cpu_threads=args.threads,
    )

    best, text = None, ""
    for i in range(args.runs):
        t0 = time.perf_counter()
        segments, _info = model.transcribe(
            audio,
            language=args.language,
            beam_size=args.beam_size,
            vad_filter=False,
        )
        text = " ".join(s.text.strip() for s in segments)
        dt = time.perf_counter() - t0
        best = dt if best is None else min(best, dt)
        print(f"run {i + 1}: {dt:.2f}s")

    print(f"\nbest: {best:.2f}s for {duration:.1f}s audio "
          f"({duration / best:.1f}x realtime)")
    print(f"text: {text}")


if __name__ == "__main__":
    main()
