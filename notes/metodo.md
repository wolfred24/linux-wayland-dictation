# Cómo encontré la herramienta equivocada (y qué método lo evitó)

Este documento es parte del dataset: el resultado importa menos que el proceso
que llevó a él.

## La pregunta

> "Busqué `voice dictation` en GitHub y voiceio aparece hasta la página 14.
> ¿Cómo fue que lo encontraste y me lo recomendaste?"

## Lo que realmente pasó

1. **No busqué en GitHub.** Hice una búsqueda web:
   `Linux dictation tool type into any app Wayland GNOME 2026 whisper`.
2. Los resultados fueron **páginas de contenido**, no rankings:
   `voiceio.dev/linux-voice-dictation/`, un artículo de itsfoss.com, dos
   comparativas de blipai.app, la documentación de OpenWhispr y un par de repos
   pequeños.
3. voiceio salió arriba porque tiene **páginas optimizadas para esa consulta**
   (título exacto, tabla "qué funciona dónde", subtítulos por distro).
4. Su documentación decía lo que yo necesitaba comprobar:
   *"GNOME (Wayland) — IBus, ydotool fallback — tested daily"*.
5. Verifiqué en la máquina que `ydotool`/`dotool` no existen en Debian 13 y que
   `wtype` no funciona en GNOME. La afirmación encajaba con la restricción dura.
6. Recomendé. **Nunca miré estrellas, releases ni antigüedad.**

## Los tres errores

| Error | Consecuencia |
|---|---|
| Confundir visibilidad SEO con adopción | Un proyecto de 29★ pasó por delante de otros de 1k-12k★ |
| Apoyarme en listas de terceros | No hice el barrido `sort=stars` del nicho |
| No declarar el costo de madurez | Se presentó como "la opción" en vez de "la que encaja, pero joven" |

## El método corregido

1. **Definir las restricciones duras primero.** Aquí: GNOME 48 Wayland, Debian
   13, sin paquetes `ydotool`/`dotool`, `wtype` inservible, sin privilegios.
   Eso reduce el universo antes de mirar herramientas.
2. **Barrer GitHub por tracción**, no por una sola consulta web: varias
   formulaciones (`linux dictation whisper`, `voice dictation linux wayland`,
   `speech to text linux desktop`, `dictation type anywhere linux`), agregar,
   deduplicar y ordenar por estrellas.
3. **Leer en cada candidato la sección de la restricción** (no el README
   completo): ¿cómo inyecta texto?, ¿qué permisos pide?, ¿qué empaqueta?
4. **Verificar en la máquina**, no en la promesa.
5. **Medir** con el mismo audio y declarar límites.
6. **Presentar la lista corta con madurez**: estrellas, releases, mantenedores,
   fecha del último push, y el costo de cada opción.

## La lección generalizable

> Una página bien posicionada en Google no es señal de madurez ni de
> mantenimiento. La popularidad tampoco garantiza que funcione en *tu* caso.

Lo correcto es separar tres ejes y no colapsarlos:

- **Encaje técnico** (¿resuelve tu restricción?)
- **Madurez** (¿cuánta gente lo usa y lo mantiene?)
- **Costo de adopción** (¿qué permisos, paquetes o compilaciones pide?)

En este caso el eje 1 apuntaba a voiceio, el 2 a otros, y el 3 también a voiceio.
El resultado final fue bueno, pero **por accidente de descubrimiento**, no por
método. Ese es el error que este repo documenta.
