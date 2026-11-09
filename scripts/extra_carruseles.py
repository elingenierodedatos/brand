"""Carruseles de Instagram (1080 x 1350) hechos en HTML y capturados con Playwright.

Cada carrusel vive en carruseles/<nombre>.mjs y genera sus láminas como
png/social/carrusel-<nombre>-NN-1080x1350.png. Se registran en CARRUSELES para
que un cambio aquí dispare el workflow de assets (solo mira scripts/**).

No devuelve piezas SVG: las láminas se escriben directo como PNG. Si Node o
Playwright fallan, se avisa y el resto de los assets se sigue generando.
"""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CARRUSELES = [
    "r004-ciclo-de-vida",
]

DEPENDENCIAS = ["playwright@1.48.2", "@fontsource/bebas-neue@5.1.0", "@fontsource/inter@5.1.0"]


def _correr(cmd: list[str]) -> None:
    subprocess.run(cmd, cwd=ROOT, check=True)


def piezas(b) -> dict:
    if not shutil.which("node") or not shutil.which("npm"):
        print("Aviso: no hay Node en este entorno, se omiten los carruseles.")
        return {}
    try:
        _correr(["npm", "install", "--no-save", "--no-package-lock", *DEPENDENCIAS])
        _correr(["npx", "playwright", "install", "--with-deps", "chromium"])
        for nombre in CARRUSELES:
            _correr(["node", f"carruseles/{nombre}.mjs", "png/social", f"carrusel-{nombre}"])
    except subprocess.CalledProcessError as error:
        print(f"Aviso: no se pudieron generar los carruseles ({error}).")
    return {}
