# Banco de temas

Regla: la tarea programada toma **el primer pendiente**, lo publica y lo mueve a
«usados» con la fecha. Cuando queden **menos de 8 pendientes en cualquiera de las
dos listas**, la tarea tiene que investigar y agregar temas nuevos antes de
terminar. El banco nunca se vacía.

---

## EN COLA — ya armados, esperando su turno

| Archivo | Tipo | Tema |
|---|---|---|
| 010 | valor | Los colores que se están viendo este año |
| 011 | promoción | Las mismas preguntas por WhatsApp |
| 012 | valor | Traje de novio a la medida: los tiempos |
| 013 | promoción | El bloque de hotel que nadie usó |
| 014 | valor | Dos pares de zapatos |
| 015 | promoción | La galería sigue viva después de la boda |

Ojo: estos ya no están en las listas de pendientes de abajo. Cuando GitHub los
publique, pasan solos a «usados» y salen de la cola.

---

## VALOR — pendientes

Consejo práctico de organización de boda. No mencionan la página ni venden nada.

2. Cuánto tarda cada trámite del civil y cuándo hay que empezarlo
4. Menú: cuántos tiempos aguantan de verdad los invitados
5. Música: a qué hora conviene pasar de banda a DJ
6. Maquillaje de prueba: cuándo hacerlo y qué llevar
7. Boda de día contra boda de noche: qué cambia en el presupuesto
8. El brindis: cuántos discursos antes de que la gente se aburra
10. Cómo armar el bloque de hotel sin quedar mal con nadie
11. El orden real del día: qué pasa entre el civil y el brindis
12. Qué preguntar antes de firmar con el salón
13. Cómo repartir el presupuesto: en qué se va de verdad
14. Fotógrafo: qué entregables pedir por contrato
15. El pastel: cuándo se corta y cuánto rinde por invitado
16. Flores de temporada: bajar el costo sin bajar la vista
17. Niños en la boda: mesa de actividades o niñera
18. Transporte de invitados: cuándo conviene contratar camión
19. Boda en playa: qué llevar de más
20. El civil en casa: qué se necesita para que vaya el juez
21. Invitados que vienen de fuera: qué se acostumbra resolverles
22. Papelería: qué se sigue imprimiendo y qué ya no
23. El ensayo: para qué sirve de verdad y quién debe ir
24. Cómo elegir padrinos sin pelearte con la familia
25. El vestido: cuántas pruebas y en qué momento comprarlo
26. Barra libre: opciones y cómo calcular cantidades
27. Fotos de grupo: cómo sacarlas rápido y sin perder la fiesta
28. La hora dorada: por qué define tu sesión de fotos
29. El día después: tornaboda o desayuno, qué conviene
30. Seguro por lluvia o cancelación: cuándo tiene sentido

## VALOR — usados

| Fecha | Tema |
|---|---|
| 2026-08-04 | Toldo para boda en jardín en temporada de lluvias |

---

## PROMOCIÓN — pendientes

Estructura fija: portada con contexto de boda → el problema → cómo lo resuelve la
página → CTA por DM. Nunca precio, nunca país, nunca liga a la web.

2. La mesa de regalos que nadie encuentra
5. Una sola dirección en lugar de mil mensajes
6. El itinerario que cambia y hay que reavisarle a todos
7. Los que confirman y luego no llegan
8. El código de vestimenta que nadie entendió
9. Cuando la boda es en otra ciudad
10. Los papás que quieren invitar a más gente de la que cabe
11. Confirmar desde el celular, sin descargar nada
12. Cuando hay dos ceremonias en días distintos
13. La invitación impresa que llegó tarde
14. Lo que pasa con la página el día después de la boda
15. Cómo se ve la lista cuando ya todos contestaron

## PROMOCIÓN — usados

| Fecha | Tema |
|---|---|
| 2026-08-04 | La lista de invitados vive en cuatro lados |

---

## Fotos: dónde está cada una

| Foto | Ya publicada | En cola | Estado |
|---|---|---|---|
| arcos-cantera | 1 | 0 | en el feed |
| azotea-urbana | 1 | 0 | en el feed |
| banquete-toldo | 1 | 0 | en el feed |
| calle-colonial | 1 | 0 | en el feed |
| cipreses-hacienda | 1 | 0 | en el feed |
| civil-terraza | 2 | 0 | en el feed |
| damas-vistiendo | 0 | 1 | en cola |
| dia-jardin | 1 | 0 | en el feed |
| fiesta-noche | 0 | 1 | en cola |
| frentes-buganvilia | 1 | 0 | en el feed |
| fuente-hacienda | 1 | 0 | en el feed |
| iglesia-vitral | 0 | 0 | **libre** |
| jardin-tropical | 1 | 0 | en el feed |
| manos-anillos | 1 | 0 | en el feed |
| mesa-banquete | 1 | 0 | en el feed |
| novio-espejo | 2 | 0 | en el feed |
| papeleria-mesa | 0 | 0 | **libre** |
| pareja-mayor-jardin | 0 | 1 | en cola |
| playa-atardecer | 1 | 0 | en el feed |
| ramo-manos | 0 | 0 | **libre** |

**Regla, y ahora la revisa el código:** ninguna foto que ya salió al feed vuelve a
aparecer, ni de portada ni en el interior. `revisar_contra_el_feed()` en `base.py`
compara las láminas contra el diccionario `YA_EN_EL_FEED` de `lote_agosto.py` y hace
fallar la compilación si encuentra una repetida. Cuando publiques algo, agrega sus
fotos a ese diccionario: es la única lista que manda.

Quedan **3 fotos libres**: iglesia-vitral, papeleria-mesa, ramo-manos. Con dos publicaciones en cola,
la siguiente sesión de contenido ya tiene que traer fotos nuevas (ver README) o
resolverse con láminas tipográficas.

Las cuatro últimas se agregaron para romper la monotonía: el banco entero era
luz dorada de tarde en hacienda. `dia-jardin` mete luz de mediodía y verdes
frescos, `mesa-banquete` es un detalle sin gente, `novio-espejo` es interior de
tonos fríos y `fiesta-noche` es la única nocturna. Cuando elijas foto para una
publicación, fíjate en que no repita la *luz* de la anterior, no solo el
archivo.

### La regla que ahora vigila el código

En el feed se vieron dos publicaciones distintas abriendo con la misma foto y se
notó feísimo. Ya no puede volver a pasar sin que alguien lo vea: al generar, el
script averigua qué foto usa cada lámina —la imagen va incrustada en el archivo,
así que no hace falta que nadie lo declare— y revienta si:

- una foto abre dos publicaciones distintas, contando las que ya salieron al feed
- una foto aparece más de una vez dentro del mismo carrusel

Si el build falla por esto, no lo saltes: elige otra foto o haz la portada
tipográfica, que además rompe mejor la cuadrícula.
