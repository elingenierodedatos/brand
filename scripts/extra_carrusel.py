"""Carruseles y tarjetas de texto para Instagram, Threads y LinkedIn.

Cada lámina mide 1080 × 1350 (4:5). El texto se parte en líneas a mano, en
LAMINAS, porque así se controla dónde corta cada frase. Una línea en mayúsculas
sale en Bold y grande (titular); las demás salen en SemiBold (cuerpo). Un
asterisco al inicio de una línea la pinta de amarillo.

Para un carrusel nuevo, agrega una entrada a CARRUSELES con su nombre y láminas.
"""

W, H = 1080, 1350
MARGEN = 96

# nombre del carrusel: lista de láminas; cada lámina es una lista de líneas.
CARRUSELES = {
    "curso-python-archivo-real": [
        ["HAY CIENTOS", "DE CURSOS", "DE PYTHON.", "*HICE OTRO."],
        ["EL PROBLEMA", "Mucha teoría, poca práctica.", "", "Un CSV limpio en el tutorial.", "Bases transaccionales, APIs y", "varios sistemas en la vida real."],
        ["EL CURSO TAMBIÉN", "EMPIEZA CON UN CSV.", "*PERO SUCIO.", "", "63 pedidos de una tienda", "tal como llegan."],
        ["LO QUE TRAE ADENTRO", "Precios con símbolo y comas.", "Fechas en dos formatos.", "Ciudades escritas de varias maneras.", "Pedidos duplicados."],
        ["LO QUE HACES CON ESO", "Lo que no se puede corregir", "se rechaza con motivo.", "", "Lo demás se carga a SQLite", "y sale en un reporte."],
        ["*475 PRUEBAS", "CALIFICAN CADA PASO.", "", "Corren en tu máquina", "y en GitHub, en cada push.", "El código pasa o no pasa."],
        ["GRATIS.", "*27 DE OCTUBRE.", "", "elingenierodedatos.com"],
    ],
}


def _firma(b, u):
    out = b.BOLD.path("EL INGENIERO", MARGEN, H - 72 * u, 32 * u, b.WHITE, tracking=0.04)
    ancho = b.BOLD.width("EL INGENIERO", 32 * u, 0.04)
    out += b.BOLD.path("DE DATOS", MARGEN + ancho + 10 * u, H - 72 * u, 32 * u, b.YELLOW, tracking=0.04)
    out += b.place((b.mark(), b.MARK_BOX), W - 120 * u, H - 100 * u, 120 * u, 120 * u)
    return out


def lamina(b, lineas, indice, total):
    u = 1.0
    body = b.background(W, H) + f'<rect width="18" height="{H}" fill="{b.YELLOW}"/>'
    body += b.SEMI.path(f"{indice} / {total}", W - MARGEN, 110, 30, b.MIST, tracking=0.22, anchor="end")
    # Altura total del bloque de texto, para centrarlo verticalmente.
    altos = []
    for linea in lineas:
        texto = linea.lstrip("*")
        if texto == "":
            altos.append(40)
        elif texto.isupper():
            altos.append(118)
        else:
            altos.append(74)
    y = (H - sum(altos)) / 2 + 20
    for linea, alto in zip(lineas, altos):
        texto = linea.lstrip("*")
        color = b.YELLOW if linea.startswith("*") else b.WHITE
        if texto == "":
            y += alto
            continue
        y += alto
        if texto.isupper():
            body += b.BOLD.path(texto, MARGEN, y - 22, 104, color, tracking=0.0)
        else:
            body += b.SEMI.path(texto, MARGEN, y - 16, 56, color if color == b.YELLOW else b.MIST, tracking=0.01)
    body += _firma(b, u)
    return b.svg(W, H, body)


def piezas(b) -> dict[str, str]:
    salida = {}
    for nombre, laminas in CARRUSELES.items():
        for i, lineas in enumerate(laminas, 1):
            salida[f"carrusel-{nombre}-{i:02d}-1080x1350"] = lamina(b, lineas, i, len(laminas))
    return salida
