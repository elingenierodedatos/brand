"""Piezas puntuales: anuncios y campañas."""


def anuncio_rebrand(b, w: int, h: int) -> str:
    """Anuncio del cambio de nombre: el nombre anterior tachado y el logo nuevo."""
    u = min(w, h) / 1080  # unidad de escala
    cx = w / 2
    top = h * 0.16
    viejo = "El Ingeniero de Datos Jr."
    size = 58 * u
    ancho = b.SEMI.width(viejo, size, 0.01)
    body = b.background(w, h)
    body += b.SEMI.path(viejo, cx, top, size, b.MIST, tracking=0.01, anchor="middle")
    body += (f'<rect x="{cx - ancho / 2 - 14 * u:.1f}" y="{top - size * 0.36:.1f}" '
             f'width="{ancho + 28 * u:.1f}" height="{7 * u:.1f}" fill="{b.YELLOW}"/>')
    body += b.SEMI.path("AHORA ES", cx, top + 96 * u, 34 * u, b.MIST, tracking=0.32, anchor="middle")
    body += b.place(b.lockup_v(), cx, h * 0.56, w * 0.74, h * 0.50)
    body += b.SEMI.path(b.TAGLINE, cx, h * 0.92, 46 * u, b.WHITE, tracking=0.01, anchor="middle")
    return b.svg(w, h, body)


def piezas(b) -> dict[str, str]:
    return {
        "anuncio-rebrand-1080x1350": anuncio_rebrand(b, 1080, 1350),
        "anuncio-rebrand-1200x675": anuncio_rebrand(b, 1200, 675),
    }
