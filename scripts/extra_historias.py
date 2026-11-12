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
    "historia-leccion-02-1080x1920": {
        "miniatura": "curso-python-miniatura-02-1280x720.png",
        "titular": ("YA SALIÓ", "LA LECCIÓN 2"),
        "apoyo": ("Recorrer una lista con un for", "y acumular el total, vuelta por vuelta"),
    },
    "historia-leccion-03-1080x1920": {
        "miniatura": "curso-python-miniatura-03-1280x720.png",
        "titular": ("YA SALIÓ", "LA LECCIÓN 3"),
        "apoyo": ("Tu código aprende a preguntar", "antes de actuar: if, elif, else y while"),
    },
    "historia-explicador-02-1080x1920": {
        "miniatura": "../youtube/miniatura-explicador-ep02-v2-1280x720.png",
        "encabezado": "SERIE EXPLICADORES · EPISODIO 2",
        "titular": ("YA SALIÓ", "EL MODELO ESTRELLA"),
        "tam": 104,
        "apoyo": ("Un ticket de 100 pesos que suma 400", "y cómo se evita, en 7 minutos"),
    },
}

ENCABEZADO = "CURSO GRATIS DE PYTHON PARA DATOS"


def historia(b, cfg: dict) -> str:
    body = b.background(W, H) + f'<rect width="18" height="{H}" fill="{b.YELLOW}"/>'
    cx = W / 2

    uno, dos = cfg["titular"]
    body += b.SEMI.path(cfg.get("encabezado", ENCABEZADO), cx, 330, 40, b.MIST, tracking=0.12, anchor="middle")
    t = cfg.get("tam", 150)
    body += b.BOLD.path(uno, cx, 500, t, b.WHITE, anchor="middle")
    body += b.BOLD.path(dos, cx, 650, t, b.YELLOW, anchor="middle")

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


def publicacion(b, cfg: dict) -> str:
    """Misma pieza en 1080 x 1350 para el feed de Instagram, sin flecha de sticker."""
    w, h = 1080, 1350
    body = b.background(w, h) + f'<rect width="18" height="{h}" fill="{b.YELLOW}"/>'
    cx = w / 2
    uno, dos = cfg["titular"]
    body += b.SEMI.path(cfg.get("encabezado", ENCABEZADO), cx, 130, 36, b.MIST, tracking=0.12, anchor="middle")
    t = cfg.get("tam", 150) * 130 / 150
    body += b.BOLD.path(uno, cx, 270, t, b.WHITE, anchor="middle")
    body += b.BOLD.path(dos, cx, 400, t, b.YELLOW, anchor="middle")
    datos = base64.b64encode((PNG / cfg["miniatura"]).read_bytes()).decode()
    ancho, x0, y0 = 960, (w - 960) / 2, 460
    alto = ancho * 720 / 1280
    body += (f'<rect x="{x0 - 6}" y="{y0 - 6}" width="{ancho + 12}" height="{alto + 12}" rx="22" fill="{b.YELLOW}"/>'
             f'<image href="data:image/png;base64,{datos}" x="{x0}" y="{y0}" width="{ancho}" height="{alto}"/>')
    a1, a2 = cfg["apoyo"]
    y = y0 + alto + 110
    body += b.SEMI.path(a1, cx, y, 52, b.WHITE, tracking=0.01, anchor="middle")
    body += b.SEMI.path(a2, cx, y + 66, 52, b.WHITE, tracking=0.01, anchor="middle")
    return b.svg(w, h, body)


def piezas(b) -> dict[str, str]:
    out = {nombre: historia(b, cfg) for nombre, cfg in HISTORIAS.items()}
    for nombre, cfg in HISTORIAS.items():
        out[nombre.replace("historia-", "publicacion-").replace("1080x1920", "1080x1350")] = publicacion(b, cfg)
    return out
