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
            if "background:url(data:image/jpeg" not in (el.inner_html() or ""):
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
