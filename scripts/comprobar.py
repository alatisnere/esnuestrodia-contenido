#!/usr/bin/env python3
"""
Comprueba que la conexión con Instagram está bien puesta, sin publicar nada.

Dice a qué cuenta apunta el token, cuántos días le quedan, cuánto margen
queda en la ventana de publicación y qué hay en la cola. Nunca imprime el
token.
"""

import json
import os
import pathlib
import sys
import urllib.request

API = "https://graph.instagram.com/v26.0"
RAIZ = pathlib.Path(__file__).resolve().parent.parent
COLA = RAIZ / "cola"

lineas = []


def di(msg):
    print(msg, flush=True)
    lineas.append(msg)


def pedir(url):
    with urllib.request.urlopen(url, timeout=45) as r:
        return json.loads(r.read())


def main():
    token = os.environ.get("IG_ACCESS_TOKEN")
    ig_id = os.environ.get("IG_USER_ID")
    problemas = []

    if not token:
        problemas.append("Falta el secreto IG_ACCESS_TOKEN.")
    if not ig_id:
        problemas.append("Falta el secreto IG_USER_ID.")
    if problemas:
        for p in problemas:
            di(f"MAL — {p}")
        escribir_resumen()
        sys.exit(1)

    # ¿A qué cuenta apunta el token?
    try:
        yo = pedir(f"{API}/me?fields=user_id,username&access_token={token}")
        di(f"BIEN — el token es de la cuenta @{yo.get('username')} (id {yo.get('user_id')})")
        if str(yo.get("user_id")) != str(ig_id):
            di(f"OJO — IG_USER_ID dice {ig_id} pero el token es de {yo.get('user_id')}. "
               "Corrige el secreto IG_USER_ID.")
            problemas.append("IG_USER_ID no coincide")
    except Exception as e:
        di(f"MAL — el token no sirve: {e}")
        escribir_resumen()
        sys.exit(1)

    # ¿Cuánto le queda de vida?
    try:
        info = pedir(f"https://graph.instagram.com/refresh_access_token"
                     f"?grant_type=ig_refresh_token&access_token={token}")
        dias = int(info.get("expires_in", 0)) // 86400
        di(f"BIEN — el token es de larga duración; le quedan unos {dias} días")
    except Exception:
        di("OJO — no se pudo renovar el token. Puede ser que sea de corta duración "
           "(dura 1 hora) o que tenga menos de 24 horas de vida. Si acabas de "
           "generarlo en el panel de Meta, espera un día y vuelve a comprobar.")

    # Margen de publicación.
    try:
        lim = pedir(f"{API}/{ig_id}/content_publishing_limit"
                    f"?fields=quota_usage&access_token={token}")
        usado = lim.get("data", [{}])[0].get("quota_usage", 0)
        di(f"BIEN — {usado} publicaciones usadas de 100 en las últimas 24 horas")
    except Exception as e:
        di(f"OJO — no pude leer el límite de publicación ({e})")

    # Cola.
    cuenta = {"valor": 0, "promocion": 0}
    for f in sorted(COLA.glob("*.json")) if COLA.is_dir() else []:
        try:
            cuenta[json.loads(f.read_text(encoding="utf-8")).get("tipo")] += 1
        except Exception:
            di(f"OJO — {f.name} no se pudo leer")
    di(f"Cola: {cuenta['valor']} de valor, {cuenta['promocion']} de promoción")
    if cuenta["valor"] == 0 or cuenta["promocion"] == 0:
        di("OJO — falta material en la cola; hay que reponerla.")

    escribir_resumen()
    sys.exit(1 if problemas else 0)


def escribir_resumen():
    ruta = os.environ.get("GITHUB_STEP_SUMMARY")
    if ruta:
        with open(ruta, "a", encoding="utf-8") as f:
            f.write("### Comprobación\n\n")
            for l in lineas:
                f.write(f"- {l}\n")


if __name__ == "__main__":
    main()
