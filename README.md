# Es Nuestro Día — contenido de Instagram

Repositorio de trabajo de la cuenta [@esnuestrodia](https://instagram.com/esnuestrodia).
Lo usa la tarea programada de Cowork para armar y publicar sin intervención manual.

## Estructura

| Carpeta | Qué hay |
|---|---|
| `listos/` | Publicaciones ya aprobadas y listas para subir, con su copy en `listos/copys.md` |
| `fotos/` | Banco de fotografía generada con IA. Distintas parejas y estilos de boda |
| `marca/` | Tipografías (woff2), isotipo, logotipo, filete y texturas |
| `plantillas/` | `plantillas.py` — genera las láminas de 1080×1350 con Playwright |
| `plan/` | Reglas de diseño y de tono, banco de temas, y bitácora de lo publicado |

## Reglas que no se rompen

1. Contexto de boda visible en la portada. Siempre.
2. Ningún texto por debajo de 32 px sobre lienzo de 1080. Cuerpo entre 44 y 50 px.
3. Contraste mínimo 4.5:1. Sobre foto: velo arriba, velo abajo y sombra en el texto.
4. Tuteo. Frases que suenen a alguien hablando, no a copy publicitario.
5. Primero la recomendación completa, luego el detalle.
6. Las de valor no venden nada. Las de promoción cierran en DM.
   Solo la de presentación manda a la web.
7. Nunca mencionar país ni precio.

## Ritmo

- 13:30 — publicación de valor
- 20:30 — publicación de promoción

## Cómo publicar (sesión programada de Cowork)

1. Clonar este repo.
2. Leer `plan/publicadas.md` para saber qué toca y qué no repetir.
3. Si hay algo en `listos/` que corresponda a la franja, usarlo tal cual.
4. Si no, elegir tema del banco, investigar con búsqueda web, y generar las
   láminas con `plantillas/plantillas.py`.
5. Publicar en Instagram y anotar el resultado en `plan/publicadas.md`.

## El banco nunca se vacía

`plan/temas.md` tiene dos listas de pendientes: valor y promoción. La tarea
programada toma el primero de la lista que le toque, lo publica y lo pasa a
«usados» con la fecha.

**Regla de reposición:** si al terminar quedan menos de **8 pendientes** en
cualquiera de las dos listas, la tarea investiga con búsqueda web y agrega al
menos **10 temas nuevos** a esa lista antes de cerrar. Así nunca hay un día sin
material.

Fuentes para reponer temas de valor: qué está preguntando la gente en foros y
blogs de bodas, calendario del año (temporada de lluvias, meses de más bodas,
fechas de trámites), y las dudas que lleguen por DM o comentarios.

## Cuando se acaben las fotos

`plan/temas.md` lleva la cuenta de usos por foto. Ninguna se repite antes de tres
publicaciones. Si todas pasan de cuatro usos, hay que generar fotos nuevas con
Gemini a través del navegador (gemini.google.com), pidiendo formato vertical 4:5,
parejas y estilos de boda distintos a los que ya hay, y recortando la marca de agua
de la esquina inferior derecha antes de guardarlas en `fotos/`.
