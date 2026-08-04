"""Instagram: presentación + valor + promoción (con contexto de boda en todas)."""
import base64, pathlib
from playwright.sync_api import sync_playwright

SITE=pathlib.Path("/root/site2"); DEMO=pathlib.Path("/root/demo/anayluis/invitations/static/invitations/images")
NEW=pathlib.Path("/root/ig2/fotos"); OUT=pathlib.Path("/mnt/user-data/outputs/ig"); OUT.mkdir(parents=True,exist_ok=True)
W,H=1080,1350

def b64(p,m): return f"data:{m};base64,"+base64.b64encode(pathlib.Path(p).read_bytes()).decode()
def font(f,fam,w=400,st="normal"):
    return (f"@font-face{{font-family:'{fam}';font-weight:{w};font-style:{st};"
            f"src:url({b64(SITE/'fonts'/f,'font/woff2')}) format('woff2')}}")
FONTS="".join([
 font("playfair-display-latin-400-normal.woff2","Playfair"),
 font("playfair-display-latin-500-normal.woff2","Playfair",500),
 font("cormorant-garamond-latin-400-normal.woff2","Serif"),
 font("cormorant-garamond-latin-400-italic.woff2","Serif",400,"italic"),
 font("montserrat-latin-400-normal.woff2","UI"),
 font("montserrat-latin-500-normal.woff2","UI",500),
])
ISO=b64(SITE/"img/isotipo.svg","image/svg+xml"); ISO_P=b64(SITE/"img/isotipo-papel.svg","image/svg+xml")
LOGO=b64(SITE/"img/logo-tinta.svg","image/svg+xml"); LOGO_P=b64(SITE/"img/logo-papel.svg","image/svg+xml")
FIL=b64(SITE/"img/filete-tan.svg","image/svg+xml"); FIL_P=b64(SITE/"img/filete-papel.svg","image/svg+xml")
LINO=b64(SITE/"img/tex-lino.svg","image/svg+xml"); REL=b64(SITE/"img/tex-relieve.jpg","image/jpeg")
F={"jardin":b64(NEW/"jardin-tropical.png","image/png"),
   "terraza":b64(NEW/"civil-terraza.png","image/png"),
   "cipres":b64(DEMO/"break/break_1.webp","image/webp"),
   "frentes":b64(DEMO/"break/break_2.webp","image/webp"),
   "arcos":b64(DEMO/"hero/hero_right.webp","image/webp"),
   "calle":b64(DEMO/"hero/hero_left.webp","image/webp")}

TINTA="#3A322C"; SUAVE="#5D5349"; ACENTO="#5A4636"; PAPEL="#FBF9F6"; ARENA="#EDE4DA"
OSCURO="#332C26"; CLARO="#D8CFC4"

CSS=f"""
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
.logo{{height:110px;background:url({LOGO}) center/contain no-repeat}}
.logo.p{{background-image:url({LOGO_P})}}
.gap{{flex:1}}
.sombra{{text-shadow:0 2px 18px rgba(20,16,13,.55)}}
"""
def sl(i,c="papel"): return f'<div class="s {c}">{i}</div>'
def foto(k,pos="center"): return f'<div style="position:absolute;inset:0;background:url({F[k]}) {pos}/cover"></div>'
VELO_ARRIBA=('<div style="position:absolute;left:0;right:0;top:0;height:320px;'
  'background:linear-gradient(180deg,rgba(18,15,12,.66),rgba(18,15,12,0))"></div>')
def velo_abajo(h=740):
    return (f'<div style="position:absolute;left:0;right:0;bottom:0;height:{h}px;'
      'background:linear-gradient(180deg,rgba(18,15,12,0),rgba(18,15,12,.82) 42%,rgba(18,15,12,.96))"></div>')
VELO_PLANO='<div style="position:absolute;inset:0;background:rgba(20,16,13,.70)"></div>'

# =================================================== 0. PRESENTACIÓN
I=[]
I.append(sl(
 f'<div style="position:absolute;left:0;top:0;width:{W}px;height:600px;'
 f'background:url({F["arcos"]}) center 33%/cover"></div>'
 f'<div style="position:absolute;left:0;top:520px;width:{W}px;height:120px;'
 f'background:linear-gradient(180deg,rgba(251,249,246,0),{PAPEL} 82%)"></div>'
 f'<div style="position:absolute;left:0;top:600px;width:{W}px;height:{H-600}px;background:{PAPEL}"></div>'
 f'<div class="tex" style="top:600px;height:{H-600}px"></div>'
 f'<div style="position:absolute;left:88px;right:88px;top:648px;display:flex;'
 f'flex-direction:column;align-items:center;text-align:center">'
 f'<div class="iso" style="width:104px;height:104px"></div><div style="height:26px"></div>'
 f'<div class="logo" style="width:600px;height:96px"></div><div style="height:26px"></div>'
 f'<div class="tit m" style="font-size:66px">Hacemos la página<br>web de tu boda</div><div style="height:24px"></div>'
 f'<div class="cuerpo" style="max-width:820px">Una sola dirección con todo lo que tus '
 f'invitados van a preguntar.</div>'
 f'<div style="height:32px"></div><div class="fil"></div></div>'))

QUE=[("Itinerario","A qué hora es cada cosa y dónde"),
     ("Confirmación","Tus invitados confirman ahí mismo"),
     ("Hospedaje","Los hoteles, con liga para reservar"),
     ("Mesa de regalos","A donde ustedes quieran mandarla"),
     ("Galería","Sus fotos, y las del día después")]
que="".join(
 f'<div style="display:flex;gap:28px;align-items:baseline;padding:24px 0;'
 f'border-bottom:1px solid rgba(58,50,44,.16)">'
 f'<span style="font-family:UI;font-weight:500;font-size:30px;color:{ACENTO};min-width:64px">0{i}</span>'
 f'<span><span style="font-family:Playfair;font-size:46px">{a}</span><br>'
 f'<span style="font-family:Serif;font-size:38px;color:{SUAVE}">{b}</span></span></div>'
 for i,(a,b) in enumerate(QUE,1))
I.append(sl('<div class="rel"></div>'
 '<div style="position:absolute;inset:88px;display:flex;flex-direction:column;justify-content:center">'
 '<div class="kick">Qué lleva la página</div><div style="height:28px"></div>'
 '<div class="tit ch">Todo lo que hoy<br>contestas por WhatsApp</div>'
 f'<div style="height:36px"></div>{que}</div>', "arena"))

I.append(sl('<div class="tex" style="opacity:.16"></div>'
 '<div style="position:absolute;inset:88px;display:flex;flex-direction:column;justify-content:center">'
 '<div class="kick cl">Cómo la hacemos</div><div style="height:36px"></div>'
 '<div class="tit m" style="color:#FBF9F6">A mano, con<br>ustedes dos.</div>'
 '<div style="height:34px"></div>'
 '<div class="cuerpo cl">No es una plantilla donde cambias la foto y el nombre. Nos '
 'sentamos con ustedes, elegimos qué secciones entran y cuáles no, y la armamos. '
 'Queda lista en dos semanas.</div></div>', "tinta"))

I.append(sl('<div class="tex"></div>'
 '<div style="position:absolute;inset:88px;display:flex;flex-direction:column;justify-content:center">'
 '<div class="kick">Qué vas a ver por aquí</div><div style="height:30px"></div>'
 '<div class="tit ch">Consejos de boda,<br>no solo publicidad</div>'
 '<div style="height:38px"></div>'
 '<div class="cuerpo">Dos publicaciones al día. Una con algo útil para organizar tu boda: '
 'proveedores, tiempos, errores que salen caros. Y otra donde te contamos lo que hacemos, '
 'por si te sirve.</div>'
 '<div style="height:44px"></div><div class="fil"></div></div>'))

I.append(sl(
 foto("calle","center 30%") + VELO_ARRIBA + velo_abajo(800) +
 '<div style="position:absolute;inset:88px;display:flex;flex-direction:column;'
 'align-items:center;text-align:center;justify-content:flex-end;color:#FBF9F6">'
 '<div class="iso p" style="width:104px;height:104px"></div><div style="height:30px"></div>'
 '<div class="tit m sombra" style="color:#FBF9F6">Mira una boda<br>de ejemplo</div>'
 '<div style="height:26px"></div>'
 '<div class="cuerpo sombra" style="color:#F1EAE2;max-width:840px">Una invitación completa '
 'y funcionando, para que veas de qué estamos hablando.</div>'
 '<div style="height:44px"></div>'
 f'<div style="font-family:UI;font-weight:500;font-size:38px;letter-spacing:.10em;'
 f'color:{OSCURO};background:#FBF9F6;padding:30px 62px;border-radius:999px">esnuestrodia.com</div>'
 '<div style="height:30px"></div>'
 '<div style="font-family:UI;font-weight:400;font-size:32px;letter-spacing:.14em;'
 'text-transform:uppercase;color:#FBF9F6" class="sombra">La liga está en el perfil</div></div>'))

# =================================================== 1. VALOR (con contexto en cada lámina)
V=[]
V.append(sl(
 foto("jardin","center 20%") + VELO_ARRIBA + velo_abajo(740) +
 '<div style="position:absolute;inset:80px;display:flex;flex-direction:column;color:#FBF9F6">'
 '<div style="display:flex;justify-content:space-between;align-items:flex-start">'
 '<div class="kick cl sombra">Organizando tu boda</div><div class="iso p"></div></div>'
 '<div class="gap"></div>'
 '<div class="tit sombra" style="color:#FBF9F6">¿Boda en jardín<br>en temporada<br>de lluvias?</div>'
 '<div style="height:30px"></div>'
 '<div class="cuerpo sombra" style="color:#F1EAE2;font-size:52px">Aparta el toldo desde ahora.</div>'
 '<div style="height:36px"></div>'
 '<div style="font-family:UI;font-weight:500;font-size:32px;letter-spacing:.18em;'
 'text-transform:uppercase;color:#FBF9F6" class="sombra">Desliza · 4 cosas que sí importan</div></div>'))

def ficha(num,tit,cuerpo,kick,cls="papel"):
    return sl(('<div class="tex"></div>' if cls=="papel" else '<div class="rel"></div>')+
      '<div style="position:absolute;inset:88px;display:flex;flex-direction:column;justify-content:center">'
      f'<div class="kick">{kick}</div><div style="height:30px"></div>'
      f'<div style="font-family:Playfair;font-size:96px;line-height:1;color:{ACENTO}">{num}</div>'
      '<div style="height:22px"></div>'
      f'<div class="tit m">{tit}</div><div style="height:32px"></div>'
      f'<div class="cuerpo">{cuerpo}</div>'
      '<div style="height:52px"></div><div class="fil"></div></div>', cls)

V.append(ficha("01","Llueve a la peor hora",
 "Si va a llover, casi siempre cae por la tarde. Justo cuando ya tienes a todos tus "
 "invitados sentados y acaban de servir el plato fuerte.","Boda en jardín"))
V.append(ficha("02","Y luego está el pasto",
 "Aunque pare la lluvia, el pasto se queda blando toda la noche. Los tacones se entierran "
 "y nadie se para a bailar. Pregunta si el toldo trae piso o si eso va aparte.",
 "Boda en jardín","arena"))

PREG=["¿El toldo va incluido o se cobra aparte?","¿Hasta qué día puedo decidir sin que me cobren?",
      "¿Caben todas las mesas y la pista debajo?","¿Trae piso, o el piso es otro proveedor?"]
preg="".join(
 f'<div style="display:flex;gap:26px;align-items:flex-start;padding:26px 0;'
 f'border-bottom:1px solid rgba(58,50,44,.18)">'
 f'<span style="font-family:UI;font-weight:500;font-size:30px;color:{ACENTO};padding-top:12px">0{i}</span>'
 f'<span style="font-family:Serif;font-size:46px;line-height:1.3;color:{TINTA}">{q}</span></div>'
 for i,q in enumerate(PREG,1))
V.append(sl('<div class="tex"></div>'
 '<div style="position:absolute;inset:88px;display:flex;flex-direction:column;justify-content:center">'
 '<div class="kick">Antes de firmar con el jardín</div><div style="height:30px"></div>'
 '<div class="tit m">Cuatro preguntas<br>para tu boda</div>'
 f'<div style="height:44px"></div>{preg}</div>'))

V.append(sl(
 foto("cipres","center 40%") + VELO_ARRIBA + velo_abajo(760) +
 '<div style="position:absolute;inset:88px;display:flex;flex-direction:column;'
 'align-items:center;text-align:center;justify-content:flex-end;color:#FBF9F6">'
 '<div class="tit m sombra" style="color:#FBF9F6">Apártalo aunque<br>no lo uses.</div>'
 '<div style="height:28px"></div>'
 '<div class="cuerpo sombra" style="color:#F1EAE2;max-width:850px">Buscarlo tres días antes '
 'de la boda cuesta el triple, y eso si todavía queda alguno libre en la zona.</div>'
 '<div style="height:44px"></div><div class="fil p"></div><div style="height:26px"></div>'
 '<div class="iso p" style="width:80px;height:80px"></div><div style="height:18px"></div>'
 '<div style="font-family:UI;font-weight:500;font-size:32px;letter-spacing:.20em;'
 'text-transform:uppercase;color:#FBF9F6" class="sombra">Guárdalo, se te va a olvidar</div></div>'))

# =================================================== 2. PROMOCIÓN (con contexto)
P=[]
P.append(sl(
 foto("terraza","center 28%") + VELO_ARRIBA + velo_abajo(780) +
 '<div style="position:absolute;inset:80px;display:flex;flex-direction:column;color:#FBF9F6">'
 '<div style="display:flex;justify-content:space-between;align-items:flex-start">'
 '<div class="kick cl sombra">Faltan 3 días para tu boda</div><div class="iso p"></div></div>'
 '<div class="gap"></div>'
 '<div class="tit sombra" style="color:#FBF9F6">¿Cuántos<br>invitados van<br>a llegar?</div>'
 '<div style="height:26px"></div>'
 '<div class="cuerpo sombra" style="color:#F1EAE2;font-size:48px">Y todavía nadie lo sabe.</div></div>'))

P.append(sl('<div class="tex" style="opacity:.16"></div>'
 '<div style="position:absolute;inset:88px;display:flex;flex-direction:column;justify-content:center">'
 '<div class="kick cl">Pasa en casi todas las bodas</div><div style="height:36px"></div>'
 '<div class="tit m" style="color:#FBF9F6">Tu lista de<br>invitados vive<br>en cuatro lados.</div>'
 '<div style="height:36px"></div>'
 '<div class="cuerpo cl">Un Excel, dos chats, lo que se acuerda tu mamá y un papel pegado '
 'en el refri. Y ninguno dice lo mismo.</div></div>', "tinta"))

BAR=[("Ya confirmaron","94","73%","#4A6580"),("Sin contestar","22","17%","#8A7259"),
     ("No pueden ir","12","10%","#5D5349")]
bar="".join(
 f'<div style="margin-bottom:46px">'
 f'<div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:16px">'
 f'<span style="font-family:UI;font-weight:500;font-size:32px;letter-spacing:.12em;'
 f'text-transform:uppercase;color:{ACENTO}">{n}</span>'
 f'<span style="font-family:Playfair;font-size:56px;color:{TINTA}">{v}</span></div>'
 f'<div style="height:16px;background:rgba(58,50,44,.16)">'
 f'<div style="height:16px;width:{p};background:{c}"></div></div></div>' for n,v,p,c in BAR)
P.append(sl('<div class="rel"></div>'
 '<div style="position:absolute;inset:88px;display:flex;flex-direction:column;justify-content:center">'
 '<div class="kick">Con la página de tu boda</div><div style="height:30px"></div>'
 '<div class="tit m">Una sola lista<br>de invitados.</div>'
 f'<div style="height:52px"></div>{bar}<div style="height:14px"></div>'
 '<div class="cuerpo" style="font-size:44px">Cada invitación trae sus lugares. Si son dos, '
 'nadie puede confirmar cuatro.</div></div>', "arena"))

P.append(sl(
 foto("frentes") + VELO_PLANO +
 '<div style="position:absolute;inset:88px;display:flex;flex-direction:column;'
 'align-items:center;text-align:center;justify-content:center;color:#FBF9F6">'
 '<div class="iso p" style="width:112px;height:112px"></div><div style="height:34px"></div>'
 '<div class="tit m sombra" style="color:#FBF9F6">Te mandamos una<br>invitación de ejemplo</div>'
 '<div style="height:26px"></div>'
 '<div class="cuerpo sombra" style="color:#F1EAE2;max-width:830px">Una página de boda completa '
 'y funcionando, para que la abras en tu celular.</div>'
 '<div style="height:46px"></div>'
 f'<div style="font-family:UI;font-weight:500;font-size:36px;letter-spacing:.14em;'
 f'text-transform:uppercase;color:{OSCURO};background:#FBF9F6;padding:30px 60px;'
 f'border-radius:999px">Escríbenos «boda» por DM</div>'
 '<div style="height:30px"></div>'
 '<div style="font-family:UI;font-weight:400;font-size:32px;letter-spacing:.12em;'
 'color:#FBF9F6" class="sombra">Contestamos el mismo día</div></div>'))

for nom in ("valor2","promo2"):
    for f in OUT.glob(nom+"-*.png"): f.unlink()
POSTS={"intro":I,"valor3":V,"promo3":P}
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":W,"height":H})
    for nom,sls in POSTS.items():
        for i,s in enumerate(sls,1):
            pg.set_content(f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{s}</body></html>")
            pg.wait_for_timeout(430); f=OUT/f"{nom}-{i}.png"; pg.screenshot(path=str(f))
            print(f.name, f.stat().st_size//1024,"KB")
    b.close()
