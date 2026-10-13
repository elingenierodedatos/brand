"""Piezas del curso Python básico: portada general y miniatura de cada lección.

Las miniaturas dejan libre el tercio derecho para colocar la foto del instructor
en Canva. Si no se pone foto, funcionan igual.
"""

CURSO = "PYTHON BÁSICO PARA INGENIERÍA DE DATOS"

# (número en pantalla, etiqueta, título en una o dos líneas)
LECCIONES = [
    ("00", "LECCIÓN 0", ("PREPARA", "TU COMPUTADORA")),
    ("01", "LECCIÓN 1", ("VARIABLES,", "TEXTO Y NÚMEROS")),
    ("02", "LECCIÓN 2", ("LISTAS", "Y BUCLES")),
    ("03", "LECCIÓN 3", ("DECISIONES", "CON IF Y WHILE")),
    ("04", "LECCIÓN 4", ("DICCIONARIOS", "Y CONJUNTOS")),
    ("05", "LECCIÓN 5", ("FUNCIONES", "Y MÓDULOS")),
    ("06", "LECCIÓN 6", ("ARCHIVOS", "Y ERRORES")),
    ("07", "LECCIÓN 7", ("PRUEBAS", "CON PYTEST")),
    ("08", "LECCIÓN 8", ("DATOS", "EN SQLITE")),
    ("09", "PROYECTO FINAL", ("FLUJO", "DE VENTAS")),
]


def _firma(b, w, h, u):
    """Nombre de la marca abajo a la izquierda e isotipo abajo a la derecha."""
    out = b.BOLD.path("EL INGENIERO", 64 * u, h - 56 * u, 30 * u, b.WHITE, tracking=0.04)
    ancho = b.BOLD.width("EL INGENIERO", 30 * u, 0.04)
    out += b.BOLD.path("DE DATOS", 64 * u + ancho + 10 * u, h - 56 * u, 30 * u, b.YELLOW, tracking=0.04)
    out += b.place((b.mark(), b.MARK_BOX), w - 110 * u, h - 90 * u, 130 * u, 130 * u)
    return out


def miniatura(b, numero, etiqueta, titulo, w=1280, h=720):
    u = h / 720
    body = b.background(w, h) + f'<rect width="{18 * u:.0f}" height="{h}" fill="{b.YELLOW}"/>'
    body += b.SEMI.path(f"{CURSO}  ·  {etiqueta}", 64 * u, 92 * u, 30 * u, b.MIST, tracking=0.22)
    body += b.BOLD.path(numero, 56 * u, 372 * u, 300 * u, b.YELLOW, tracking=-0.02)
    linea1, linea2 = titulo
    body += b.BOLD.path(linea1, 64 * u, 490 * u, 104 * u, b.WHITE, tracking=0.0)
    body += b.BOLD.path(linea2, 64 * u, 594 * u, 104 * u, b.WHITE, tracking=0.0)
    body += _firma(b, w, h, u)
    return b.svg(w, h, body)


def portada(b, w, h):
    """Portada general del curso: para la landing, la lista de YouTube y redes."""
    u = min(w / 1920, h / 1080)
    x = 96 * u
    body = b.background(w, h) + f'<rect width="{24 * u:.0f}" height="{h}" fill="{b.YELLOW}"/>'
    body += b.SEMI.path("CURSO GRATUITO  ·  EN ESPAÑOL", x, h * 0.20, 40 * u, b.YELLOW, tracking=0.28)
    size = 168 * u
    body += b.BOLD.path("PYTHON BÁSICO", x, h * 0.20 + 200 * u, size, b.WHITE, tracking=0.0)
    body += b.BOLD.path("PARA INGENIERÍA", x, h * 0.20 + 360 * u, size, b.WHITE, tracking=0.0)
    body += b.BOLD.path("DE DATOS", x, h * 0.20 + 520 * u, size, b.YELLOW, tracking=0.0)
    body += b.SEMI.path("Aprende Python desde cero limpiando datos reales.", x, h * 0.20 + 630 * u,
                        54 * u, b.MIST, tracking=0.01)
    body += b.SEMI.path("9 LECCIONES  ·  1 PROYECTO  ·  470 PRUEBAS", x, h * 0.20 + 712 * u,
                        34 * u, b.MIST, tracking=0.22)
    body += _firma(b, w, h, u * 1.5)
    return b.svg(w, h, body)


def piezas(b) -> dict[str, str]:
    salida = {
        "curso-python-portada-1920x1080": portada(b, 1920, 1080),
        "curso-python-og-1200x630": portada(b, 1200, 630),
    }
    for numero, etiqueta, titulo in LECCIONES:
        salida[f"curso-python-miniatura-{numero}-1280x720"] = miniatura(b, numero, etiqueta, titulo)
    return salida
