"""Calendario semanal de publicación, una lámina 1920 × 1080 para tener a la vista.

Refleja la Estrategia vigente v3 (27 de octubre de 2026): qué sale cada día,
a qué hora (Ciudad de México) y con qué periodicidad. Cuando cambie el
calendario en Notion, se cambia aquí y el workflow regenera el PNG.

Tipos de pieza (color del chip):
  largo     amarillo lleno      videos largos de YouTube (lección, Carrera)
  derivado  verde               podcast y explicador (derivados o experimento)
  short     contorno amarillo   shorts en YouTube, TikTok y Reels
  texto     marino claro        Threads, LinkedIn y feed de Instagram
  tarea     gris punteado       lo que hace Elmer, no se publica
"""

W, H = 1920, 1080
MARGEN = 72
GREEN = "#3DDC84"

VIGENCIA = "CALENDARIO SEMANAL V3  ·  DESDE EL 2 DE NOVIEMBRE DE 2026  ·  HORA DE CIUDAD DE MÉXICO"

# (día, [(hora, red, tipo, líneas)])
DIAS = [
    ("LUNES", [
        ("12:30", "THREADS", "texto", ["Pregunta o problema", "de la semana"]),
        ("18:30", "SHORT 1", "short", ["De un largo", "ya publicado"]),
    ]),
    ("MARTES", [
        ("8:30", "LINKEDIN", "texto", ["Aprendizaje aplicado", "de la lección"]),
        ("10:00", "YOUTUBE", "largo", ["LECCIÓN DEL CURSO", "60 a 100 min"]),
        ("19:00", "INSTAGRAM FEED", "texto", ["Carrusel de la lección", "(opcional, nunca con Reel)"]),
        ("19:30", "THREADS", "texto", ["Ejemplo de la lección", "con enlace"]),
    ]),
    ("MIÉRCOLES", [
        ("18:30", "SHORT 2", "short", ["Resultado o error", "de la lección"]),
        ("19:30", "THREADS", "texto", ["Conversación sobre", "el ejemplo (opcional)"]),
    ]),
    ("JUEVES", [
        ("8:30", "LINKEDIN", "texto", ["Postura o experiencia", "propia"]),
        ("12:30", "YOUTUBE", "largo", ["CARRERA EN DATOS", "12 a 15 min, a cámara"]),
        ("19:30", "THREADS", "texto", ["Una idea del episodio", "con enlace"]),
    ]),
    ("VIERNES", [
        ("8:00", "PODCAST", "derivado", ["Audio del episodio", "del jueves"]),
        ("18:30", "SHORT 3", "short", ["Relacionado con", "Carrera en datos"]),
    ]),
    ("SÁBADO", [
        ("10:00", "YOUTUBE", "derivado", ["EXPLICADOR", "cada dos semanas"]),
        ("10:30", "THREADS", "texto", ["Pregunta o reflexión", "(opcional)"]),
        ("TARDE", "GRABACIÓN", "tarea", ["Episodio y lección", "por bloques"]),
    ]),
    ("DOMINGO", [
        ("MAÑANA", "REVISIÓN", "tarea", ["Horas válidas (Studio)", "y plan de la semana"]),
        ("TARDE", "PROGRAMAR", "tarea", ["Buffer y YouTube de", "la semana que entra"]),
    ]),
]

RESUMEN = [
    ("2", "LARGOS"),
    ("3", "SHORTS"),
    ("1", "PODCAST"),
    ("2", "LINKEDIN"),
    ("3 A 4", "THREADS"),
    ("3 + 1", "REELS + CARRUSEL"),
]

RECORTE = "SI NO ALCANZA EL TIEMPO SE RECORTA EN ESTE ORDEN: CARRUSEL, THREADS OPCIONALES, LINKEDIN DEL JUEVES, SHORT 3.  NUNCA LA LECCIÓN NI EL EPISODIO."


def _chip(b, x, y, w, hora, red, tipo, lineas):
    """Un bloque de publicación. Devuelve (svg, alto)."""
    alto = 46 + 34 * len(lineas) + 18
    if tipo == "largo":
        fondo, borde, t1, t2 = b.YELLOW, b.YELLOW, b.NAVY, b.NAVY
    elif tipo == "derivado":
        fondo, borde, t1, t2 = GREEN, GREEN, b.NAVY, b.NAVY
    elif tipo == "short":
        fondo, borde, t1, t2 = "none", b.YELLOW, b.YELLOW, b.WHITE
    elif tipo == "texto":
        fondo, borde, t1, t2 = b.NAVY_SOFT, b.NAVY_SOFT, b.WHITE, b.MIST
    else:  # tarea
        fondo, borde, t1, t2 = "none", b.MIST, b.MIST, b.MIST
    dash = ' stroke-dasharray="6 6"' if tipo == "tarea" else ""
    out = (f'<rect x="{x}" y="{y}" width="{w}" height="{alto}" rx="12" fill="{fondo}" '
           f'stroke="{borde}" stroke-width="3"{dash}/>')
    out += b.BOLD.path(hora, x + 18, y + 36, 34, t1, tracking=0.02)
    ancho_hora = b.BOLD.width(hora, 34, 0.02)
    out += b.SEMI.path(red, x + 18 + ancho_hora + 12, y + 35, 20, t1, tracking=0.14)
    yy = y + 36
    for linea in lineas:
        yy += 34
        # Si una línea no cabe en el chip, baja el tamaño en lugar de salirse.
        tam = 28
        while tam > 20 and b.SEMI.width(linea, tam, 0.01) > w - 36:
            tam -= 1
        out += b.SEMI.path(linea, x + 18, yy, tam, t2, tracking=0.01)
    return out, alto


def calendario(b):
    body = b.background(W, H) + f'<rect width="18" height="{H}" fill="{b.YELLOW}"/>'
    body += b.SEMI.path(VIGENCIA, MARGEN, 76, 26, b.MIST, tracking=0.2)
    body += b.BOLD.path("QUÉ SE PUBLICA", MARGEN, 160, 88, b.WHITE, tracking=0.0)
    ancho_titulo = b.BOLD.width("QUÉ SE PUBLICA", 88, 0.0)
    body += b.BOLD.path("Y CUÁNDO", MARGEN + ancho_titulo + 26, 160, 88, b.YELLOW, tracking=0.0)

    # Resumen semanal a la derecha del título.
    x = W - MARGEN
    for numero, etiqueta in reversed(RESUMEN):
        ancho = max(b.BOLD.width(numero, 54, 0.0), b.SEMI.width(etiqueta, 18, 0.12)) + 28
        x -= ancho
        body += b.BOLD.path(numero, x + ancho / 2, 140, 54, b.YELLOW, tracking=0.0, anchor="middle")
        body += b.SEMI.path(etiqueta, x + ancho / 2, 166, 18, b.MIST, tracking=0.12, anchor="middle")
    body += b.SEMI.path("POR SEMANA", x - 24 - b.SEMI.width("POR SEMANA", 20, 0.16), 150, 20, b.MIST, tracking=0.16)

    # Rejilla de días.
    hueco = 18
    ancho_col = (W - 2 * MARGEN - 6 * hueco) / 7
    y_top = 222
    for i, (dia, piezas) in enumerate(DIAS):
        x = MARGEN + i * (ancho_col + hueco)
        body += b.BOLD.path(dia, x, y_top + 34, 40, b.WHITE, tracking=0.04)
        body += f'<rect x="{x}" y="{y_top + 48}" width="{ancho_col:.1f}" height="3" fill="{b.NAVY_SOFT}"/>'
        y = y_top + 68
        for hora, red, tipo, lineas in piezas:
            chip, alto = _chip(b, x, y, ancho_col, hora, red, tipo, lineas)
            body += chip
            y += alto + 14

    # Leyenda y orden de recorte.
    y_leg = H - 150
    body += f'<rect x="{MARGEN}" y="{y_leg - 36}" width="{W - 2 * MARGEN}" height="2" fill="{b.NAVY_SOFT}"/>'
    leyenda = [
        (b.YELLOW, b.YELLOW, "VIDEO LARGO EN YOUTUBE"),
        (GREEN, GREEN, "PODCAST Y EXPLICADOR"),
        ("none", b.YELLOW, "SHORT EN TRES REDES"),
        (b.NAVY_SOFT, b.NAVY_SOFT, "THREADS, LINKEDIN E INSTAGRAM"),
        ("none", b.MIST, "TAREA DE ELMER"),
    ]
    x = MARGEN
    for fondo, borde, texto in leyenda:
        body += f'<rect x="{x}" y="{y_leg - 16}" width="26" height="26" rx="6" fill="{fondo}" stroke="{borde}" stroke-width="3"/>'
        body += b.SEMI.path(texto, x + 40, y_leg + 5, 22, b.MIST, tracking=0.1)
        x += 40 + b.SEMI.width(texto, 22, 0.1) + 44
    body += b.SEMI.path(RECORTE, MARGEN, y_leg + 54, 24, b.WHITE, tracking=0.04)
    body += b.SEMI.path("LOS SHORTS DE YOUTUBE MANDAN AL VIDEO COMPLETO (VIDEO RELACIONADO EN STUDIO). EL SITIO SOLO CUANDO HAY PUENTE NATURAL.",
                        MARGEN, y_leg + 92, 24, b.MIST, tracking=0.04)

    # Firma.
    body += b.BOLD.path("EL INGENIERO", MARGEN, H - 28, 30, b.WHITE, tracking=0.04)
    ancho = b.BOLD.width("EL INGENIERO", 30, 0.04)
    body += b.BOLD.path("DE DATOS", MARGEN + ancho + 10, H - 28, 30, b.YELLOW, tracking=0.04)
    body += b.place((b.mark(), b.MARK_BOX), W - 110, H - 72, 110, 110)
    return b.svg(W, H, body)


def piezas(b) -> dict[str, str]:
    return {"calendario-semanal-v3-1920x1080": calendario(b)}
