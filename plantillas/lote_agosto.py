"""
Seis publicaciones: tres de valor y tres de promoción.

Cada una tiene su propia firma visual —color de fondo, textura, tratamiento de
la foto y disposición— para que dos seguidas no se vean iguales en el feed. Lo
que las mantiene de la misma familia son las tipografías, el isotipo y que
todos los tonos son apagados.

  colores   arcilla + olivo · grano     · foto cálida    · muestras de color
  preguntas bosque + hueso   · acuarela  · foto fría      · foto partida
  traje     cacao + arena    · rayado    · foto en gris   · cifra grande
  hotel     azul + hueso     · puntos    · foto apagada   · banda de foto
  zapatos   vino + salvia    · rayado    · foto cálida    · cifra grande
  galería   salvia + tinta   · acuarela  · foto normal    · frase suelta
"""

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from base import (portada_color, portada_tipografica, cierre_color, cta_dm_color, texto_color,
                  lista_color, muestras, banda, cita, dato, partido,
                  render, revisar, contraste_sobre_foto)

RAIZ = pathlib.Path(__file__).resolve().parent.parent
LISTOS = RAIZ / "listos"
COLA = RAIZ / "cola"
POSTS = []


def post(archivo, tipo, titulo, prefijo, laminas, caption):
    malos = revisar(laminas)
    if malos:
        raise SystemExit(f"{prefijo}: fuentes por debajo de 32 px: {malos}")
    if len(caption) > 2200:
        raise SystemExit(f"{prefijo}: el copy tiene {len(caption)} caracteres")
    if caption.count("#") > 30:
        raise SystemExit(f"{prefijo}: demasiados hashtags")
    peor = min((r for _, r in contraste_sobre_foto(laminas)), default=99)
    if peor < 4.5:
        raise SystemExit(f"{prefijo}: contraste sobre foto insuficiente ({peor})")
    rutas = render(laminas, prefijo, LISTOS)
    datos = {"tipo": tipo, "titulo": titulo,
             "imagenes": [str(r.relative_to(RAIZ)) for r in rutas],
             "caption": caption}
    (COLA / archivo).write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")
    POSTS.append((archivo, prefijo, len(rutas), len(caption), peor))


# ══════════════════════════════ VALOR 1 · Colores ═══════════════════════
# Firma: arcilla y olivo, textura de grano, foto cálida.
V1 = [
    portada_tipografica("Decoración de boda",
                        "Los colores<br>que se están<br>viendo este año",
                        "Y uno que ya venía de salida.",
                        "Desliza · la combinación que más se repite",
                        "arcilla", "grano",
                        muestras_color=["#B0603F", "#EFE6D8", "#6B7048"]),
    texto_color("Decoración de boda", "Terracota, crema<br>y verde olivo",
                "Si todavía estás eligiendo los colores del banquete, esa es la "
                "combinación que más se repite entre las fuentes del sector para este "
                "año. Funciona porque los tres son tonos apagados: se llevan bien con "
                "la madera, con la cantera y con la luz de la tarde.",
                "arcilla", "grano"),
    partido("ramo-manos", "Para acentos y centros de mesa",
            "Cómo se ve<br>junto",
            "Los tres tonos son apagados, así que ninguno pelea con el otro ni con la "
            "luz de la tarde. Es lo que hace que funcione en fotos.",
            "hueso", pos="center 30%", trato="calido", tex="grano"),
    muestras("Para acentos y centros de mesa", "La paleta, en corto",
             [("Terracota", "#B0603F", "Servilletas, velas, listón"),
              ("Crema", "#EFE6D8", "Mantelería y vajilla"),
              ("Verde olivo", "#6B7048", "Follaje y tallos")],
             "Dos apagados y uno cálido. Si metes un cuarto color, que sea metal: "
             "latón mate antes que dorado brillante.", "papel"),
    texto_color("Lo que va de salida", "El azul empolvado<br>y el verde salvia",
                "Llevan tres años en todas las bodas y las floristerías ya lo notan: "
                "se están enfriando. En su lugar suben los verdes más profundos "
                "—bosque, esmeralda— y los marrones cálidos tipo chocolate o café con "
                "leche.<br><br>Si ya los tenías apartados, tampoco pasa nada. Nadie en "
                "tu boda va a pensar «qué salvia tan de 2023».",
                "olivo", "grano"),
    texto_color("Un dato que sirve", "El color del año<br>es blanco",
                "Pantone eligió para 2026 un blanco suave que llamó <i>Cloud "
                "Dancer</i>. Es el primer blanco puro que eligen desde que existe el "
                "programa.<br><br>Para una boda es buena noticia: el blanco roto como "
                "base deja que los acentos hagan todo el trabajo, y sale más barato "
                "que llenar el salón de color.",
                "hueso", "acuarela"),
    cierre_color("jardin-tropical", "No te cases<br>con la tendencia.",
                 "Una wedding planner lo dijo mejor que nosotros: de cada veinte "
                 "bodas, en una se ve de verdad la paleta que anuncian las revistas. "
                 "Elige el color que te guste a ti y usa la lista como referencia, no "
                 "como regla.",
                 "Guárdalo para cuando cotices la decoración",
                 pos="center 40%", trato="calido", tinte_color="olivo", op=.26),
]

CAP_V1 = """Si todavía estás eligiendo los colores del banquete, la combinación que más se repite este año es terracota, crema y verde olivo.

Funciona porque los tres son tonos apagados. Se llevan bien con la madera, con la cantera y con la luz de la tarde, que es cuando se ve casi todo tu banquete. Si quieres meter un cuarto, que sea metal: latón mate antes que dorado brillante.

Lo que va de salida es el azul empolvado y el verde salvia. Llevan tres años en todas las bodas y las floristerías ya lo están notando. En su lugar suben los verdes profundos, tipo bosque o esmeralda, y los marrones cálidos. Si ya los tenías apartados, tampoco te agobies: nadie en tu boda va a pensar «qué salvia tan de 2023».

Un dato que sirve más de lo que parece: Pantone eligió como color del año un blanco suave, Cloud Dancer. Es el primer blanco puro desde que existe el programa. Para una boda es buena noticia, porque un blanco roto como base deja que los acentos hagan todo el trabajo y sale bastante más barato que llenar el salón de color.

Y una advertencia honesta. Una wedding planner lo dijo mejor que nosotros: de cada veinte bodas, en una se ve de verdad la paleta que anuncian las revistas. Usa esto como referencia, no como regla. El color que se va a ver en las fotos toda la vida es el que les gusta a ustedes dos.

Guarda este post para cuando te sientes a cotizar la decoración, o mándaselo a esa pareja que sigue peleada con la paleta.

#bodas #decoraciondebodas #paletadecolores #tendenciasdebodas #novios2027 #organizaciondebodas #banquetedeboda #centrosdemesa"""


# ══════════════════════════ PROMOCIÓN 1 · Preguntas ═════════════════════
# Firma: bosque y hueso, acuarela, foto fría, una lámina partida.
P1 = [
    portada_color("civil-terraza", "Organizando tu boda",
                  "«Oye, ¿a qué<br>hora era el civil?»",
                  "Por decimoquinta vez esta semana.",
                  "Desliza", pos="center 30%", trato="frio",
                  tinte_color="bosque", op=.24),
    texto_color("El problema", "No es que no<br>pongan atención",
                "Es que la información está repartida: la hora en un mensaje de hace "
                "dos meses, la dirección en otro, el cambio de última hora en el grupo "
                "donde no está tu tía. Nadie va a buscar entre trescientos mensajes. "
                "Te preguntan a ti, que es más rápido.",
                "hueso", "acuarela"),
    texto_color("Cómo lo resolvemos", "Una sola dirección<br>con todo adentro",
                "Te hacemos la página de tu boda: el itinerario con horas y lugares, "
                "cómo llegar, los hoteles, el código de vestimenta, la mesa de regalos "
                "y la confirmación de asistencia.<br><br>Compartes el link una vez. "
                "Cuando algo cambia, lo cambias ahí y ya está cambiado para todos.",
                "bosque", "acuarela"),
    cta_dm_color("civil-terraza", "Te la hacemos<br>a mano, con ustedes.",
                 "Vemos juntos qué secciones necesita tu boda y cuáles sobran. En dos "
                 "semanas está lista.", "boda",
                 pos="center 60%", trato="frio", tinte_color="bosque", op=.26),
]

CAP_P1 = """«Oye, ¿a qué hora era el civil?». Por decimoquinta vez esta semana.

No es que tus invitados no pongan atención. Es que la información está repartida: la hora en un mensaje de hace dos meses, la dirección en otro, el cambio de última hora en el grupo donde no está tu tía. Nadie va a ponerse a buscar entre trescientos mensajes. Te preguntan a ti, que es más rápido.

Nosotros te hacemos la página de tu boda con todo adentro: el itinerario con horas y lugares, cómo llegar, los hoteles, el código de vestimenta, la mesa de regalos y la confirmación de asistencia. Compartes el link una vez y ya. Cuando algo cambia, lo cambias ahí y queda cambiado para todos al mismo tiempo.

No es una plantilla donde le cambias la foto y el nombre. Nos sentamos contigo, vemos qué secciones necesita tu boda y cuáles sobran, y la armamos. En dos semanas está lista.

Escríbenos «boda» por DM y te mandamos una de ejemplo para que la abras en tu celular, que es donde la van a abrir tus invitados. Contestamos el mismo día.

#bodas #invitaciondigital #paginadeboda #organizaciondebodas #novios2027 #planeaciondeboda #invitacionesdeboda #mecaso"""


# ══════════════════════════════ VALOR 2 · Traje ═════════════════════════
# Firma: cacao y arena media, rayado, foto en blanco y negro, cifra grande.
V2 = [
    portada_color("arcos-cantera", "Traje de novio",
                  "¿El novio va<br>a mandar a hacer<br>su traje?",
                  "Empieza antes de lo que crees.",
                  "Desliza · cuánto tarda de verdad",
                  pos="center 40%", trato="gris"),
    dato("4-6", "meses", "Traje de novio",
         "Es el margen que conviene darle antes de la boda. Y la primera pregunta al "
         "sastre no es el precio: es si la tela ya está en el taller o la tiene que "
         "traer.", "cacao", "rayado"),
    texto_color("Por qué esa pregunta", "La tela que hay<br>que traer suma<br>semanas",
                "Las sastrerías que publican sus tiempos cuentan de una a tres semanas "
                "extra cuando la tela viene de fuera: envío más aduana.<br><br>Y hay un "
                "detalle de calendario que casi nadie te dice: las fábricas de tela "
                "italianas cierran entre tres y cuatro semanas en agosto. Un pedido "
                "hecho a finales de julio se puede quedar esperando todo ese mes.",
                "arena-media", "rayado"),
    partido("cipreses-hacienda", "Lo que sí toma tiempo", "Dos o tres<br>pruebas, no una",
            "Un traje a la medida de verdad lleva dos o tres pruebas, de media hora a "
            "una hora cada una, repartidas entre las semanas de confección. Si te "
            "ofrecen una sola, probablemente es semimedida: también está bien, pero es "
            "otra cosa y otro precio.",
            "hueso", pos="center 35%", trato="gris", tex="rayado"),
    lista_color("Antes de dejar el anticipo", "Cinco preguntas<br>para tu sastre",
                ["¿La tela ya está aquí o hay que pedirla?",
                 "¿Cuántas pruebas incluye y cuándo son?",
                 "¿Qué fecha de entrega me pones por escrito?",
                 "Si algo se retrasa, ¿qué plan hay?",
                 "¿Los ajustes de última hora se cobran?"],
                "cacao", "rayado"),
    cierre_color("arcos-cantera", "El traje no es<br>lo que se retrasa.<br>Es la tela.",
                 "Nadie se acuerda de esto hasta que faltan seis semanas y el sastre "
                 "dice que el corte viene en camino. Preguntarlo el primer día no "
                 "cuesta nada.",
                 "Mándaselo al novio, que se le va a olvidar",
                 pos="center 20%", trato="gris"),
]

CAP_V2 = """Si el novio va a mandar a hacer su traje a la medida, empieza entre cuatro y seis meses antes de la boda. Y la primera pregunta al sastre no es el precio: es si la tela ya está en el taller o la tiene que traer.

De ahí sale casi toda la diferencia entre entregar a tiempo y entregar con prisas. Las sastrerías que publican sus tiempos cuentan de una a tres semanas extra cuando la tela viene de fuera, entre el envío y la aduana. Y hay un detalle de calendario que casi nadie te dice: las fábricas de tela italianas cierran entre tres y cuatro semanas en agosto. Un pedido hecho a finales de julio se puede quedar esperando todo ese mes sin que nadie te avise.

Lo otro que toma tiempo son las pruebas. Un traje a la medida de verdad lleva dos o tres, de media hora a una hora cada una, repartidas entre las semanas de confección. Si te ofrecen una sola prueba, lo más probable es que sea semimedida. También está bien, pero es otra cosa y es otro precio: que quede claro desde el principio para que nadie se sienta engañado.

Cinco preguntas antes de dejar el anticipo:
¿la tela ya está aquí o hay que pedirla?
¿cuántas pruebas incluye y cuándo son?
¿qué fecha de entrega me pones por escrito?
si algo se retrasa, ¿qué plan hay?
¿los ajustes de última hora se cobran?

Nadie se acuerda de esto hasta que faltan seis semanas y el sastre dice que el corte viene en camino. Preguntarlo el primer día no cuesta nada.

Mándaselo al novio, que es al que se le va a olvidar.

#bodas #trajedenovio #novio #consejosdeboda #organizaciondebodas #novios2027 #planeaciondeboda #sastreria"""


# ══════════════════════════ PROMOCIÓN 2 · Hotel ═════════════════════════
# Firma: azul y hueso, puntos, foto apagada, banda de foto.
P2 = [
    portada_color("calle-colonial", "Invitados de fuera",
                  "«¿Y dónde nos<br>quedamos?»",
                  "La pregunta que llega a las once de la noche.",
                  "Desliza", pos="center 40%", trato="apagado",
                  tinte_color="azul", op=.26),
    banda("calle-colonial", "El problema", "El bloque de hotel<br>que nadie usó",
          "Apartaste habitaciones con tarifa especial, mandaste el código por WhatsApp "
          "y la mitad reservó por su cuenta más caro, porque para cuando fueron a "
          "reservar ya no encontraban el mensaje.",
          "hueso", pos="center 65%", alto=520, trato="apagado", tex="puntos"),
    texto_color("Cómo lo resolvemos", "Los hoteles, con<br>su liga, en la página",
                "Cada hotel con su precio, su distancia al salón y el botón para "
                "reservar. El código de descuento ahí mismo, donde no se pierde."
                "<br><br>Los que vienen de fuera entran una vez y resuelven todo: dónde "
                "dormir, a qué hora llegar y qué ponerse.",
                "azul", "puntos"),
    cta_dm_color("calle-colonial", "Sobre todo si tu<br>boda es de destino.",
                 "Cuando la mitad de la lista viaja, la página deja de ser un lujo y se "
                 "vuelve lo que evita cincuenta llamadas.", "boda",
                 pos="center 20%", trato="apagado", tinte_color="azul", op=.28),
]

CAP_P2 = """«Oigan, ¿y dónde nos quedamos?». La pregunta que siempre llega a las once de la noche.

Apartaste habitaciones con tarifa especial, mandaste el código por WhatsApp y aun así la mitad de tus invitados reservó por su cuenta y más caro. No por descuidados: para cuando se sentaron a reservar, el mensaje ya estaba enterrado. Y tú te quedas con habitaciones apartadas que hay que pagar o liberar antes de la fecha límite.

En la página de tu boda los hoteles van con su precio, su distancia al salón y el botón para reservar. El código de descuento ahí mismo, donde no se pierde. Los que vienen de fuera entran una vez y resuelven todo de una sentada: dónde dormir, a qué hora llegar y qué ponerse.

Si tu boda es de destino, esto deja de ser un lujo. Cuando la mitad de la lista viaja, la página es lo que te evita cincuenta llamadas.

Escríbenos «boda» por DM y te mandamos una de ejemplo para que la abras en tu celular. Contestamos el mismo día.

#bodas #bodadedestino #invitaciondigital #paginadeboda #organizaciondebodas #novios2027 #hospedaje #planeaciondeboda"""


# ═════════════════════════════ VALOR 3 · Zapatos ════════════════════════
# Firma: vino y salvia, rayado, foto cálida, cifra grande.
V3 = [
    portada_tipografica("El día de tu boda",
                        "Lleva dos pares<br>de zapatos.<br>En serio.",
                        "Los de las fotos y los de la fiesta.",
                        "Desliza · cuándo se hace el cambio",
                        "vino", "rayado"),
    dato("2", "pares", "El día de tu boda",
         "Uno para verse y otro para durar. El zapato que se ve increíble en las fotos "
         "casi nunca es el que aguanta seis horas de pie.", "vino", "rayado"),
    texto_color("El momento del cambio", "Después de las<br>fotos de grupo",
                "Ese es el punto natural. Ya pasó la ceremonia, ya se tomaron las fotos "
                "formales y todavía no abre la pista. Si esperas a que te duelan, vas a "
                "estar cambiándote a media pista con la falda en la mano.",
                "salvia", "rayado"),
    lista_color("Lo que sí conviene hacer", "Cuatro cosas<br>que ayudan",
                ["Estrenarlos en casa varias tardes antes",
                 "Que el segundo par tenga la misma altura",
                 "Dejarlos con alguien que no vaya a desaparecer",
                 "Suela lisa: pídele al salón que la raye o ponle cinta"],
                "hueso", "puntos"),
    cierre_color("fuente-hacienda", "La misma altura,<br>eso es lo clave.",
                 "Si el segundo par es más bajo, el vestido arrastra y te lo vas a "
                 "pisar toda la noche. Si ya lo mandaste a bastillar, llévale los dos "
                 "pares a la costurera y que mida con el más alto.",
                 "Guárdalo para cuando compres el vestido",
                 pos="center 15%", trato="calido", tinte_color="vino", op=.22),
]

CAP_V3 = """Lleva dos pares de zapatos el día de tu boda. Los de las fotos y los de la fiesta.

El zapato que se ve increíble en las fotos casi nunca es el que aguanta seis horas de pie. Cómpralos desde el principio los dos y date permiso de cambiarlos, que nadie va a estar mirándote los pies a las once de la noche.

El momento del cambio es después de las fotos de grupo. Ya pasó la ceremonia, ya se tomaron las formales y todavía no abre la pista. Si esperas a que te duelan, vas a terminar cambiándote a media pista con la falda en una mano.

Cuatro cosas que ayudan:
estrénalos en casa varias tardes antes, no el mismo día
que el segundo par tenga la misma altura que el primero
déjalos con alguien que no vaya a desaparecer a media fiesta
si la suela es lisa, pídele al salón que la raye o ponle cinta

Lo de la misma altura es lo más importante de la lista. Si el segundo par es más bajo, el vestido arrastra y te lo vas a pisar toda la noche. Si ya lo mandaste a bastillar, llévale los dos pares a la costurera y que mida con el más alto.

Guarda este post para cuando vayas a comprar el vestido, o compártelo con la que ya anda buscando los suyos.

#bodas #zapatosdenovia #vestidodenovia #consejosdeboda #novios2027 #organizaciondebodas #planeaciondeboda #noviareal"""


# ═════════════════════════ PROMOCIÓN 3 · Galería ════════════════════════
# Firma: salvia y tinta, acuarela, una frase suelta.
P3 = [
    portada_color("frentes-buganvilia", "Después de tu boda",
                  "Las fotos que<br>tus invitados<br>tomaron",
                  "Están en cien celulares y ahí se quedan.",
                  "Desliza", pos="center 30%", trato="normal"),
    cita("Las mejores fotos de<br>la noche están en la<br>galería de gente que<br>"
         "no vas a volver a ver<br>en meses.", "Es Nuestro Día", "tinta", "acuarela"),
    texto_color("Cómo lo resolvemos", "La página sigue ahí<br>cuando la boda<br>ya pasó",
                "Cuando el fotógrafo entrega, subimos la sesión a la misma dirección "
                "que ya compartiste. Tus invitados entran al mismo link de siempre y "
                "ahí están.<br><br>Sirve para los que no pudieron ir, para los papás "
                "que quieren enseñarlas y para ustedes dentro de diez años.",
                "salvia", "acuarela"),
    cta_dm_color("frentes-buganvilia", "No se acaba el día<br>de la boda.",
                 "La misma dirección que usaste para organizar todo se queda como el "
                 "lugar donde vive el recuerdo.", "boda",
                 pos="center 60%", trato="normal"),
]

CAP_P3 = """Las fotos que tus invitados tomaron en tu boda están en cien celulares distintos, y ahí se van a quedar.

Ya sabes cómo termina: alguien abre un álbum compartido, lo manda al grupo, suben fotos veinte personas el primer día y a la semana ya nadie entra. Las mejores fotos de la noche, las que no salieron en la sesión oficial, se quedan en la galería de gente que no vas a volver a ver en meses.

La página de tu boda sigue ahí cuando la boda ya pasó. Cuando el fotógrafo entrega, subimos la sesión a la misma dirección que ya compartiste con todos. Tus invitados entran al mismo link de siempre y ahí están. Sirve para los que no pudieron ir, para los papás que quieren enseñarlas y para ustedes dentro de diez años, cuando ya nadie se acuerde en qué nube quedaron.

Es la parte que casi nadie piensa cuando está eligiendo invitación, y es la que más se agradece después.

Escríbenos «boda» por DM y te mandamos una de ejemplo para que la veas completa. Contestamos el mismo día.

#bodas #fotografiadebodas #invitaciondigital #paginadeboda #galeriadeboda #novios2027 #organizaciondebodas #recuerdos"""


# ══════════════════════════════ construir ═══════════════════════════════
post("010-valor-colores-de-temporada.json", "valor",
     "Los colores que se están viendo este año", "valor-colores", V1, CAP_V1)
post("011-promocion-mismas-preguntas.json", "promocion",
     "Las mismas preguntas por WhatsApp", "promo-preguntas", P1, CAP_P1)
post("012-valor-traje-a-la-medida.json", "valor",
     "Traje de novio a la medida: los tiempos", "valor-traje", V2, CAP_V2)
post("013-promocion-bloque-de-hotel.json", "promocion",
     "El bloque de hotel que nadie usó", "promo-hotel", P2, CAP_P2)
post("014-valor-dos-pares-de-zapatos.json", "valor",
     "Dos pares de zapatos", "valor-zapatos", V3, CAP_V3)
post("015-promocion-galeria-despues.json", "promocion",
     "La galería sigue viva después de la boda", "promo-galeria", P3, CAP_P3)

for archivo, prefijo, n, largo, peor in POSTS:
    print(f"{archivo:44s} {prefijo:16s} {n} láminas  {largo:5d} car.  contraste {peor}")
