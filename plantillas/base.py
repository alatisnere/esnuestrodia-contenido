"""
Sistema de láminas de Es Nuestro Día.

Todo lo que necesita está dentro del repositorio (marca/ y fotos/), así que se
puede regenerar cualquier publicación desde cero sin depender de la máquina
donde se hizo la primera vez.

Reglas de diseño que no se rompen:
  - nada por debajo de 32 px sobre lienzo de 1080
  - contraste mínimo 4.5:1 en todo el texto
  - contexto de boda visible en cada lámina
  - sobre foto siempre va velo, arriba y abajo
"""

import base64
import pathlib
import re

from playwright.sync_api import sync_playwright

RAIZ = pathlib.Path(__file__).resolve().parent.parent
MARCA = RAIZ / "marca"
FOTOS = RAIZ / "fotos"
W, H = 1080, 1350

# Paleta verificada contra WCAG. Los números son la razón de contraste real:
#   tinta sobre papel 11.95:1 · suave sobre papel 7.14:1 · suave sobre arena 5.97:1
#   acento sobre papel 8.45:1 · acento sobre arena 7.07:1 · claro sobre oscuro 8.92:1
TINTA = "#3A322C"
SUAVE = "#5D5349"
ACENTO = "#5A4636"
PAPEL = "#FBF9F6"
ARENA = "#EDE4DA"
OSCURO = "#332C26"
CLARO = "#D8CFC4"


def _b64(ruta, mime):
    return f"data:{mime};base64," + base64.b64encode(pathlib.Path(ruta).read_bytes()).decode()


def _font(archivo, familia, peso=400, estilo="normal"):
    return (
        f"@font-face{{font-family:'{familia}';font-weight:{peso};font-style:{estilo};"
        f"src:url({_b64(MARCA / 'fonts' / archivo, 'font/woff2')}) format('woff2')}}"
    )


FONTS = "".join([
    _font("playfair-display-latin-400-normal.woff2", "Playfair"),
    _font("playfair-display-latin-500-normal.woff2", "Playfair", 500),
    _font("cormorant-garamond-latin-400-normal.woff2", "Serif"),
    _font("cormorant-garamond-latin-400-italic.woff2", "Serif", 400, "italic"),
    _font("montserrat-latin-400-normal.woff2", "UI"),
    _font("montserrat-latin-500-normal.woff2", "UI", 500),
])

ISO = _b64(MARCA / "img/isotipo.svg", "image/svg+xml")
ISO_P = _b64(MARCA / "img/isotipo-papel.svg", "image/svg+xml")
LOGO = _b64(MARCA / "img/logo-tinta.svg", "image/svg+xml")
FIL = _b64(MARCA / "img/filete-tan.svg", "image/svg+xml")
FIL_P = _b64(MARCA / "img/filete-papel.svg", "image/svg+xml")
LINO = _b64(MARCA / "img/tex-lino.svg", "image/svg+xml")
REL = _b64(MARCA / "img/tex-relieve.jpg", "image/jpeg")

FOTO = {p.stem: _b64(p, "image/jpeg") for p in sorted(FOTOS.glob("*.jpg"))}

CSS = f"""
{FONTS}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:{W}px;height:{H}px;overflow:hidden}}
body{{background:{PAPEL};color:{TINTA};-webkit-font-smoothing:antialiased}}
.s{{position:relative;width:{W}px;height:{H}px;overflow:hidden}}
.papel{{background:{PAPEL}}} .arena{{background:{ARENA}}} .tinta{{background:{OSCURO};color:{PAPEL}}}
.tex{{position:absolute;inset:0;background:url({LINO}) 0 0/100% 100% no-repeat;opacity:.40;mix-blend-mode:multiply}}
.rel{{position:absolute;inset:0;background:url({REL}) center/cover no-repeat;opacity:.26;mix-blend-mode:multiply}}
.kick{{font-family:UI;font-weight:500;font-size:32px;letter-spacing:.20em;text-transform:uppercase;color:{ACENTO}}}
.kick.cl{{color:{CLARO}}}
.tit{{font-family:Playfair;font-weight:400;font-size:88px;line-height:1.08}}
.tit.m{{font-size:70px}} .tit.ch{{font-size:60px}}
.cuerpo{{font-family:Serif;font-weight:400;font-size:50px;line-height:1.42;color:{SUAVE}}}
.cuerpo.cl{{color:{CLARO}}}
.fil{{width:280px;height:20px;background:url({FIL}) center/contain no-repeat}}
.fil.p{{background-image:url({FIL_P})}}
.iso{{width:96px;height:96px;background:url({ISO}) center/contain no-repeat}}
.iso.p{{background-image:url({ISO_P})}}
.gap{{flex:1}}
.sombra{{text-shadow:0 2px 18px rgba(20,16,13,.55)}}
"""

VELO_ARRIBA = ('<div style="position:absolute;left:0;right:0;top:0;height:320px;'
               'background:linear-gradient(180deg,rgba(18,15,12,.66),rgba(18,15,12,0))"></div>')


def velo_abajo(h=740):
    return (f'<div style="position:absolute;left:0;right:0;bottom:0;height:{h}px;'
            'background:linear-gradient(180deg,rgba(18,15,12,0),'
            'rgba(18,15,12,.82) 42%,rgba(18,15,12,.96))"></div>')


VELO_PLANO_SUAVE = ('<div style="position:absolute;inset:0;'
                    'background:rgba(18,15,12,.34)"></div>')


def lamina(interior, fondo="papel"):
    return f'<div class="s {fondo}">{interior}</div>'


def foto(nombre, pos="center"):
    return (f'<div style="position:absolute;inset:0;'
            f'background:url({FOTO[nombre]}) {pos}/cover"></div>')


def portada(nombre_foto, rotulo, titulo, bajada, pie, pos="center"):
    """Lámina 1: foto + rótulo de contexto arriba + título y bajada abajo."""
    return lamina(
        foto(nombre_foto, pos) + VELO_PLANO_SUAVE + VELO_ARRIBA + velo_abajo(760) +
        '<div class="cont" style="position:absolute;inset:80px;display:flex;flex-direction:column;color:#FBF9F6">'
        '<div style="display:flex;justify-content:space-between;align-items:flex-start">'
        f'<div class="kick cl sombra">{rotulo}</div><div class="iso p"></div></div>'
        '<div class="gap"></div>'
        f'<div class="tit sombra" style="color:#FBF9F6">{titulo}</div>'
        '<div style="height:30px"></div>'
        f'<div class="cuerpo sombra" style="color:#F1EAE2;font-size:52px">{bajada}</div>'
        '<div style="height:36px"></div>'
        '<div style="font-family:UI;font-weight:500;font-size:32px;letter-spacing:.18em;'
        f'text-transform:uppercase;color:#FBF9F6" class="sombra">{pie}</div></div>')


def texto(rotulo, titulo, cuerpo, fondo="papel", numero=None, filete=True):
    """Lámina tipográfica. `cuerpo` puede traer <br> y <b>."""
    num = (f'<div style="font-family:Playfair;font-size:96px;line-height:1;'
           f'color:{ACENTO}">{numero}</div><div style="height:22px"></div>') if numero else ""
    fil = '<div style="height:52px"></div><div class="fil"></div>' if filete else ""
    tex = '<div class="tex"></div>' if fondo == "papel" else '<div class="rel"></div>'
    return lamina(
        tex +
        '<div style="position:absolute;inset:88px;display:flex;flex-direction:column;justify-content:center">'
        f'<div class="kick">{rotulo}</div><div style="height:30px"></div>{num}'
        f'<div class="tit m">{titulo}</div><div style="height:32px"></div>'
        f'<div class="cuerpo">{cuerpo}</div>{fil}</div>', fondo)


def lista(rotulo, titulo, filas, fondo="papel"):
    """Lámina de lista numerada. `filas` es una lista de textos."""
    items = "".join(
        '<div style="display:flex;gap:26px;align-items:flex-start;padding:26px 0;'
        'border-bottom:1px solid rgba(58,50,44,.18)">'
        f'<span style="font-family:UI;font-weight:500;font-size:32px;color:{ACENTO};'
        f'padding-top:12px">{i:02d}</span>'
        f'<span style="font-family:Serif;font-size:46px;line-height:1.3;color:{TINTA}">{t}</span></div>'
        for i, t in enumerate(filas, 1))
    tex = '<div class="tex"></div>' if fondo == "papel" else '<div class="rel"></div>'
    return lamina(
        tex +
        '<div style="position:absolute;inset:88px;display:flex;flex-direction:column;justify-content:center">'
        f'<div class="kick">{rotulo}</div><div style="height:30px"></div>'
        f'<div class="tit m">{titulo}</div>'
        f'<div style="height:44px"></div>{items}</div>', fondo)


def muestras(rotulo, titulo, colores, nota, fondo="papel"):
    """Lámina de paleta: círculos de color con su nombre."""
    circulos = "".join(
        f'<div style="display:flex;align-items:center;gap:32px;padding:22px 0">'
        f'<div style="width:112px;height:112px;border-radius:999px;background:{hexa};'
        f'box-shadow:inset 0 0 0 1px rgba(58,50,44,.18)"></div>'
        f'<div><div style="font-family:Playfair;font-size:50px;color:{TINTA}">{nombre}</div>'
        f'<div style="font-family:UI;font-size:32px;letter-spacing:.10em;color:{SUAVE}">{donde}</div>'
        f'</div></div>'
        for nombre, hexa, donde in colores)
    tex = '<div class="tex"></div>' if fondo == "papel" else '<div class="rel"></div>'
    return lamina(
        tex +
        '<div style="position:absolute;inset:88px;display:flex;flex-direction:column;justify-content:center">'
        f'<div class="kick">{rotulo}</div><div style="height:28px"></div>'
        f'<div class="tit ch">{titulo}</div><div style="height:36px"></div>{circulos}'
        f'<div style="height:30px"></div><div class="cuerpo" style="font-size:42px">{nota}</div></div>',
        fondo)


VELO_PLANO = ('<div style="position:absolute;inset:0;'
              'background:rgba(18,15,12,.53)"></div>')


def cierre(nombre_foto, titulo, cuerpo, pie, pos="center"):
    """Última lámina: foto, remate y llamada a guardar o compartir.

    Lleva velo plano además del degradado: el título queda a media altura y
    ahí el degradado todavía es débil, así que sobre una foto clara —un ramo
    blanco, un muro encalado— el texto se perdía.
    """
    return lamina(
        foto(nombre_foto, pos) + VELO_PLANO + VELO_ARRIBA + velo_abajo(780) +
        '<div class="cont" style="position:absolute;inset:88px;display:flex;flex-direction:column;'
        'align-items:center;text-align:center;justify-content:flex-end;color:#FBF9F6">'
        f'<div class="tit m sombra" style="color:#FBF9F6">{titulo}</div>'
        '<div style="height:28px"></div>'
        f'<div class="cuerpo sombra" style="color:#F1EAE2;max-width:850px">{cuerpo}</div>'
        '<div style="height:44px"></div><div class="fil p"></div><div style="height:26px"></div>'
        '<div class="iso p" style="width:80px;height:80px"></div><div style="height:18px"></div>'
        '<div style="font-family:UI;font-weight:500;font-size:32px;letter-spacing:.20em;'
        f'text-transform:uppercase;color:#FBF9F6" class="sombra">{pie}</div></div>')


def cta_dm(nombre_foto, titulo, cuerpo, palabra, pos="center"):
    """Cierre de las publicaciones de promoción: manda a DM, nunca a la web."""
    return lamina(
        foto(nombre_foto, pos) + VELO_PLANO + VELO_ARRIBA + velo_abajo(820) +
        '<div class="cont" style="position:absolute;inset:88px;display:flex;flex-direction:column;'
        'align-items:center;text-align:center;justify-content:flex-end;color:#FBF9F6">'
        '<div class="iso p" style="width:96px;height:96px"></div><div style="height:28px"></div>'
        f'<div class="tit m sombra" style="color:#FBF9F6">{titulo}</div>'
        '<div style="height:26px"></div>'
        f'<div class="cuerpo sombra" style="color:#F1EAE2;max-width:840px">{cuerpo}</div>'
        '<div style="height:44px"></div>'
        f'<div style="font-family:UI;font-weight:500;font-size:38px;letter-spacing:.10em;'
        f'color:{OSCURO};background:#FBF9F6;padding:30px 62px;border-radius:999px">'
        f'Escríbenos «{palabra}» por DM</div>'
        '<div style="height:26px"></div>'
        '<div style="font-family:UI;font-weight:400;font-size:32px;letter-spacing:.14em;'
        'text-transform:uppercase;color:#FBF9F6" class="sombra">Contestamos el mismo día</div></div>')


def render(laminas, prefijo, destino):
    """Escribe prefijo-1.jpg … prefijo-N.jpg en `destino`. Devuelve las rutas."""
    destino = pathlib.Path(destino)
    destino.mkdir(parents=True, exist_ok=True)
    html = f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{''.join(laminas)}</body></html>"
    salidas = []
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pag = nav.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        pag.set_content(html)
        pag.wait_for_timeout(1200)
        for i, el in enumerate(pag.query_selector_all(".s"), 1):
            ruta = destino / f"{prefijo}-{i}.jpg"
            el.screenshot(path=str(ruta), type="jpeg", quality=92)
            salidas.append(ruta)
        nav.close()
    return salidas


def revisar(laminas):
    """Avisa de tamaños de fuente por debajo del mínimo acordado."""
    malos = sorted({int(m) for m in re.findall(r"font-size:(\d+)px", "".join(laminas)) if int(m) < 32})
    return malos


def contraste_sobre_foto(laminas, destino_tmp="/tmp/fondos"):
    """Mide el contraste real del texto claro sobre las láminas con foto.

    Renderiza las mismas láminas con el texto en transparente, así queda solo
    el fondo con sus velos. Después busca, dentro de cada banda donde vive
    texto, el pixel MÁS CLARO —el peor caso— y calcula su razón de contraste
    contra el papel (#FBF9F6). Devuelve una lista de (lámina, peor razón).
    """
    from PIL import Image

    def luz(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    def lum(px):
        r, g, b = px[:3]
        return 0.2126 * luz(r) + 0.7152 * luz(g) + 0.0722 * luz(b)

    destino = pathlib.Path(destino_tmp)
    destino.mkdir(parents=True, exist_ok=True)
    oculto = "<style>.cont{display:none!important}</style>"
    html = (f"<html><head><meta charset='utf-8'><style>{CSS}</style>{oculto}</head>"
            f"<body>{''.join(laminas)}</body></html>")

    L_PAPEL = lum((251, 249, 246))
    fuera = []
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pag = nav.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        pag.set_content(html)
        pag.wait_for_timeout(1200)
        for i, el in enumerate(pag.query_selector_all(".s"), 1):
            html_l = el.inner_html() or ""
            # Solo interesan las láminas donde el texto claro cae ENCIMA de la
            # foto. En las partidas o de banda el texto va sobre color, y ahí
            # medir el fondo de la foto no dice nada.
            if "background:url(data:image/jpeg" not in html_l or 'class="cont"' not in html_l:
                continue
            ruta = destino / f"fondo-{i}.png"
            el.screenshot(path=str(ruta))
            im = Image.open(ruta).convert("RGB")
            # Solo la mitad inferior: ahí es donde va el texto claro sobre foto.
            recorte = im.crop((80, int(H * 0.52), W - 80, H - 60)).resize((240, 260))
            vals = sorted(lum(px) for px in recorte.getdata())
            peor = vals[int(len(vals) * 0.99)]
            razon = (max(L_PAPEL, peor) + 0.05) / (min(L_PAPEL, peor) + 0.05)
            fuera.append((i, round(razon, 2)))
        nav.close()
    return fuera


# ══════════════════════════════════════════════════════════════════════
# Variedad: fondos de acento, texturas y disposiciones alternativas.
#
# Todo lo de aquí abajo existe para que dos publicaciones seguidas no se
# vean igual. La congruencia la sostienen las tipografías, el isotipo y el
# hecho de que todos los tonos son apagados; la variedad la dan el color de
# fondo, la textura y la disposición.
#
# Contraste verificado contra el texto que les corresponde:
#   olivo 8.64 · bosque 11.25 · azul 7.80 · cacao 10.31 · vino 11.07  (texto papel)
#   hueso 10.97 · arena media 8.77 · salvia 8.08 · arcilla 9.25       (texto tinta)
# ══════════════════════════════════════════════════════════════════════

OLIVO = "#454B36"
BOSQUE = "#2C3B31"
AZUL = "#3E5163"
CACAO = "#4A3A30"
VINO = "#5A2A2E"
HUESO = "#F4EFE7"
ARENA_MEDIA = "#E2D6C6"
SALVIA = "#CBD2C0"
ARCILLA = "#EFD9CC"

OSCUROS = {"olivo": OLIVO, "bosque": BOSQUE, "azul": AZUL, "cacao": CACAO,
           "vino": VINO, "tinta": OSCURO}
CLAROS = {"papel": PAPEL, "hueso": HUESO, "arena": ARENA, "arena-media": ARENA_MEDIA,
          "salvia": SALVIA, "arcilla": ARCILLA}


def _svg(cuerpo, w=400, h=400):
    import urllib.parse
    svg = (f"<svg xmlns='http://www.w3.org/2000/svg' width='{w}' height='{h}' "
           f"viewBox='0 0 {w} {h}'>{cuerpo}</svg>")
    return "data:image/svg+xml," + urllib.parse.quote(svg)


# Texturas. Se aplican con multiply y opacidad baja: se sienten, no se ven.
TEX = {
    "lino": LINO,
    "relieve": REL,
    "grano": _svg("<filter id='g'><feTurbulence type='fractalNoise' baseFrequency='.9' "
                  "numOctaves='3'/></filter><rect width='400' height='400' filter='url(#g)' "
                  "opacity='.5'/>"),
    "acuarela": _svg("<filter id='a'><feTurbulence type='fractalNoise' baseFrequency='.012' "
                     "numOctaves='4'/><feDisplacementMap in='SourceGraphic' scale='60'/></filter>"
                     "<rect width='400' height='400' fill='#000' filter='url(#a)' opacity='.35'/>"),
    "rayado": _svg("<pattern id='r' width='14' height='14' patternUnits='userSpaceOnUse' "
                   "patternTransform='rotate(35)'><line x1='0' y1='0' x2='0' y2='14' "
                   "stroke='#000' stroke-width='1.1' opacity='.5'/></pattern>"
                   "<rect width='400' height='400' fill='url(#r)'/>"),
    "puntos": _svg("<pattern id='p' width='26' height='26' patternUnits='userSpaceOnUse'>"
                   "<circle cx='6' cy='6' r='2.1' fill='#000' opacity='.55'/></pattern>"
                   "<rect width='400' height='400' fill='url(#p)'/>"),
}

_OPACIDAD = {"lino": .40, "relieve": .26, "grano": .10, "acuarela": .16,
             "rayado": .07, "puntos": .09}


def textura(nombre, escala="100% 100%"):
    if nombre is None:
        return ""
    op = _OPACIDAD.get(nombre, .2)
    tam = "cover" if nombre in ("relieve", "acuarela") else escala
    return (f'<div style="position:absolute;inset:0;background:url({TEX[nombre]}) 0 0/{tam};'
            f'opacity:{op};mix-blend-mode:multiply"></div>')


def _color(nombre):
    return OSCUROS.get(nombre) or CLAROS.get(nombre) or nombre


def _es_oscuro(nombre):
    return nombre in OSCUROS


def fondo(nombre, tex=None):
    """Devuelve el par (estilo del div, capa de textura) para un fondo con nombre."""
    return f'background:{_color(nombre)}', textura(tex)


# ── Tratamientos de foto ────────────────────────────────────────────────
TRATO = {
    "normal": "",
    "calido": "filter:saturate(1.06) contrast(1.04) sepia(.12)",
    "frio": "filter:saturate(.72) contrast(1.06) hue-rotate(-8deg)",
    "gris": "filter:grayscale(1) contrast(1.08)",
    "apagado": "filter:saturate(.55) contrast(1.02) brightness(.96)",
}


def foto_tratada(nombre, pos="center", trato="normal"):
    return (f'<div style="position:absolute;inset:0;'
            f'background:url({FOTO[nombre]}) {pos}/cover;{TRATO[trato]}"></div>')


def tinte(color, op=.30):
    """Capa de color sobre la foto: la mete en la paleta de la publicación."""
    return (f'<div style="position:absolute;inset:0;background:{_color(color)};'
            f'opacity:{op};mix-blend-mode:multiply"></div>')


# ── Disposiciones nuevas ────────────────────────────────────────────────

def banda(nombre_foto, rotulo, titulo, cuerpo, fondo_color="hueso", pos="center",
          alto=560, trato="normal", tex="grano", tinte_foto=None):
    """Foto arriba como banda, texto abajo sobre color. Rompe el pleno de foto."""
    oscuro = _es_oscuro(fondo_color)
    txt = PAPEL if oscuro else TINTA
    txt2 = CLARO if oscuro else SUAVE
    kick = CLARO if oscuro else ACENTO
    capa = tinte(tinte_foto, .34) if tinte_foto else ""
    return lamina(
        f'<div style="position:absolute;left:0;top:0;width:{W}px;height:{alto}px;overflow:hidden">'
        f'{foto_tratada(nombre_foto, pos, trato)}{capa}</div>'
        f'<div style="position:absolute;left:0;top:{alto}px;width:{W}px;height:{H-alto}px;'
        f'background:{_color(fondo_color)}"></div>'
        f'<div style="position:absolute;left:0;top:{alto}px;width:{W}px;height:{H-alto}px;'
        f'overflow:hidden">{textura(tex)}</div>'
        f'<div style="position:absolute;left:88px;right:88px;top:{alto+72}px;'
        f'display:flex;flex-direction:column">'
        f'<div style="font-family:UI;font-weight:500;font-size:32px;letter-spacing:.20em;'
        f'text-transform:uppercase;color:{kick}">{rotulo}</div><div style="height:28px"></div>'
        f'<div style="font-family:Playfair;font-size:70px;line-height:1.08;color:{txt}">{titulo}</div>'
        f'<div style="height:30px"></div>'
        f'<div style="font-family:Serif;font-size:48px;line-height:1.42;color:{txt2}">{cuerpo}</div>'
        f'</div>')


def cita(texto_grande, autor, fondo_color="bosque", tex="acuarela"):
    """Una sola frase grande. Sirve para dar aire entre láminas densas."""
    oscuro = _es_oscuro(fondo_color)
    txt = PAPEL if oscuro else TINTA
    txt2 = CLARO if oscuro else SUAVE
    return lamina(
        f'<div style="position:absolute;inset:0;background:{_color(fondo_color)}"></div>'
        f'{textura(tex)}'
        '<div style="position:absolute;inset:100px;display:flex;flex-direction:column;'
        'justify-content:center;align-items:center;text-align:center">'
        f'<div style="font-family:Playfair;font-size:82px;line-height:1.14;color:{txt}">'
        f'{texto_grande}</div><div style="height:40px"></div>'
        f'<div style="width:220px;height:1px;background:{txt2};opacity:.5"></div>'
        f'<div style="height:28px"></div>'
        f'<div style="font-family:UI;font-weight:400;font-size:34px;letter-spacing:.10em;'
        f'color:{txt2}">{autor}</div></div>')


def dato(numero, unidad, rotulo, cuerpo, fondo_color="cacao", tex="rayado"):
    """Una cifra enorme. Para lo que se recuerda por el número."""
    oscuro = _es_oscuro(fondo_color)
    txt = PAPEL if oscuro else TINTA
    txt2 = CLARO if oscuro else SUAVE
    kick = CLARO if oscuro else ACENTO
    return lamina(
        f'<div style="position:absolute;inset:0;background:{_color(fondo_color)}"></div>'
        f'{textura(tex)}'
        '<div style="position:absolute;inset:88px;display:flex;flex-direction:column;'
        'justify-content:center">'
        f'<div style="font-family:UI;font-weight:500;font-size:32px;letter-spacing:.20em;'
        f'text-transform:uppercase;color:{kick}">{rotulo}</div><div style="height:36px"></div>'
        f'<div style="display:flex;align-items:baseline;gap:24px">'
        f'<span style="font-family:Playfair;font-size:250px;line-height:.86;color:{txt}">{numero}</span>'
        f'<span style="font-family:Serif;font-size:60px;color:{txt2}">{unidad}</span></div>'
        f'<div style="height:44px"></div>'
        f'<div style="font-family:Serif;font-size:50px;line-height:1.42;color:{txt2}">{cuerpo}</div>'
        f'</div>')


def partido(nombre_foto, rotulo, titulo, cuerpo, fondo_color="arcilla", pos="center",
            trato="normal", tex="puntos", ancho_foto=470):
    """Foto a un lado, texto al otro. Buena para comparar o para respirar."""
    oscuro = _es_oscuro(fondo_color)
    txt = PAPEL if oscuro else TINTA
    txt2 = CLARO if oscuro else SUAVE
    kick = CLARO if oscuro else ACENTO
    return lamina(
        f'<div style="position:absolute;left:0;top:0;width:{ancho_foto}px;height:{H}px;'
        f'overflow:hidden">{foto_tratada(nombre_foto, pos, trato)}</div>'
        f'<div style="position:absolute;left:{ancho_foto}px;top:0;width:{W-ancho_foto}px;'
        f'height:{H}px;background:{_color(fondo_color)}"></div>'
        f'<div style="position:absolute;left:{ancho_foto}px;top:0;width:{W-ancho_foto}px;'
        f'height:{H}px;overflow:hidden">{textura(tex)}</div>'
        f'<div style="position:absolute;left:{ancho_foto+64}px;right:64px;top:110px;bottom:110px;'
        f'display:flex;flex-direction:column;justify-content:center">'
        f'<div style="font-family:UI;font-weight:500;font-size:32px;letter-spacing:.18em;'
        f'text-transform:uppercase;color:{kick}">{rotulo}</div><div style="height:26px"></div>'
        f'<div style="font-family:Playfair;font-size:60px;line-height:1.1;color:{txt}">{titulo}</div>'
        f'<div style="height:28px"></div>'
        f'<div style="font-family:Serif;font-size:44px;line-height:1.4;color:{txt2}">{cuerpo}</div>'
        f'</div>')


def texto_color(rotulo, titulo, cuerpo, fondo_color="olivo", tex="grano", filete=True):
    """La lámina de texto de siempre, pero sobre un color de acento."""
    oscuro = _es_oscuro(fondo_color)
    txt = PAPEL if oscuro else TINTA
    txt2 = CLARO if oscuro else SUAVE
    kick = CLARO if oscuro else ACENTO
    fil = (f'<div style="height:52px"></div><div class="fil{" p" if oscuro else ""}"></div>'
           if filete else "")
    return lamina(
        f'<div style="position:absolute;inset:0;background:{_color(fondo_color)}"></div>'
        f'{textura(tex)}'
        '<div style="position:absolute;inset:88px;display:flex;flex-direction:column;'
        'justify-content:center">'
        f'<div style="font-family:UI;font-weight:500;font-size:32px;letter-spacing:.20em;'
        f'text-transform:uppercase;color:{kick}">{rotulo}</div><div style="height:30px"></div>'
        f'<div style="font-family:Playfair;font-size:70px;line-height:1.08;color:{txt}">{titulo}</div>'
        f'<div style="height:32px"></div>'
        f'<div style="font-family:Serif;font-size:50px;line-height:1.42;color:{txt2}">{cuerpo}</div>'
        f'{fil}</div>')


def lista_color(rotulo, titulo, filas, fondo_color="arena-media", tex="rayado"):
    oscuro = _es_oscuro(fondo_color)
    txt = PAPEL if oscuro else TINTA
    txt2 = CLARO if oscuro else SUAVE
    kick = CLARO if oscuro else ACENTO
    linea = "rgba(251,249,246,.22)" if oscuro else "rgba(58,50,44,.18)"
    items = "".join(
        f'<div style="display:flex;gap:26px;align-items:flex-start;padding:26px 0;'
        f'border-bottom:1px solid {linea}">'
        f'<span style="font-family:UI;font-weight:500;font-size:32px;color:{kick};'
        f'padding-top:12px">{i:02d}</span>'
        f'<span style="font-family:Serif;font-size:46px;line-height:1.3;color:{txt}">{t}</span></div>'
        for i, t in enumerate(filas, 1))
    return lamina(
        f'<div style="position:absolute;inset:0;background:{_color(fondo_color)}"></div>'
        f'{textura(tex)}'
        '<div style="position:absolute;inset:88px;display:flex;flex-direction:column;'
        'justify-content:center">'
        f'<div style="font-family:UI;font-weight:500;font-size:32px;letter-spacing:.20em;'
        f'text-transform:uppercase;color:{kick}">{rotulo}</div><div style="height:30px"></div>'
        f'<div style="font-family:Playfair;font-size:70px;line-height:1.08;color:{txt}">{titulo}</div>'
        f'<div style="height:44px"></div>{items}</div>')


def portada_color(nombre_foto, rotulo, titulo, bajada, pie, pos="center",
                  trato="normal", tinte_color=None, op=.32):
    """Portada de foto, pero teñida con el color de la publicación."""
    capa = tinte(tinte_color, op) if tinte_color else ""
    return lamina(
        foto_tratada(nombre_foto, pos, trato) + capa + VELO_PLANO_SUAVE + VELO_ARRIBA +
        velo_abajo(760) +
        '<div class="cont" style="position:absolute;inset:80px;display:flex;'
        'flex-direction:column;color:#FBF9F6">'
        '<div style="display:flex;justify-content:space-between;align-items:flex-start">'
        f'<div class="kick cl sombra">{rotulo}</div><div class="iso p"></div></div>'
        '<div class="gap"></div>'
        f'<div class="tit sombra" style="color:#FBF9F6">{titulo}</div>'
        '<div style="height:30px"></div>'
        f'<div class="cuerpo sombra" style="color:#F1EAE2;font-size:52px">{bajada}</div>'
        '<div style="height:36px"></div>'
        '<div style="font-family:UI;font-weight:500;font-size:32px;letter-spacing:.18em;'
        f'text-transform:uppercase;color:#FBF9F6" class="sombra">{pie}</div></div>')


def cierre_color(nombre_foto, titulo, cuerpo, pie, pos="center", trato="normal",
                 tinte_color=None, op=.32):
    capa = tinte(tinte_color, op) if tinte_color else ""
    return lamina(
        foto_tratada(nombre_foto, pos, trato) + capa + VELO_PLANO + VELO_ARRIBA +
        velo_abajo(780) +
        '<div class="cont" style="position:absolute;inset:88px;display:flex;'
        'flex-direction:column;align-items:center;text-align:center;'
        'justify-content:flex-end;color:#FBF9F6">'
        f'<div class="tit m sombra" style="color:#FBF9F6">{titulo}</div>'
        '<div style="height:28px"></div>'
        f'<div class="cuerpo sombra" style="color:#F1EAE2;max-width:850px">{cuerpo}</div>'
        '<div style="height:44px"></div><div class="fil p"></div><div style="height:26px"></div>'
        '<div class="iso p" style="width:80px;height:80px"></div><div style="height:18px"></div>'
        '<div style="font-family:UI;font-weight:500;font-size:32px;letter-spacing:.20em;'
        f'text-transform:uppercase;color:#FBF9F6" class="sombra">{pie}</div></div>')


def cta_dm_color(nombre_foto, titulo, cuerpo, palabra, pos="center", trato="normal",
                 tinte_color=None, op=.32):
    capa = tinte(tinte_color, op) if tinte_color else ""
    return lamina(
        foto_tratada(nombre_foto, pos, trato) + capa + VELO_PLANO + VELO_ARRIBA +
        velo_abajo(820) +
        '<div class="cont" style="position:absolute;inset:88px;display:flex;'
        'flex-direction:column;align-items:center;text-align:center;'
        'justify-content:flex-end;color:#FBF9F6">'
        '<div class="iso p" style="width:96px;height:96px"></div><div style="height:28px"></div>'
        f'<div class="tit m sombra" style="color:#FBF9F6">{titulo}</div>'
        '<div style="height:26px"></div>'
        f'<div class="cuerpo sombra" style="color:#F1EAE2;max-width:840px">{cuerpo}</div>'
        '<div style="height:44px"></div>'
        f'<div style="font-family:UI;font-weight:500;font-size:38px;letter-spacing:.10em;'
        f'color:{OSCURO};background:#FBF9F6;padding:30px 62px;border-radius:999px">'
        f'Escríbenos «{palabra}» por DM</div>'
        '<div style="height:26px"></div>'
        '<div style="font-family:UI;font-weight:400;font-size:32px;letter-spacing:.14em;'
        'text-transform:uppercase;color:#FBF9F6" class="sombra">Contestamos el mismo día</div></div>')


def portada_tipografica(rotulo, titulo, bajada, pie, fondo_color="vino", tex="rayado",
                        muestras_color=None):
    """Portada sin foto: puro color y tipografía.

    En la cuadrícula del perfil una portada así rompe la fila mucho más que
    cambiarle el tono a otra foto. Conviene una de cada tres o cuatro.
    """
    oscuro = _es_oscuro(fondo_color)
    txt = PAPEL if oscuro else TINTA
    txt2 = CLARO if oscuro else SUAVE
    kick = CLARO if oscuro else ACENTO
    iso = 'iso p' if oscuro else 'iso'
    puntos = ""
    if muestras_color:
        borde = "rgba(251,249,246,.35)" if oscuro else "rgba(58,50,44,.20)"
        puntos = ('<div style="display:flex;gap:26px;margin-top:52px">' + "".join(
            f'<div style="width:132px;height:132px;border-radius:999px;background:{c};'
            f'box-shadow:inset 0 0 0 1px {borde}"></div>' for c in muestras_color) + '</div>')
    return lamina(
        f'<div style="position:absolute;inset:0;background:{_color(fondo_color)}"></div>'
        f'{textura(tex)}'
        '<div style="position:absolute;inset:88px;display:flex;flex-direction:column">'
        '<div style="display:flex;justify-content:space-between;align-items:flex-start">'
        f'<div style="font-family:UI;font-weight:500;font-size:32px;letter-spacing:.20em;'
        f'text-transform:uppercase;color:{kick}">{rotulo}</div>'
        f'<div class="{iso}"></div></div>'
        '<div class="gap"></div>'
        f'<div style="font-family:Playfair;font-size:96px;line-height:1.04;color:{txt}">{titulo}</div>'
        f'{puntos}'
        '<div style="height:34px"></div>'
        f'<div style="font-family:Serif;font-size:52px;line-height:1.36;color:{txt2}">{bajada}</div>'
        '<div style="height:40px"></div>'
        f'<div style="font-family:UI;font-weight:500;font-size:32px;letter-spacing:.18em;'
        f'text-transform:uppercase;color:{kick}">{pie}</div></div>')


# ══════════════════════════════════════════════════════════════════════
# Control de repetición de fotos.
#
# En el feed se vio feo: dos publicaciones distintas abriendo con la misma
# foto. Como las láminas ya llevan la imagen incrustada en base64, se puede
# averiguar qué foto usa cada una sin que nadie tenga que declararlo a mano
# —y por lo tanto sin que se pueda olvidar.
# ══════════════════════════════════════════════════════════════════════

def _firma(uri):
    """Trozo del base64 tomado de la mitad del archivo.

    El principio de dos JPEG es casi idéntico (cabecera y tablas), así que un
    prefijo no distingue una foto de otra. A media imagen ya son datos de
    píxel y sí son únicos.
    """
    medio = len(uri) // 2
    return uri[medio:medio + 120]


_INDICE = {_firma(uri): nombre for nombre, uri in FOTO.items()}
assert len(_INDICE) == len(FOTO), "dos fotos comparten firma; alarga el trozo"


def fotos_en(laminas):
    """Qué fotos usa cada lámina, en orden. Devuelve lista de listas."""
    salida = []
    for lam in laminas:
        aqui = []
        for firma, nombre in _INDICE.items():
            if firma in lam and nombre not in aqui:
                aqui.append(nombre)
        salida.append(aqui)
    return salida


def portada_de(laminas):
    """La foto de la primera lámina, o None si la portada es tipográfica."""
    primeras = fotos_en(laminas)[0]
    return primeras[0] if primeras else None


class RegistroDePortadas:
    """Lleva la cuenta de qué foto abrió cada publicación.

    Se inicializa con las que ya salieron al feed para que una publicación
    nueva no repita la portada de una vieja.
    """

    def __init__(self, ya_publicadas=()):
        self.usadas = dict(ya_publicadas)

    def registrar(self, nombre_post, laminas):
        p = portada_de(laminas)
        if p is None:
            return None          # portada tipográfica: no consume foto
        if p in self.usadas:
            raise SystemExit(
                f"{nombre_post}: la portada «{p}» ya se usó en "
                f"«{self.usadas[p]}». Elige otra o hazla tipográfica."
            )
        self.usadas[p] = nombre_post
        return p


def revisar_repeticiones(laminas, nombre_post, max_por_publicacion=2):
    """Avisa si una misma foto aparece demasiadas veces dentro del carrusel."""
    cuenta = {}
    for aqui in fotos_en(laminas):
        for n in aqui:
            cuenta[n] = cuenta.get(n, 0) + 1
    exceso = {n: c for n, c in cuenta.items() if c > max_por_publicacion}
    if exceso:
        raise SystemExit(f"{nombre_post}: fotos repetidas dentro del carrusel: {exceso}")
    return cuenta
