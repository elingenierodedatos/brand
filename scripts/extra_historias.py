"""Historias de Instagram (1080 x 1920) para anunciar lecciones del curso.

Cada historia lleva la miniatura de la lección, un titular y un espacio libre
para el sticker de enlace, dentro de las zonas seguras de Instagram
(250 px arriba y abajo).
"""
from __future__ import annotations

import base64
from pathlib import Path

PNG = Path(__file__).resolve().parent.parent / "png" / "social"
W, H = 1080, 1920

HISTORIAS = {
    "historia-leccion-01-1080x1920": {
        "miniatura": "curso-python-miniatura-01-1280x720.png",
        "titular": ("YA SALIÓ", "LA LECCIÓN 1"),
        "apoyo": ("Convertir $1,250.00 en un número", "con el que puedas sumar"),
    },
}


def historia(b, cfg: dict) -> str:
    body = b.background(W, H) + f'<rect width="18" height="{H}" fill="{b.YELLOW}"/>'
    cx = W / 2

    uno, dos = cfg["titular"]
    body += b.SEMI.path("CURSO GRATIS DE PYTHON PARA DATOS", cx, 330, 40, b.MIST, tracking=0.12, anchor="middle")
    body += b.BOLD.path(uno, cx, 500, 150, b.WHITE, anchor="middle")
    body += b.BOLD.path(dos, cx, 650, 150, b.YELLOW, anchor="middle")

    # Miniatura de la lección con borde amarillo.
    datos = base64.b64encode((PNG / cfg["miniatura"]).read_bytes()).decode()
    ancho, x0, y0 = 960, (W - 960) / 2, 720
    alto = ancho * 720 / 1280
    body += (f'<rect x="{x0 - 6}" y="{y0 - 6}" width="{ancho + 12}" height="{alto + 12}" rx="22" fill="{b.YELLOW}"/>'
             f'<image href="data:image/png;base64,{datos}" x="{x0}" y="{y0}" width="{ancho}" height="{alto}"/>')

    a1, a2 = cfg["apoyo"]
    y = y0 + alto + 100
    body += b.SEMI.path(a1, cx, y, 54, b.WHITE, tracking=0.01, anchor="middle")
    body += b.SEMI.path(a2, cx, y + 68, 54, b.WHITE, tracking=0.01, anchor="middle")

    # Flecha hacia el sticker de enlace, que va en el espacio libre de abajo.
    ya = y + 140
    body += f'<path d="M{cx - 34} {ya}L{cx + 34} {ya}L{cx} {ya + 40}Z" fill="{b.YELLOW}"/>'
    # Debajo de la flecha no va nada: ahí se pone el sticker. La marca ya va en la miniatura.
    return b.svg(W, H, body)


def piezas(b) -> dict[str, str]:
    return {nombre: historia(b, cfg) for nombre, cfg in HISTORIAS.items()}
