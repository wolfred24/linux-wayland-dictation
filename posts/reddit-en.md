# Reddit draft (English) — r/linux (also fits r/gnome, r/debian)

**Title:** I measured three local dictation tools on GNOME Wayland: the one with 29 stars won, and the numbers explain why

**Body:**

Context: Debian 13, GNOME 48, Wayland. I wanted system-wide dictation in Spanish,
offline. The usual advice is `ydotool`, but Debian 13 doesn't package it and
`wtype` doesn't work on GNOME (no virtual-keyboard protocol). So I measured what
actually works without extra privileges.

Same 17.6 s Spanish WAV for every tool, greedy decoding, single machine
(Ryzen 5 5600G, RX 6950 XT, 15 GiB):

| Tool | Model | Runtime | Time | Realtime |
|---|---|---|---|---|
| voiceio 1.18.14 | whisper small int8 (244M) | CTranslate2, CPU 6 threads | **1.55 s** | **11.3×** |
| hex 3.4.0 | whisper large-v3-turbo Q8 (809M) | whisper.cpp + Vulkan | 4.00 s | 4.4× |
| vocalinux 0.18.6 | whisper small | whisper.cpp baseline, CPU 6 threads | 27.40 s | 0.6× |

Accuracy was identical between voiceio and vocalinux (same model). Hex differed
by one word, expected from a different model.

The interesting part is *why*:

- **vocalinux's `.deb`** ships only the baseline `libggml-cpu.so` (no AVX2
  variant, no Vulkan backend), so whisper.cpp crawls. Their AppImage/Flatpak ship
  Vulkan. I filed an issue with the evidence; it's a packaging bug, not a bad
  project.
- **hex** is the most polished product and really uses the GPU
  (`hex model check` → `ready ... (vulkan)`), but its Linux beta is silent on
  GNOME: no recording feedback while it works.
- **voiceio** (29 stars) won on speed because CTranslate2 int8 is very well
  optimised for CPU, and it types through IBus with **zero extra permissions**
  (no `input` group, no `ydotool`).

Caveats: batch decode, not end-to-end latency; n=1 per tool; one machine and one
speaker. Versions and hardware are pinned in the repo below.

All numbers, scripts and the raw logs: `https://github.com/wolfred24/linux-wayland-dictation`

Happy to answer questions or re-run with another sample if someone wants to
compare on different hardware.
