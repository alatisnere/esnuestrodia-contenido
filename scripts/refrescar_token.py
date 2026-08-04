#!/usr/bin/env python3
"""
Renueva el token de Instagram por otros 60 días y lo guarda de vuelta
en los secretos del repositorio.

El token de larga duración dura 60 días y se puede renovar sin intervención
humana, siempre que se renueve ANTES de que caduque. Este script corre cada
tres semanas, así que hay margen de sobra.

Si el token llega a caducar del todo, ya no hay renovación posible: hay que
volver a generarlo a mano en el panel de Meta.

Variables de entorno:
    IG_ACCESS_TOKEN   token vigente
    GH_TOKEN          token de GitHub con permiso de escritura en secretos
    GITHUB_REPOSITORY lo pone GitHub Actions solo
"""

import json
import os
import subprocess
import sys
import urllib.request

API = "https://graph.instagram.com"


def main():
    token = os.environ.get("IG_ACCESS_TOKEN")
    if not token:
        print("ERROR: falta IG_ACCESS_TOKEN")
        sys.exit(1)

    url = f"{API}/refresh_access_token?grant_type=ig_refresh_token&access_token={token}"
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            datos = json.loads(r.read())
    except Exception as e:
        print(f"ERROR: no se pudo renovar el token — {e}")
        print("Si ya caducó, hay que generarlo de nuevo en el panel de Meta.")
        sys.exit(1)

    nuevo = datos["access_token"]
    dias = int(datos.get("expires_in", 0)) // 86400
    print(f"Token renovado. Vence en {dias} días.")

    # Guardarlo de vuelta como secreto del repositorio.
    subprocess.run(
        ["gh", "secret", "set", "IG_ACCESS_TOKEN"],
        input=nuevo, text=True, check=True,
    )
    print("Secreto IG_ACCESS_TOKEN actualizado.")

    resumen = os.environ.get("GITHUB_STEP_SUMMARY")
    if resumen:
        with open(resumen, "a", encoding="utf-8") as f:
            f.write(f"Token de Instagram renovado. Vence en {dias} días.\n")


if __name__ == "__main__":
    main()
