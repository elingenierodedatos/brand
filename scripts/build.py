"""Genera el logo y el kit de redes de EL INGENIERO DE DATOS.

Uso:  python scripts/build.py
Salida: logo/*.svg, social/*.svg, favicon/* y sus PNG en png/.

Los SVG son la fuente de verdad. El texto se convierte a trazos, así que los
archivos no dependen de tener la tipografía instalada.

El lema de los banners se edita en scripts/lema.txt.
"""
from __future__ import annotations

import io
import urllib.request
from pathlib import Path

import cairosvg
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = ROOT / ".fonts"
FONT_URL = "https://raw.githubusercontent.com/google/fonts/main/ofl/barlowcondensed/{}.ttf"

NAVY = "#0B1F3A"       # fondo y texto sobre claro
NAVY_SOFT = "#17335C"  # trama de puntos sobre el fondo
YELLOW = "#F5B800"     # acento
YELLOW_TOP = "#FFD84D" # tapa del cilindro
WHITE = "#FFFFFF"
MIST = "#C9D3E0"       # texto secundario sobre marino

TAGLINE = (Path(__file__).resolve().parent / "lema.txt").read_text(encoding="utf-8").strip()


# --------------------------------------------------------------------------- tipografía
class Face:
    def __init__(self, name: str):
        path = FONT_DIR / f"{name}.ttf"
        if not path.exists():
            FONT_DIR.mkdir(exist_ok=True)
            urllib.request.urlretrieve(FONT_URL.format(name), path)
        font = TTFont(path)
        self.glyphs, self.cmap, self.upm = font.getGlyphSet(), font.getBestCmap(), font["head"].unitsPerEm

    def width(self, text: str, size: float, tracking: float = 0.02) -> float:
        scale = size / self.upm
        return sum(self.glyphs[self.cmap[ord(c)]].width * scale + size * tracking for c in text) - size * tracking

    def path(self, text: str, x: float, baseline: float, size: float, fill: str,
             tracking: float = 0.02, anchor: str = "start") -> str:
        if anchor == "middle":
            x -= self.width(text, size, tracking) / 2
        scale = size / self.upm
        pen = SVGPathPen(self.glyphs)
        for ch in text:
            name = self.cmap[ord(ch)]
            self.glyphs[name].draw(TransformPen(pen, (scale, 0, 0, -scale, x, baseline)))
            x += self.glyphs[name].width * scale + size * tracking
        return f'<path d="{pen.getCommands()}" fill="{fill}"/>'


BOLD = Face("BarlowCondensed-Bold")
SEMI = Face("BarlowCondensed-SemiBold")


# --------------------------------------------------------------------------- isotipo
def disk(top: int, bottom: int) -> str:
    return f'<path d="M184 {top}A72 25 0 0 0 328 {top}V{bottom}A72 25 0 0 1 184 {bottom}Z"/>'


def cylinder() -> str:
    return (f'<g fill="{YELLOW}">{disk(185, 223)}{disk(237, 275)}{disk(289, 327)}</g>'
            f'<ellipse cx="256" cy="185" rx="72" ry="25" fill="{YELLOW_TOP}"/>')


def mark(brace: str = WHITE) -> str:
    """Isotipo en un lienzo de 512: llaves de código que encierran un cilindro de datos."""
    left = ("M142 110C108 110 96 128 96 162V208C96 234 82 250 58 256"
            "C82 262 96 278 96 304V350C96 384 108 402 142 402")
    right = ("M370 110C404 110 416 128 416 162V208C416 234 430 250 454 256"
             "C430 262 416 278 416 304V350C416 384 404 402 370 402")
    return (f'<g fill="none" stroke="{brace}" stroke-width="32" stroke-linecap="round" '
            f'stroke-linejoin="round"><path d="{left}"/><path d="{right}"/></g>' + cylinder())


MARK_BOX = (42, 94, 470, 418)  # caja visible del isotipo


# --------------------------------------------------------------------------- composiciones
def lockup_h(brace=WHITE, line1=WHITE, line2=YELLOW, tagline: str | None = None, tag_fill=MIST):
    """Isotipo a la izquierda y nombre en dos líneas. Devuelve (svg, caja)."""
    body = mark(brace) + BOLD.path("EL INGENIERO", 500, 236, 168, line1) + BOLD.path("DE DATOS", 500, 392, 168, line2)
    right = 500 + max(BOLD.width("EL INGENIERO", 168), BOLD.width("DE DATOS", 168))
    bottom = 418
    if tagline:
        body += SEMI.path(tagline, 502, 478, 62, tag_fill, tracking=0.01)
        right = max(right, 502 + SEMI.width(tagline, 62, 0.01))
        bottom = 494
    return body, (42, 94, right, bottom)


def lockup_v(label: str | None = None, tagline: str | None = None):
    """Isotipo arriba y nombre centrado debajo. Devuelve (svg, caja)."""
    body = mark() + BOLD.path("EL INGENIERO", 256, 560, 118, WHITE, anchor="middle")
    body += BOLD.path("DE DATOS", 256, 672, 118, YELLOW, anchor="middle")
    half = max(BOLD.width("EL INGENIERO", 118) / 2, BOLD.width("DE DATOS", 118) / 2, 214)
    bottom = 676
    if label:
        body += SEMI.path(label, 256, 760, 60, MIST, tracking=0.32, anchor="middle")
        bottom = 764
    if tagline:
        body += SEMI.path(tagline, 256, 748, 40, MIST, tracking=0.01, anchor="middle")
        half = max(half, SEMI.width(tagline, 40, 0.01) / 2)
        bottom = 760
    return body, (256 - half, 94, 256 + half, bottom)


def place(item, cx: float, cy: float, max_w: float, max_h: float) -> str:
    """Escala y centra una composición dentro de una caja."""
    body, (x0, y0, x1, y1) = item
    s = min(max_w / (x1 - x0), max_h / (y1 - y0))
    tx, ty = cx - s * (x0 + x1) / 2, cy - s * (y0 + y1) / 2
    return f'<g transform="translate({tx:.2f} {ty:.2f}) scale({s:.4f})">{body}</g>'


def background(w: int, h: int, dots: bool = True, radius: int = 0) -> str:
    out = f'<rect width="{w}" height="{h}" rx="{radius}" fill="{NAVY}"/>'
    if dots:
        step = max(24, round(min(w, h) / 22))
        out = (f'<defs><pattern id="puntos" width="{step}" height="{step}" patternUnits="userSpaceOnUse">'
               f'<circle cx="{step / 2}" cy="{step / 2}" r="{step / 14:.2f}" fill="{NAVY_SOFT}"/></pattern></defs>'
               + out + f'<rect width="{w}" height="{h}" fill="url(#puntos)"/>')
    return out


def svg(w: int, h: int, body: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="EL INGENIERO DE DATOS">{body}</svg>\n')


def banner(w, h, cx, cy, max_w, max_h, tagline=True):
    return svg(w, h, background(w, h) + place(lockup_h(tagline=TAGLINE if tagline else None), cx, cy, max_w, max_h))


def stacked(w, h, scale=0.62, label=None, tagline=None, dots=True):
    return svg(w, h, background(w, h, dots) + place(lockup_v(label, tagline), w / 2, h / 2, w * scale, h * scale))


def avatar(size: int, fill: float = 0.6) -> str:
    """Isotipo centrado con margen para el recorte circular de las redes."""
    return svg(size, size, background(size, size, dots=False)
               + place((mark(), MARK_BOX), size / 2, size / 2, size * fill, size * fill))


def thumbnail() -> str:
    w, h = 1280, 720
    body = background(w, h) + f'<rect width="18" height="{h}" fill="{YELLOW}"/>'
    body += place((mark(), MARK_BOX), w - 130, h - 105, 150, 150)
    return svg(w, h, body)


def favicon() -> str:
    """A 16 px las llaves se empastan: el favicon usa solo el cilindro."""
    body = f'<rect width="512" height="512" rx="104" fill="{NAVY}"/>'
    body += f'<g transform="translate(-205 -205) scale(1.8)">{cylinder()}</g>'
    return svg(512, 512, body)


# --------------------------------------------------------------------------- catálogo
LOGO = {
    "eid-logo-horizontal-oscuro": lambda: svg(*_fit(lockup_h(), NAVY)),
    "eid-logo-horizontal-claro": lambda: svg(*_fit(lockup_h(NAVY, NAVY, NAVY), WHITE)),
    "eid-logo-horizontal-transparente-para-oscuro": lambda: svg(*_fit(lockup_h(), None)),
    "eid-logo-horizontal-transparente-para-claro": lambda: svg(*_fit(lockup_h(NAVY, NAVY, NAVY), None)),
    "eid-logo-vertical-oscuro": lambda: svg(1024, 1024, background(1024, 1024, False) + place(lockup_v(), 512, 512, 760, 760)),
    "eid-isotipo-para-oscuro": lambda: svg(512, 512, mark()),
    "eid-isotipo-para-claro": lambda: svg(512, 512, mark(NAVY)),
    "eid-icono-app": lambda: svg(512, 512, f'<rect width="512" height="512" rx="104" fill="{NAVY}"/>' + mark()),
}


def _fit(item, bg):
    body, (x0, y0, x1, y1) = item
    pad = 70
    w, h = round(x1 - x0 + 2 * pad), round(y1 - y0 + 2 * pad)
    back = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return w, h, back + f'<g transform="translate({pad - x0:.2f} {pad - y0:.2f})">{body}</g>'


SOCIAL = {
    # nombre: (constructor, red y uso)
    "avatar-1080": (lambda: avatar(1080), "Avatar universal"),
    "youtube-banner-2560x1440": (lambda: banner(2560, 1440, 1280, 720, 1400, 380), "YouTube, banner del canal"),
    "youtube-miniatura-plantilla-1280x720": (thumbnail, "YouTube, base para miniaturas"),
    "youtube-marca-de-agua-150": (lambda: svg(150, 150, f'<g transform="scale({150 / 512:.5f})"><rect width="512" height="512" rx="104" fill="{NAVY}"/>{mark()}</g>'), "YouTube, marca de agua"),
    "linkedin-banner-perfil-1584x396": (lambda: banner(1584, 396, 1060, 198, 900, 250), "LinkedIn, perfil personal"),
    "linkedin-portada-pagina-1512x256": (lambda: banner(1512, 256, 800, 128, 800, 176), "LinkedIn, página de empresa"),
    "x-encabezado-1500x500": (lambda: banner(1500, 500, 750, 215, 980, 270), "X, encabezado"),
    "facebook-portada-1640x624": (lambda: banner(1640, 624, 820, 312, 1050, 300), "Facebook, portada"),
    "instagram-publicacion-1080x1350": (lambda: stacked(1080, 1350, 0.7), "Instagram y Threads, publicación"),
    "instagram-historia-1080x1920": (lambda: stacked(1080, 1920, 0.74), "Instagram, historia"),
    "podcast-portada-3000": (lambda: stacked(3000, 3000, 0.7, label="PODCAST"), "Spotify y Apple Podcasts"),
    "discord-banner-960x540": (lambda: banner(960, 540, 480, 270, 760, 230), "Discord, banner del servidor"),
    "github-social-1280x640": (lambda: banner(1280, 640, 640, 320, 940, 290), "GitHub, vista previa de repos"),
    "og-image-1200x630": (lambda: banner(1200, 630, 600, 315, 900, 280), "Sitio web, imagen al compartir enlaces"),
}

FAVICON_SIZES = (16, 32, 48, 180, 192, 512)


def png(svg_text: str, path: Path, size: int | None = None) -> None:
    kwargs = {"output_width": size, "output_height": size} if size else {}
    cairosvg.svg2png(bytestring=svg_text.encode(), write_to=str(path), **kwargs)


def main() -> None:
    for folder in ("logo", "social", "favicon", "png/logo", "png/social"):
        (ROOT / folder).mkdir(parents=True, exist_ok=True)
    for name, make in LOGO.items():
        text = make()
        (ROOT / "logo" / f"{name}.svg").write_text(text, encoding="utf-8")
        png(text, ROOT / "png" / "logo" / f"{name}.png")
    for name, (make, _) in SOCIAL.items():
        text = make()
        (ROOT / "social" / f"{name}.svg").write_text(text, encoding="utf-8")
        png(text, ROOT / "png" / "social" / f"{name}.png")
    icon = favicon()
    (ROOT / "favicon" / "favicon.svg").write_text(icon, encoding="utf-8")
    for size in FAVICON_SIZES:
        png(icon, ROOT / "favicon" / f"favicon-{size}.png", size)
    buffer = io.BytesIO()
    cairosvg.svg2png(bytestring=icon.encode(), write_to=buffer, output_width=256, output_height=256)
    Image.open(buffer).save(ROOT / "favicon" / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    print(f"{len(LOGO)} logos, {len(SOCIAL)} piezas de redes y {len(FAVICON_SIZES) + 2} favicons generados.")


if __name__ == "__main__":
    main()
