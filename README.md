# Local dictation on Debian 13 + GNOME 48 (Wayland): three tools, measured

Measured on **2026-11-24**, on one machine, with one Spanish audio sample.
This is a small, reproducible dataset — not a benchmark suite. Read the
[Limitations](#limitations) before quoting any number.

**TL;DR:** on GNOME Wayland, three tools can type into any window without
extra privileges. On this hardware, `voiceio` (29 stars) decoded the sample
**7× faster** than `hex` with a 3× larger model and **17× faster** than the
`vocalinux` `.deb`, because of *runtime packaging*, not model quality.

## Environment

| | |
|---|---|
| OS | Debian GNU/Linux 13 (trixie) |
| Desktop | GNOME Shell 48.7, **Wayland** |
| CPU | AMD Ryzen 5 5600G (6C/12T) |
| GPU | AMD Radeon RX 6950 XT (RADV NAVI21), Mesa 25.0.7, libvulkan 1.4.309 |
| RAM | 15 GiB |
| Mic | Behringer UMC202HD 192k (USB) |
| Sample | 17.6 s of Spanish speech, 16 kHz mono WAV, same file for every run |

## Results (same audio, greedy decoding)

| Tool | Version | Model | Runtime | Time | Realtime | Text |
|---|---|---|---|---|---|---|
| **voiceio** | 1.18.14 (`.deb`) | faster-whisper `small` int8 (244M) | CTranslate2, CPU, 6 threads | **1.55 s** | **11.3×** | reference |
| **hex** | 3.4.0 (`.deb`) | whisper.cpp `large-v3-turbo` Q8_0 (809M) | whisper.cpp + **Vulkan** | 4.00 s | 4.4× | 1 word different |
| **vocalinux** | 0.18.6 (`.deb`) | whisper.cpp `small` | whisper.cpp, **baseline ggml**, CPU, 6 threads | 27.40 s | **0.6×** | reference |

`vocalinux` with 12 threads: 31.8 s (memory-bound, slower).

Reference transcript (voiceio and vocalinux, identical output):

> Ok, a ver, vamos a probar la dictación. En este momento, justamente le estoy
> dictando al micrófono de la computadora y vamos a ver si escribe lo que le
> estoy dictando.

`hex` produced the same text except *"la estoy dictando"* instead of *"le estoy
dictando"* and a missing comma — expected from a different model, not a defect.

## Findings

### 1. On GNOME Wayland the real filter is text injection, not stars

Mutter does not expose `zwp_virtual_keyboard_v1` (so `wtype` fails) and Debian 13
does not package `ydotool`/`dotool`. Only four paths remain: **IBus**, **portals**
(RemoteDesktop / GlobalShortcuts), **evdev/uinput**, or **manual clipboard paste**.

| Tool | Injection on GNOME Wayland | Privileges |
|---|---|---|
| voiceio | IBus + GNOME custom shortcut → local socket | none |
| vocalinux | IBus | `/dev/input` for its own hotkey, or a D-Bus shortcut |
| hex | RemoteDesktop + GlobalShortcuts portals | none (portal prompts) |

### 2. `vocalinux`'s `.deb` ships a baseline ggml build

This is a packaging issue, not an engine issue. Evidence:

```
$ whisper_backend_init_gpu: no GPU found
$ ls /usr/lib/vocalinux/vendor/ | grep ggml
libggml-base.so  libggml-cpu.so  libggml.so      # no AVX2 variant, no Vulkan
```

Same whisper.cpp model that `hex` runs on Vulkan is 6.8× slower in that `.deb`.
Their AppImage/Flatpak ship a Vulkan build; the `.deb` does not.

### 3. `hex` is the most polished product, with a quiet Linux beta

Portals, vocabulary, output steps, history, a local API. On GNOME its Wayland
beta gives no visual feedback while recording, and its own release notes say it
"does not claim GNOME or KDE support". It works — silently.

## Limitations

- **Batch decode, not end-to-end latency.** We time `transcribe(file)` on the
  same WAV. Mic → text latency depends on each app's streaming/chunking.
- **n = 1 per tool**, one machine, one speaker, one language (Spanish).
- Models differ between voiceio (small) and hex (large-v3-turbo); the only
  same-model comparison here is voiceio vs vocalinux (both `small`).
- Versions are pinned above; anything newer may differ.
- `hex`'s headless transcribe reported 4.0 s on `auto` and 4.3 s with
  `transcription_device=cpu`; we did not isolate the device in that path.
  `hex model check` confirms the model loads on `AMD Radeon RX 6950 XT (RADV NAVI21) (vulkan)`.

## Reproduce

```bash
# 1. Same sample: any 16 kHz mono WAV of 10-20 s works.
# 2. Add your own paths/models in scripts/ (two self-contained Python files).

# voiceio's engine (faster-whisper, CPU):
python3 -m venv .venv && . .venv/bin/activate
pip install faster-whisper
python scripts/bench_faster_whisper.py sample.wav --model small --threads 6

# whisper.cpp (needs a ggml model, e.g. ggml-small.bin):
python scripts/bench_whispercpp.py sample.wav --model ggml-small.bin --threads 6
```

## License

Text: CC BY 4.0. Scripts: MIT.
