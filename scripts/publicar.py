#!/usr/bin/env python3
"""
Publica en Instagram la siguiente publicación de la cola.

Se ejecuta desde GitHub Actions, en los servidores de GitHub. No necesita
navegador ni que la computadora de nadie esté encendida.

Uso:
    python scripts/publicar.py valor
    python scripts/publicar.py promocion

Variables de entorno obligatorias:
    IG_USER_ID        id numérico de la cuenta de Instagram
    IG_ACCESS_TOKEN   token de larga duración
    GITHUB_REPOSITORY lo pone GitHub Actions solo (ej. alatisnere/esnuestrodia-contenido)

Sale con código 0 si publicó, 1 si algo falló, 78 si la cola estaba vacía
(eso no es un error de código, es que falta trabajo humano: hay que reponer).
"""

import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://graph.instagram.com/v26.0"
RAIZ = pathlib.Path(__file__).resolve().parent.parent
COLA = RAIZ / "cola"
PUBLICADAS = RAIZ / "publicadas"
BITACORA = RAIZ / "plan" / "publicadas.md"

# Límites de la API. Si algo de esto no se cumple, la llamada falla y es
# mejor enterarse aquí que a mitad de la publicación.
MAX_IMAGENES = 10
MAX_CAPTION = 2200
MAX_HASHTAGS = 30


def log(msg):
    print(msg, flush=True)


def morir(msg, codigo=1):
    log(f"ERROR: {msg}")
    sys.exit(codigo)


def pedir(url, datos=None, metodo="GET"):
    """Llamada a la API. Devuelve el JSON o revienta con el mensaje de Meta."""
    if datos is not None:
        cuerpo = json.dumps(datos).encode()
        req = urllib.request.Request(
            url, data=cuerpo, method=metodo,
            headers={"Content-Type": "application/json"},
        )
    else:
        req = urllib.request.Request(url, method=metodo)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        detalle = e.read().decode(errors="replace")
        raise RuntimeError(f"{e.code} {e.reason} — {detalle}") from None


def siguiente_de_la_cola(tipo):
    """El archivo pendiente más antiguo del tipo pedido, por orden de nombre."""
    if not COLA.is_dir():
        return None
    for ruta in sorted(COLA.glob("*.json")):
        try:
            datos = json.loads(ruta.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            log(f"  aviso: {ruta.name} no es JSON válido ({e}); lo salto")
            continue
        if datos.get("tipo") == tipo:
            return ruta, datos
    return None


def revisar(datos, repo, rama):
    """Valida antes de tocar la API, para no dejar contenedores a medias."""
    imagenes = datos.get("imagenes") or []
    if not imagenes:
        morir("la publicación no trae imágenes")
    if len(imagenes) > MAX_IMAGENES:
        morir(f"{len(imagenes)} imágenes; el máximo por carrusel es {MAX_IMAGENES}")

    caption = datos.get("caption", "")
    if len(caption) > MAX_CAPTION:
        morir(f"el copy tiene {len(caption)} caracteres; el máximo es {MAX_CAPTION}")
    hashtags = caption.count("#")
    if hashtags > MAX_HASHTAGS:
        morir(f"{hashtags} hashtags; el máximo es {MAX_HASHTAGS}")

    urls = []
    for rel in imagenes:
        archivo = RAIZ / rel
        if not archivo.is_file():
            morir(f"no existe la imagen {rel}")
        if archivo.suffix.lower() not in (".jpg", ".jpeg"):
            morir(f"{rel} no es .jpg — Instagram solo acepta JPEG por API")
        if archivo.stat().st_size > 8 * 1024 * 1024:
            morir(f"{rel} pesa más de 8 MB")
        urls.append(
            "https://raw.githubusercontent.com/"
            f"{repo}/{rama}/{urllib.parse.quote(rel)}"
        )
    return urls, caption


def esperar_contenedor(cid, token, intentos=20, espera=3):
    """Los contenedores de imagen suelen quedar listos enseguida, pero no siempre."""
    for i in range(intentos):
        r = pedir(f"{API}/{cid}?fields=status_code&access_token={token}")
        estado = r.get("status_code")
        if estado == "FINISHED":
            return True
        if estado in ("ERROR", "EXPIRED"):
            morir(f"el contenedor {cid} quedó en estado {estado}")
        time.sleep(espera)
    morir(f"el contenedor {cid} no terminó después de {intentos * espera} segundos")


def anotar_en_bitacora(tipo, datos, post_id, fecha):
    linea = (
        f"- {fecha} · {tipo} · {datos.get('titulo', 'sin título')} "
        f"· {len(datos['imagenes'])} láminas · id {post_id}\n"
    )
    BITACORA.parent.mkdir(parents=True, exist_ok=True)
    if not BITACORA.exists():
        BITACORA.write_text("# Bitácora de publicaciones\n\n", encoding="utf-8")
    with BITACORA.open("a", encoding="utf-8") as f:
        f.write(linea)


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ("valor", "promocion"):
        morir("uso: publicar.py valor|promocion")
    tipo = sys.argv[1]

    token = os.environ.get("IG_ACCESS_TOKEN")
    ig_id = os.environ.get("IG_USER_ID")
    if not token or not ig_id:
        morir("faltan IG_ACCESS_TOKEN o IG_USER_ID")

    repo = os.environ.get("GITHUB_REPOSITORY", "alatisnere/esnuestrodia-contenido")
    rama = os.environ.get("GITHUB_REF_NAME", "main")

    encontrado = siguiente_de_la_cola(tipo)
    if not encontrado:
        log(f"La cola no tiene ninguna publicación de tipo «{tipo}».")
        log("No se publicó nada. Hay que reponer la cola.")
        sys.exit(78)
    ruta, datos = encontrado
    log(f"Toca publicar: {ruta.name} — {datos.get('titulo', '')}")

    urls, caption = revisar(datos, repo, rama)

    # Cuánto margen queda en la ventana de 24 horas.
    try:
        lim = pedir(f"{API}/{ig_id}/content_publishing_limit"
                    f"?fields=quota_usage,config&access_token={token}")
        usado = lim.get("data", [{}])[0].get("quota_usage")
        if usado is not None:
            log(f"Publicaciones usadas en las últimas 24 h: {usado}")
    except Exception as e:
        log(f"  aviso: no pude leer el límite de publicación ({e})")

    # 1. Un contenedor por lámina.
    hijos = []
    for i, url in enumerate(urls, 1):
        r = pedir(f"{API}/{ig_id}/media", {
            "image_url": url,
            "is_carousel_item": True,
            "access_token": token,
        }, "POST")
        hijos.append(r["id"])
        log(f"  lámina {i}/{len(urls)} lista ({r['id']})")

    for cid in hijos:
        esperar_contenedor(cid, token)

    # 2. El carrusel.
    carrusel = pedir(f"{API}/{ig_id}/media", {
        "media_type": "CAROUSEL",
        "caption": caption,
        "children": ",".join(hijos),
        "access_token": token,
    }, "POST")["id"]
    log(f"Carrusel armado ({carrusel})")
    esperar_contenedor(carrusel, token)

    # 3. Publicar.
    post_id = pedir(f"{API}/{ig_id}/media_publish", {
        "creation_id": carrusel,
        "access_token": token,
    }, "POST")["id"]
    log(f"PUBLICADO — id {post_id}")

    # 4. Sacar de la cola y dejar constancia.
    fecha = time.strftime("%Y-%m-%d", time.gmtime())
    PUBLICADAS.mkdir(parents=True, exist_ok=True)
    datos["publicado_en"] = fecha
    datos["post_id"] = post_id
    destino = PUBLICADAS / f"{fecha}-{ruta.name}"
    destino.write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")
    ruta.unlink()
    anotar_en_bitacora(tipo, datos, post_id, fecha)

    # Cuánto queda en la cola, para avisar antes de quedarnos secos.
    quedan = {t: 0 for t in ("valor", "promocion")}
    for f in COLA.glob("*.json"):
        try:
            quedan[json.loads(f.read_text(encoding="utf-8")).get("tipo")] += 1
        except Exception:
            pass
    log(f"Quedan en la cola: {quedan['valor']} de valor, {quedan['promocion']} de promoción")

    resumen = os.environ.get("GITHUB_STEP_SUMMARY")
    if resumen:
        with open(resumen, "a", encoding="utf-8") as f:
            f.write(
                f"### Publicado\n\n"
                f"- **{datos.get('titulo','')}** ({tipo})\n"
                f"- https://www.instagram.com/p/ — id `{post_id}`\n"
                f"- Quedan {quedan['valor']} de valor y {quedan['promocion']} de promoción\n"
            )

    if quedan[tipo] == 0:
        log(f"AVISO: era la última de tipo «{tipo}». Hay que reponer la cola.")


if __name__ == "__main__":
    main()
