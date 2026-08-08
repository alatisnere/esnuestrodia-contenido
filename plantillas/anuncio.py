"""
Anuncio de una sola imagen: qué hacemos y qué trae la página.

No es una publicación de carrusel, así que no vive en `cola/`: es una pieza
suelta que se sube a mano o se usa como creatividad de pago. Por eso está en su
propio archivo y no dentro de `lote_agosto.py`.

Sale en dos tamaños desde la misma definición:
  1080×1350 (4:5) para el feed
  1080×1920 (9:16) para historias

`base.py` está clavado a 1080×1350 —el lienzo entra en el CSS y en el
verificador de contraste—, así que aquí se rehacen esas dos cosas con el alto
como parámetro. Todo lo demás —tipografías, isotipo, filete, fotos, texturas,
tratamientos y la paleta— se importa de `base.py`: si mañana cambia la marca,
cambia en un solo sitio y este anuncio la sigue.

Las mismas reglas de siempre, revisadas por código antes de escribir el JPEG:
nada por debajo de 32 px, contraste mínimo 4.5:1 sobre la foto.
"""

import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from playwright.sync_api import sync_playwright

from base import (FONTS, ISO, FIL, FOTO, TRATO, PAPEL, OSCURO,
                  ACENTO, TINTA, SUAVE, textura)

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "anuncios"
ANCHO = 1080

# La foto: papelería de boda sobre lino, sin gente. Es la que mejor aguanta
# una lista encima —clara, quieta, sin caras que compitan— y dice «boda» sin
# necesidad de explicarlo. Además rima con lo que vendemos: es el papel al que
# la página viene a sustituir.
LA_FOTO = "papeleria-mesa"

# Lo que entra en la lista. Sale de la sección «Lo que incluye» de
# esnuestrodia.com, recortado a etiqueta corta: en un anuncio se lee de un
# vistazo o no se lee.
INCLUYE = [
    "Su propia dirección",
    "Itinerario con mapas",
    "Confirmación de asistencia",
    "Lista de confirmados en vivo",
    "Cuenta regresiva",
    "Código de vestimenta",
    "Hospedaje con liga para reservar",
    "Mesa de regalos",
    "Galería de fotos",
]

# Ni precio ni liga: este anuncio abre conversación, no cierra venta.
# En dos renglones a propósito: en una sola línea no cabe a este cuerpo y el
# navegador la parte donde quiere, dejando «SEMANAS» solo abajo.
CIERRE = "Dos rondas de ajustes incluidas<br>Lista en dos semanas"
CTA = "Escríbenos «boda» por DM"


def css(alto):
    return f"""
{FONTS}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:{ANCHO}px;height:{alto}px;overflow:hidden}}
body{{background:{OSCURO};color:{TINTA};-webkit-font-smoothing:antialiased}}
.s{{position:relative;width:{ANCHO}px;height:{alto}px;overflow:hidden}}
.kick{{font-family:UI;font-weight:500;letter-spacing:.20em;text-transform:uppercase}}
.tit{{font-family:Playfair;font-weight:400;line-height:1.06;color:{TINTA}}}
.cuerpo{{font-family:Serif;font-weight:400;line-height:1.42;color:{SUAVE}}}
.iso{{background:url({ISO}) center/contain no-repeat}}
.fil{{height:18px;background:url({FIL}) left/contain no-repeat}}
.sombra{{text-shadow:0 1px 14px rgba(251,249,246,.85)}}
.tarjeta{{position:absolute;background:{PAPEL};display:flex;flex-direction:column;
  box-shadow:0 -14px 60px rgba(18,15,12,.20)}}
.item{{display:flex;align-items:baseline;font-family:UI;font-weight:400;color:{TINTA}}}
.item .p{{flex:0 0 auto;color:{ACENTO}}}
.pill{{display:flex;align-items:center;justify-content:center;
  font-family:UI;font-weight:500;text-transform:uppercase;letter-spacing:.14em;
  color:{PAPEL};background:{ACENTO}}}
"""


def cabecera_velo(alto, m):
    """Velo de papel, no de tinta, y solo en la cabecera.

    La foto es papelería sobre lino blanco: clarísima. Meterle un velo oscuro
    para poder poner texto claro encima la ensucia y la apaga justo donde más
    bonita está. Se hace al revés —se aclara un poco la cabecera y el rótulo va
    en tinta— y la foto se queda como es.
    """
    # Solo hasta donde empieza la tarjeta: más abajo la tarjeta ya tapa, y
    # aclarar de más deja la foto lavada sin ganar nada.
    banda = alto - m["tarjeta"] - m["marco"] + 40
    return (f'<div style="position:absolute;left:0;right:0;top:0;height:{banda}px;'
            f'background:linear-gradient(180deg,rgba(251,249,246,.94),'
            f'rgba(251,249,246,.62) 62%,rgba(251,249,246,0))"></div>')


def lista(tam, hueco):
    """Una prestación por renglón. En una sola columna: dos columnas obligan a
    partir las etiquetas largas en dos renglones y la lista deja de leerse de
    un vistazo, que es lo único que tiene que hacer."""
    return "".join(
        f'<div class="item" style="font-size:{tam}px;line-height:1.25;margin-bottom:{hueco}px">'
        f'<span class="p" style="margin-right:20px">·</span><span>{t}</span></div>'
        for t in INCLUYE)


def pieza(alto, m):
    """Foto de fondo a sangre, y la lista sobre una tarjeta de papel.

    La lista lleva nueve renglones: encima de una foto, aunque se le meta velo,
    nueve renglones se leen mal y se ven sucios. Sobre papel el contraste es
    11.95:1 sin discusión y la foto se queda entera arriba, que es donde
    trabaja.
    """
    return (
        f'<div class="s">'
        f'<div style="position:absolute;inset:0;background:url({FOTO[LA_FOTO]}) '
        f'{m["pos"]}/{m["zoom"]};{TRATO["calido"]}"></div>'
        + cabecera_velo(alto, m)
        + f'<div class="cont" style="position:absolute;left:0;right:0;top:0;padding:{m["pad"]}px;'
          f'display:flex;justify-content:space-between;align-items:flex-start">'
          f'<div class="kick sombra" style="font-size:{m["kick"]}px;color:{ACENTO};'
          f'max-width:620px;line-height:1.5">Páginas web de boda<br>hechas a mano</div>'
          f'<div class="iso" style="width:{m["iso"]}px;height:{m["iso"]}px;flex:0 0 auto"></div>'
          f'</div>'
        + f'<div class="tarjeta cont" style="height:{m["tarjeta"]}px;padding:{m["pad"]}px;'
          f'left:{m["marco"]}px;right:{m["marco"]}px;bottom:{m["marco"]}px">'
          # Sin textura. El lino es un SVG que se estira al alto de la tarjeta
          # y sale convertido en rayas verticales; el relieve es una foto de
          # papel repujado que a este tamaño trae su propia costura por el
          # medio. Papel liso y ya: lo que tiene que verse es la lista.

          f'<div id="dentro" style="position:relative">'
          f'<div class="tit" style="font-size:{m["tit"]}px">'
          f'Hacemos la página<br>de su boda.</div>'
          f'<div style="height:{m["h1"]}px"></div>'
          f'<div class="cuerpo" style="font-size:{m["lead"]}px;max-width:{m["leadw"]}px">'
          f'Una sola dirección con todo lo que sus invitados van a preguntar.</div>'
          f'<div style="height:{m["h2"]}px"></div>'
          f'<div class="fil" style="width:{m["fil"]}px"></div>'
          f'<div style="height:{m["h2"]}px"></div>'
          + lista(m["item"], m["hueco"]) +
          f'<div style="height:{m["h3"]}px"></div>'
          f'<div class="kick" style="font-size:{m["pie"]}px;letter-spacing:.14em;'
          f'color:{ACENTO}">{CIERRE}</div>'
          f'<div style="height:{m["h4"]}px"></div>'
          f'<div class="pill" style="font-size:{m["cta"]}px;padding:{m["ctay"]}px 0">'
          f'{CTA}</div>'
          f'</div>'
          f'</div>'
        f'</div>'
    )


# La tarjeta se lleva la mayor parte del 4:5 porque son nueve renglones y no
# hay forma de que quepan en menos. En el 9:16 sobra alto y la foto respira.
TAMANOS = {
    "feed-4x5": dict(
        alto=1350, pos="center 45%", zoom="130%", marco=44,
        pad=56, kick=32, iso=74, tarjeta=1060,
        tit=60, h1=14, lead=34, leadw=780, h2=18, fil=190,
        item=32, hueco=9, h3=20, pie=32, h4=18, cta=32, ctay=24),
    "historia-9x16": dict(
        alto=1920, pos="center 45%", zoom="130%", marco=52,
        pad=76, kick=34, iso=94, tarjeta=1410,
        tit=80, h1=24, lead=42, leadw=840, h2=30, fil=250,
        item=40, hueco=17, h3=32, pie=34, h4=28, cta=38, ctay=32),
}


def cabe(html, alto):
    """¿Cabe todo dentro de la tarjeta?

    Ajustar tamaños a ojo y luego mirar el JPEG es justo como se cuela un
    renglón cortado. Se mide en el navegador: el contenido de la tarjeta contra
    el hueco que tiene. Devuelve (sobra_o_falta, alto_del_contenido).
    """
    doc = (f"<html><head><meta charset='utf-8'><style>{css(alto)}</style></head>"
           f"<body>{html}</body></html>")
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pag = nav.new_page(viewport={"width": ANCHO, "height": alto}, device_scale_factor=1)
        pag.set_content(doc)
        pag.wait_for_timeout(1000)
        r = pag.evaluate("""() => {
            const t = document.querySelector('.tarjeta');
            const d = document.getElementById('dentro');
            const pad = parseFloat(getComputedStyle(t).paddingTop);
            return {hueco: t.clientHeight - pad * 2, contenido: d.getBoundingClientRect().height};
        }""")
        nav.close()
    return round(r["hueco"] - r["contenido"]), round(r["contenido"])


def revisar_fuentes(html):
    return sorted({int(x) for x in re.findall(r"font-size:(\d+)px", html) if int(x) < 32})


def contraste(html, alto):
    """Contraste real del rótulo contra la foto que tiene debajo.

    Dos pasadas sobre la misma pieza. En la primera se mide dónde cae de verdad
    el rótulo, preguntándoselo al navegador en vez de estimarlo: estimar la
    banda a ojo fue justo lo que hizo que la medición saliera mal, porque
    incluía hojas oscuras que están muy por debajo del texto. En la segunda se
    esconde el contenido y se fotografía el fondo, y se busca el pixel más
    oscuro de ese rectángulo exacto: el rótulo va en tinta, así que el caso
    malo es donde el fondo se oscurece.
    """
    from PIL import Image

    def luz(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    def lum(px):
        return 0.2126 * luz(px[0]) + 0.7152 * luz(px[1]) + 0.0722 * luz(px[2])

    tmp = pathlib.Path("/tmp/anuncio-fondo.png")
    base_doc = f"<html><head><meta charset='utf-8'><style>{css(alto)}</style>"
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pag = nav.new_page(viewport={"width": ANCHO, "height": alto}, device_scale_factor=1)
        pag.set_content(base_doc + f"</head><body>{html}</body></html>")
        pag.wait_for_timeout(900)
        caja = pag.evaluate("""() => {
            const k = document.querySelector('.kick.sombra');
            const r = k.getBoundingClientRect();
            return [r.left, r.top, r.right, r.bottom];
        }""")
        pag.set_content(base_doc + "<style>.cont{display:none!important}</style>"
                        f"</head><body>{html}</body></html>")
        pag.wait_for_timeout(900)
        pag.query_selector(".s").screenshot(path=str(tmp))
        nav.close()
    im = Image.open(tmp).convert("RGB")
    x0, y0, x1, y1 = (int(v) for v in caja)
    recorte = im.crop((x0, y0, x1, y1)).resize((240, 300))
    vals = sorted(lum(px) for px in recorte.getdata())
    # El rótulo va en tinta sobre una foto clara, así que el caso malo no es el
    # pixel más brillante sino el más oscuro: es donde la tinta se pierde.
    peor = vals[int(len(vals) * 0.01)]
    L = lum((90, 70, 54))          # ACENTO #5A4636
    return round((max(L, peor) + 0.05) / (min(L, peor) + 0.05), 2)


def main():
    SALIDA.mkdir(parents=True, exist_ok=True)
    for nombre, m in TAMANOS.items():
        alto = m["alto"]
        html = pieza(alto, m)

        malos = revisar_fuentes(html)
        if malos:
            raise SystemExit(f"{nombre}: fuentes por debajo de 32 px: {malos}")

        sobra, contenido = cabe(html, alto)
        if sobra < 0:
            raise SystemExit(f"{nombre}: el contenido no cabe en la tarjeta; se sale "
                             f"{-sobra} px (mide {contenido}). Sube «tarjeta» o baja tamaños.")

        # Lo único que va sobre la foto es la cabecera: rótulo e isotipo. Se
        # mide justo esa banda. El resto vive sobre papel y ahí el contraste ya
        # está verificado en la paleta (tinta sobre papel, 11.95:1).
        razon = contraste(html, alto)
        if razon < 4.5:
            raise SystemExit(f"{nombre}: la cabecera no se lee sobre la foto ({razon})")

        doc = (f"<html><head><meta charset='utf-8'><style>{css(alto)}</style></head>"
               f"<body>{html}</body></html>")
        ruta = SALIDA / f"anuncio-{nombre}.jpg"
        with sync_playwright() as p:
            nav = p.chromium.launch()
            pag = nav.new_page(viewport={"width": ANCHO, "height": alto}, device_scale_factor=1)
            pag.set_content(doc)
            pag.wait_for_timeout(1200)
            pag.query_selector(".s").screenshot(path=str(ruta), type="jpeg", quality=92)
            nav.close()
        kb = ruta.stat().st_size // 1024
        print(f"{ruta.name:30} {ANCHO}×{alto}  {kb} KB  "
              f"contraste cabecera {razon}  holgura {sobra} px")


if __name__ == "__main__":
    main()
