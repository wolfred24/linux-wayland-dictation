#!/usr/bin/env python3
"""Time whisper.cpp (pywhispercpp) on a WAV file.

Requires: pip install pywhispercpp  (or the copy vendored by vocalinux, see below)
          plus a ggml model, e.g. ggml-small.bin from
          https://huggingface.co/ggerganov/whisper.cpp

Note: the CPU build matters more than the model. A baseline ggml build with no
AVX2/AVX512 dispatch is roughly 6-17x slower than an optimised one.

Example:
    python bench_whispercpp.py sample.wav --model ggml-small.bin --threads 6 --language es

Using vocalinux's vendored copy (Debian):
    LD_LIBRARY_PATH=/usr/lib/vocalinux/vendor \\
    PYTHONPATH=/usr/lib/vocalinux/vendor \\
    python bench_whispercpp.py sample.wav --model ggml-small.bin --threads 6
"""
import argparse
import time

from pywhispercpp.model import Model


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("wav")
    p.add_argument("--model", required=True, help="path to a ggml-*.bin model")
    p.add_argument("--threads", type=int, default=6)
    p.add_argument("--language", default="es")
    p.add_argument("--runs", type=int, default=3)
    args = p.parse_args()

    kwargs = dict(
        n_threads=args.threads,
        language=args.language,
        print_progress=False,
    )
    # pywhispercpp >=1.5 takes the sampling strategy in the constructor;
    # older releases accept beam_size=1 per call instead.
    try:
        model = Model(args.model, params_sampling_strategy=0, **kwargs)
        transcribe_kwargs = {}
    except TypeError:
        model = Model(args.model, **kwargs)
        transcribe_kwargs = {"beam_size": 1}

    best, text = None, ""
    for i in range(args.runs):
        t0 = time.perf_counter()
        segments = model.transcribe(args.wav, **transcribe_kwargs)
        text = " ".join(s.text.strip() for s in segments)
        dt = time.perf_counter() - t0
        best = dt if best is None else min(best, dt)
        print(f"run {i + 1}: {dt:.2f}s")

    print(f"\nbest: {best:.2f}s")
    print(f"text: {text}")


if __name__ == "__main__":
    main()
