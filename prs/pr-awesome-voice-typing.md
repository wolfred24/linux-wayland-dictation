# PR draft — primaprashant/awesome-voice-typing

## Change

Add `voiceio` to the Directory table, alphabetically after *VoiceFlow*.

```markdown
| [voiceio](https://github.com/Hugo0/voiceio)<br/><br/>![stars](https://img.shields.io/github/stars/Hugo0/voiceio?style=plastic&label=%E2%98%85) | Linux | Local | Faster Whisper, whisper.cpp | Offline dictation that reaches IBus, ydotool, wtype or the clipboard, so it types in any app on GNOME/KDE Wayland without extra permissions; vocabulary, corrections and learning from your own recordings. |
```

## Optional second change (same PR)

The Vocalinux row links to the old repository owner. The project now lives at
`VocaHQ/vocalinux`:

```diff
-| [Vocalinux](https://github.com/jatinkrmalik/vocalinux)<br/>...
+| [Vocalinux](https://github.com/VocaHQ/vocalinux)<br/>...
```

## PR body

> Adds **voiceio** (`Hugo0/voiceio`, MIT) to the directory.
>
> Worth listing for a specific reason: on GNOME Wayland it types through **IBus**,
> so it works without `ydotool`, without `wtype` (GNOME does not expose the
> virtual-keyboard protocol) and without the `input` group. On Debian 13 none of
> those helpers are packaged, which is exactly the case where the other options
> need extra setup.
>
> Measured on Debian 13 + GNOME 48 Wayland (Ryzen 5 5600G / RX 6950 XT), same
> 17.6 s Spanish WAV, greedy decoding:
>
> | Tool | Model | Time |
> |---|---|---|
> | voiceio (faster-whisper small int8, CPU) | 244M | 1.55 s |
> | hex (large-v3-turbo Q8, Vulkan) | 809M | 4.00 s |
> | vocalinux `.deb` (small, baseline ggml) | 244M | 27.40 s |
>
> Numbers, scripts and caveats: `https://github.com/wolfred24/linux-wayland-dictation`. Happy to trim the description if it
> is longer than the list's style.
