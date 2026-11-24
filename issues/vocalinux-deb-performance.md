# Issue draft — VocaHQ/vocalinux

**Title:** Thin `.deb` ships a baseline ggml build: whisper.cpp runs at 0.6× realtime (no AVX2 variant, no Vulkan backend)

## Summary

On Debian 13 (x86_64) the `.deb` transcribes at about **0.6× realtime** on CPU,
which makes live dictation unusable. The same `small` model under `faster-whisper`
(CTranslate2 int8) runs at **11× realtime** on the same machine, and the same
whisper.cpp model under Hex (Vulkan) is several times faster. The gap looks like
packaging, not the engine.

## Environment

- Debian GNU/Linux 13 (trixie), GNOME 48.7 on Wayland
- AMD Ryzen 5 5600G (6C/12T), AMD Radeon RX 6950 XT (RADV NAVI21)
- Mesa 25.0.7, `libvulkan1` 1.4.309, `mesa-vulkan-drivers` 25.0.7
- vocalinux `0.18.6-1` from the release `.deb` (amd64)

## Steps

1. `sudo apt install ./vocalinux_0.18.6-1_amd64.deb`
2. Use `whisper_cpp` with a `small` ggml model (the same model under another tool
   was used as a reference).
3. Transcribe a 17.6 s Spanish WAV.

## Expected

Roughly real-time or faster on a 6-core Zen 3.

## Actual

```
whisper_backend_init_gpu: no GPU found

# 6 threads
run 1: 27.46s
run 2: 27.41s
run 3: 27.40s      # 0.6x realtime for 17.6 s audio

# 12 threads
run 3: 31.76s      # slower: memory-bound
```

## Evidence of the packaging cause

```
$ ls /usr/lib/vocalinux/vendor/ | grep ggml
libggml-base.so
libggml-cpu.so          # only the generic build
libggml.so
$ ls /usr/lib/vocalinux/vendor/ | grep -i vulkan
(nothing)
```

`ggml` dispatches to separate `libggml-cpu-*.so` variants (haswell/AVX2/AVX512)
when they are present. In this `.deb` only the baseline `libggml-cpu.so` ships, so
the runtime falls back to the slow path. There is also no Vulkan backend, even
though `libvulkan1` and a working RADV driver are present.

Your `docs/INSTALL.md` says the `.deb`/`.rpm` are "thin packages" and that the
AppImage rebuilds whisper.cpp with Vulkan — that matches what we see, but the
resulting `.deb` performance is a surprise for users who install it.

## Suggested fixes (any of)

1. Ship the `libggml-cpu-*` variant modules alongside `libggml-cpu.so`, so the
   dispatcher can pick AVX2/FMA.
2. Document the performance expectation of the `.deb` in `INSTALL.md`
   (e.g. "CPU-only, baseline build; use the AppImage/Flatpak for Vulkan"), and
   point to the Flatpak for GPU users.
3. Optionally add a Vulkan build to the `.deb` (or an opt-in package), since the
   runtime dependency `libvulkan1` is already fine on Debian 13.

## Willing to test

Happy to re-run the same sample on the fixed package and report timings on
Debian 13 + GNOME Wayland (Ryzen 5 5600G / RX 6950 XT).
