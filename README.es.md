# Dictado local en Debian 13 + GNOME 48 (Wayland): tres herramientas, medidas

Medido el **24 de noviembre de 2026**, en una sola máquina, con una sola muestra
de audio en español. Es un conjunto de datos pequeño y reproducible, no una
suite de benchmarks. Lee las [limitaciones](#limitaciones) antes de citar cifras.

**Resumen:** en GNOME Wayland hay tres herramientas que escriben en cualquier
ventana sin privilegios extra. En este hardware, `voiceio` (29 estrellas)
decodificó la muestra **7× más rápido** que `hex` con un modelo 3× más grande, y
**17× más rápido** que el `.deb` de `vocalinux` — por el *runtime empaquetado*,
no por la calidad del modelo.

## Entorno

| | |
|---|---|
| SO | Debian GNU/Linux 13 (trixie) |
| Escritorio | GNOME Shell 48.7, **Wayland** |
| CPU | AMD Ryzen 5 5600G (6C/12T) |
| GPU | AMD Radeon RX 6950 XT (RADV NAVI21), Mesa 25.0.7, libvulkan 1.4.309 |
| RAM | 15 GiB |
| Micrófono | Behringer UMC202HD 192k (USB) |
| Muestra | 17.6 s de voz en español, WAV 16 kHz mono, el mismo archivo en todas las corridas |

## Resultados (mismo audio, decodificación greedy)

| Herramienta | Versión | Modelo | Runtime | Tiempo | Tiempo real | Texto |
|---|---|---|---|---|---|---|
| **voiceio** | 1.18.14 (`.deb`) | faster-whisper `small` int8 (244M) | CTranslate2, CPU, 6 hilos | **1.55 s** | **11.3×** | referencia |
| **hex** | 3.4.0 (`.deb`) | whisper.cpp `large-v3-turbo` Q8_0 (809M) | whisper.cpp + **Vulkan** | 4.00 s | 4.4× | 1 palabra distinta |
| **vocalinux** | 0.18.6 (`.deb`) | whisper.cpp `small` | whisper.cpp, **ggml base**, CPU, 6 hilos | 27.40 s | **0.6×** | referencia |

`vocalinux` con 12 hilos: 31.8 s (memory-bound, más lento).

Transcripción de referencia (voiceio y vocalinux, salida idéntica):

> Ok, a ver, vamos a probar la dictación. En este momento, justamente le estoy
> dictando al micrófono de la computadora y vamos a ver si escribe lo que le
> estoy dictando.

`hex` produjo el mismo texto salvo *"la estoy dictando"* en lugar de *"le estoy
dictando"* y una coma de menos: esperable al usar otro modelo, no es un defecto.

## Hallazgos

### 1. En GNOME Wayland el filtro real es la inyección de texto, no las estrellas

Mutter no expone `zwp_virtual_keyboard_v1` (por eso `wtype` falla) y Debian 13 no
empaqueta `ydotool`/`dotool`. Solo quedan cuatro caminos: **IBus**, **portales**
(RemoteDesktop / GlobalShortcuts), **evdev/uinput** o **pegado manual del portapapeles**.

| Herramienta | Inyección en GNOME Wayland | Privilegios |
|---|---|---|
| voiceio | IBus + atajo de GNOME → socket local | ninguno |
| vocalinux | IBus | `/dev/input` para su propio atajo, o un atajo D-Bus |
| hex | portales RemoteDesktop + GlobalShortcuts | ninguno (con permiso del portal) |

### 2. El `.deb` de `vocalinux` trae una compilación base de ggml

Es un problema de empaquetado, no del motor. Evidencia:

```
$ whisper_backend_init_gpu: no GPU found
$ ls /usr/lib/vocalinux/vendor/ | grep ggml
libggml-base.so  libggml-cpu.so  libggml.so      # sin variante AVX2, sin Vulkan
```

El mismo modelo de whisper.cpp que `hex` corre en Vulkan es **6.8× más lento** en
ese `.deb`. Su AppImage/Flatpak sí traen Vulkan; el `.deb` no.

### 3. `hex` es el producto más pulido, con una beta de Linux silenciosa

Portales, vocabulario, pasos de salida, historial, API local. En GNOME su beta de
Wayland no da retroalimentación visual al grabar, y sus propias notas de release
dicen que "no reclama soporte de GNOME o KDE". Funciona — en silencio.

## Limitaciones

- **Decodificación por lotes, no latencia de extremo a extremo.** Medimos
  `transcribe(archivo)` sobre el mismo WAV. La latencia micrófono → texto depende
  del streaming/chunking de cada app.
- **n = 1 por herramienta**, una máquina, un hablante, un idioma (español).
- Los modelos difieren entre voiceio (small) y hex (large-v3-turbo); la única
  comparación con el mismo modelo es voiceio vs vocalinux (ambos `small`).
- Las versiones están fijadas arriba; versiones nuevas pueden cambiar el resultado.
- El transcribe headless de `hex` dio 4.0 s en `auto` y 4.3 s con
  `transcription_device=cpu`; no aislamos el dispositivo en esa ruta.
  `hex model check` confirma que el modelo carga en `AMD Radeon RX 6950 XT (RADV NAVI21) (vulkan)`.

## Reproducir

```bash
# 1. Misma muestra: sirve cualquier WAV mono de 16 kHz de 10-20 s.
# 2. Los dos scripts son autocontenidos; ajusta rutas/modelos.

# Motor de voiceio (faster-whisper, CPU):
python3 -m venv .venv && . .venv/bin/activate
pip install faster-whisper
python scripts/bench_faster_whisper.py muestra.wav --model small --threads 6

# whisper.cpp (necesita un modelo ggml, p. ej. ggml-small.bin):
python scripts/bench_whispercpp.py muestra.wav --model ggml-small.bin --threads 6
```

## Licencia

Texto: CC BY 4.0. Scripts: MIT.
