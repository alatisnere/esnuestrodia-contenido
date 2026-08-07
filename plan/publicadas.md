# Bitácora

Contrastada contra el feed real de instagram.com/esnuestrodia, no de memoria.
El feed manda: si algo aparece ahí y no está anotado aquí, se anota.

| Fecha | Tipo | Tema | Fotos que consumió |
|---|---|---|---|
| 2026-08-03 | Presentación | Quiénes somos y qué encontrarán aquí | arcos-cantera, calle-colonial |
| 2026-08-04 | Valor | Toldo para boda en jardín en temporada de lluvias | jardin-tropical, cipreses-hacienda |
| 2026-08-05 | Promoción | La lista de invitados vive en cuatro lados | civil-terraza, frentes-buganvilia |
| 2026-08-06 | Promoción | Las mismas preguntas por WhatsApp | civil-terraza |
| 2026-08-06 | Valor | Los colores que se están viendo este año | mesa-banquete, dia-jardin |
| 2026-08-07 | Valor | Traje de novio a la medida: los tiempos | novio-espejo, azotea-urbana, manos-anillos |

`civil-terraza` salió dos veces, el 5 y el 6 de agosto, y se nota en la cuadrícula:
las publicaciones 2 y 4 del perfil son visiblemente la misma foto. Fue antes de que
existiera la revisión automática. No debería volver a pasar.

## Lo que queda en cola

| Archivo | Tipo | Tema |
|---|---|---|
| 013 | Promoción | El bloque de hotel que nadie usó |
| 014 | Valor | Dos pares de zapatos |
| 015 | Promoción | La galería sigue viva después de la boda |

## Cómo se llena

Una fila por publicación, **con las fotos que consumió**. Esa última columna no es
decorativa: es de donde sale el diccionario `YA_EN_EL_FEED` de
`plantillas/lote_agosto.py`, que es lo que impide que una foto se repita. Si no
anotas las fotos aquí, la revisión automática se queda ciega.

Cuando una publicación sale, su JSON se mueve de `cola/` a `publicadas/`. Si se queda
en `cola/` después de publicada, el flujo de GitHub la volvería a subir.
