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
