# Borrador Reddit (español) — r/linux_es, r/debian o r/es

**Título:** Medí tres herramientas de dictado local en GNOME Wayland: ganó la de 29 estrellas, y los números explican por qué

**Cuerpo:**

Contexto: Debian 13, GNOME 48, Wayland. Quería dictado en cualquier ventana, en
español y sin nube. Lo habitual es `ydotool`, pero Debian 13 no lo empaqueta y
`wtype` no funciona en GNOME (no expone el protocolo de teclado virtual). Así que
medí lo que sí funciona sin privilegios extra.

Mismo WAV de 17.6 s en español para todas, decodificación greedy, una sola
máquina (Ryzen 5 5600G, RX 6950 XT, 15 GiB):

| Herramienta | Modelo | Runtime | Tiempo | Tiempo real |
|---|---|---|---|---|
| voiceio 1.18.14 | whisper small int8 (244M) | CTranslate2, CPU 6 hilos | **1.55 s** | **11.3×** |
| hex 3.4.0 | whisper large-v3-turbo Q8 (809M) | whisper.cpp + Vulkan | 4.00 s | 4.4× |
| vocalinux 0.18.6 | whisper small | whisper.cpp base, CPU 6 hilos | 27.40 s | 0.6× |

La precisión fue idéntica entre voiceio y vocalinux (mismo modelo). Hex difirió en
una palabra, esperable al usar otro modelo.

Lo interesante es *por qué*:

- El **`.deb` de vocalinux** trae solo `libggml-cpu.so` base (sin variante AVX2 ni
  backend Vulkan), por eso whisper.cpp va lentísimo. Su AppImage/Flatpak sí traen
  Vulkan. Abrí un issue con la evidencia: es un bug de empaquetado, no un mal
  proyecto.
- **hex** es el producto más pulido y sí usa la GPU
  (`hex model check` → `ready ... (vulkan)`), pero su beta de Linux es silenciosa
  en GNOME: no da feedback mientras graba.
- **voiceio** (29 estrellas) ganó en velocidad porque CTranslate2 int8 está muy
  optimizado para CPU, y escribe por IBus con **cero permisos extra** (sin grupo
  `input`, sin `ydotool`).

Salvedades: medí decodificación por lotes, no latencia de extremo a extremo; n=1
por herramienta; una máquina y un hablante. Versiones y hardware fijados en el repo.

Números, scripts y logs crudos: `https://github.com/wolfred24/linux-wayland-dictation`

Con gusto respondo dudas o repito la medición con otra muestra si alguien quiere
comparar en hardware distinto.
