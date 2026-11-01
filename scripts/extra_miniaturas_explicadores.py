"""Miniaturas de YouTube de la serie Explicadores (1280 x 720).

Cada miniatura parte de una ilustración base (generada con vidIQ, una sola idea
visual) y le pone encima lo que es de la marca: saturación ajustada, franja
amarilla, titular en Barlow Condensed Bold y el isotipo.

La ilustración se descarga una vez y se guarda en png/fuentes/, así el build no
depende de que la URL original siga viva.
"""
from __future__ import annotations

import base64
import io
import urllib.request
from pathlib import Path

from PIL import Image, ImageEnhance

FUENTES = Path(__file__).resolve().parent.parent / "png" / "fuentes"
W, H = 1280, 720

MINIATURAS = {
    # Explicador 01: ¿Qué es un data warehouse? (youtu.be/W_CIi0fsHqo)
    # Base: concepto B de vidIQ (80/100). Producción rota en rojo, flecha, warehouse en verde.
    "explicador-01-miniatura-1280x720": {
        "base": "explicador-01-base.png",
        "url": "https://ai-thumbnails.s3.amazonaws.com/editor/449b31e4-8218-4dc3-974b-542eccbd7470/"
               "a1b6093e-b354-41b9-b6f1-15ece2fce785.png",
        "titulo": ("DATA", "WAREHOUSE"),
        "saturacion": 1.45,
        "contraste": 1.15,
    },
}


def _base(nombre: str, url: str) -> Image.Image:
    ruta = FUENTES / nombre
    if not ruta.exists():
        FUENTES.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(url, ruta)
    return Image.open(ruta).convert("RGB").resize((W, H), Image.LANCZOS)


def _data_uri(img: Image.Image) -> str:
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=92)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def miniatura(b, cfg: dict) -> str:
    img = _base(cfg["base"], cfg["url"])
    img = ImageEnhance.Color(img).enhance(cfg["saturacion"])
    img = ImageEnhance.Contrast(img).enhance(cfg["contraste"])

    body = (
        "<defs>"
        '<radialGradient id="alerta" cx="300" cy="260" r="460" gradientUnits="userSpaceOnUse">'
        '<stop offset="0" stop-color="#FF1E1E" stop-opacity="0.30"/>'
        '<stop offset="1" stop-color="#FF1E1E" stop-opacity="0"/></radialGradient>'
        f'<linearGradient id="piso" x1="0" y1="420" x2="0" y2="{H}" gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="{b.NAVY}" stop-opacity="0"/>'
        f'<stop offset="0.18" stop-color="{b.NAVY}" stop-opacity="0.95"/>'
        f'<stop offset="0.26" stop-color="{b.NAVY}" stop-opacity="1"/></linearGradient>'
        "</defs>"
    )
    body += f'<image href="{_data_uri(img)}" x="0" y="0" width="{W}" height="{H}"/>'
    body += f'<rect width="{W}" height="{H}" fill="url(#alerta)"/>'
    body += f'<rect y="420" width="{W}" height="{H - 420}" fill="url(#piso)"/>'
    body += f'<rect width="18" height="{H}" fill="{b.YELLOW}"/>'

    # Titular: primera palabra en blanco, segunda en amarillo, centrado y ajustado al ancho.
    uno, dos = cfg["titulo"]
    espacio = 0.28
    size = 176
    ancho = b.BOLD.width(uno, size) + size * espacio + b.BOLD.width(dos, size)
    size = min(size, size * 1180 / ancho)
    ancho = b.BOLD.width(uno, size) + size * espacio + b.BOLD.width(dos, size)
    x0, base = (W - ancho) / 2 + 9, 668
    x1 = x0 + b.BOLD.width(uno, size) + size * espacio
    sombra = (b.BOLD.path(uno, x0, base + 6, size, "#000000") + b.BOLD.path(dos, x1, base + 6, size, "#000000"))
    body += f'<g opacity="0.45">{sombra}</g>'
    body += b.BOLD.path(uno, x0, base, size, b.WHITE) + b.BOLD.path(dos, x1, base, size, b.YELLOW)

    # Isotipo arriba a la derecha: la esquina de abajo queda libre para la duración del video.
    body += b.place((b.mark(), b.MARK_BOX), W - 80, 62, 110, 80)
    return b.svg(W, H, body)


def piezas(b) -> dict[str, str]:
    return {nombre: miniatura(b, cfg) for nombre, cfg in MINIATURAS.items()}
