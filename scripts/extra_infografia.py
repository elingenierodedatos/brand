"""Infografías de una sola lámina para redes (1080 × 1350).

Cada infografía es un titular, bloques numerados con encabezado y líneas de
cuerpo, y un cierre con la invitación al curso. El texto se parte a mano en
líneas para controlar los cortes. Un asterisco al inicio pinta la línea de
amarillo.

Para una infografía nueva, agrega una entrada a INFOGRAFIAS.
"""

W, H = 1080, 1350
MARGEN = 96

INFOGRAFIAS = {
    "python-en-60-segundos": {
        "etiqueta": "EXTRA  ·  ¿QUÉ ES PYTHON?",
        "titulo": ["PYTHON", "*EN 60 SEGUNDOS"],
        "bloques": [
            ("QUÉ ES", [
                "Un lenguaje de programación que se lee",
                "casi como inglés. Existe desde 1991 y hoy",
                "es el más común en datos e inteligencia artificial.",
            ]),
            ("PARA QUÉ SE USA EN DATOS", [
                "Automatizar tareas repetitivas.",
                "Limpiar y transformar archivos.",
                "Mover datos entre sistemas (pipelines).",
                "Analizar y entrenar modelos.",
            ]),
            ("POR QUÉ EMPEZAR AQUÍ", [
                "Pocas reglas y muchas librerías listas.",
                "Lo que aprendes en una semana",
                "ya resuelve problemas reales.",
            ]),
        ],
        "cierre": ["*CURSO GRATIS  ·  27 DE OCTUBRE", "elingenierodedatos.com"],
    },
    "flujo-de-datos-en-60-segundos": {
        "etiqueta": "EXTRA  ·  ¿QUÉ HACE UN INGENIERO DE DATOS?",
        "titulo": ["FLUJO DE DATOS", "*EN 60 SEGUNDOS"],
        "bloques": [
            ("EXTRAER", [
                "Los datos llegan como llegan: un CSV,",
                "una API, una base de datos. Nunca limpios.",
            ]),
            ("LIMPIAR", [
                "Corregir lo que se puede.",
                "Rechazar, con motivo, lo que no.",
                "Y dejar escrito por qué.",
            ]),
            ("CARGAR Y REPORTAR", [
                "Guardarlo donde se pueda consultar",
                "y sacar la respuesta que alguien necesita.",
                "Si nadie la usa, no era un flujo de datos.",
            ]),
        ],
        "cierre": ["*ESO ES EL PROYECTO FINAL DEL CURSO", "elingenierodedatos.com"],
    },
    "antes-de-entrar-a-datos": {
        "etiqueta": "EXTRA  ·  TRES ROLES, TRES TRABAJOS DISTINTOS",
        "titulo": ["ANTES DE", "*ENTRAR A DATOS"],
        "bloques": [
            ("ANALISTA DE DATOS", [
                "Responde preguntas del negocio con datos",
                "que ya existen. SQL, tableros, criterio.",
            ]),
            ("CIENTÍFICO DE DATOS", [
                "Busca patrones y predice.",
                "Estadística, modelos, Python.",
            ]),
            ("INGENIERO DE DATOS", [
                "Hace que los datos existan, lleguen limpios",
                "y a tiempo. Python, SQL y sistemas.",
            ]),
        ],
        "cierre": ["*PRIMERO EL ROL. LUEGO LAS BASES.", "Python y SQL sirven en los tres."],
    },
    "tres-cosas-que-no-necesitas": {
        "etiqueta": "EXTRA  ·  PARA EMPEZAR EN DATOS",
        "titulo": ["TRES COSAS QUE", "*NO NECESITAS"],
        "bloques": [
            ("UNA LAPTOP NUEVA", [
                "El curso corre en cualquier máquina",
                "con Windows, macOS o Linux.",
            ]),
            ("MATEMÁTICAS AVANZADAS", [
                "Necesitas leer un error completo",
                "y saber buscar. Eso se entrena.",
            ]),
            ("PAGAR", [
                "El curso es gratis y el código",
                "queda en tu GitHub, no en una plataforma.",
            ]),
        ],
        "cierre": ["*LO QUE SÍ: UNA HORA AL DÍA.", "elingenierodedatos.com"],
    },
}


def _firma(b):
    out = b.BOLD.path("EL INGENIERO", MARGEN, H - 72, 32, b.WHITE, tracking=0.04)
    ancho = b.BOLD.width("EL INGENIERO", 32, 0.04)
    out += b.BOLD.path("DE DATOS", MARGEN + ancho + 10, H - 72, 32, b.YELLOW, tracking=0.04)
    out += b.place((b.mark(), b.MARK_BOX), W - 120, H - 100, 120, 120)
    return out


def infografia(b, spec):
    body = b.background(W, H) + f'<rect width="18" height="{H}" fill="{b.YELLOW}"/>'
    body += b.SEMI.path(spec["etiqueta"], MARGEN, 110, 30, b.MIST, tracking=0.22)

    y = 200
    for linea in spec["titulo"]:
        texto = linea.lstrip("*")
        color = b.YELLOW if linea.startswith("*") else b.WHITE
        body += b.BOLD.path(texto, MARGEN, y, 104, color, tracking=0.0)
        y += 100

    # Centra los bloques en el espacio entre el titular y el cierre.
    altura = sum(44 + 10 + 40 * len(lineas) + 26 for _, lineas in spec["bloques"])
    disponible = (H - 180 - 70) - y
    y += max(0, (disponible - altura) / 2) - 2
    for indice, (encabezado, lineas) in enumerate(spec["bloques"], 1):
        body += f'<rect x="{MARGEN}" y="{y - 2}" width="{W - 2 * MARGEN}" height="2" fill="{b.NAVY_SOFT}"/>'
        y += 44
        body += b.BOLD.path(f"{indice:02d}", MARGEN, y, 40, b.YELLOW, tracking=0.02)
        body += b.BOLD.path(encabezado, MARGEN + 64, y, 40, b.WHITE, tracking=0.06)
        y += 10
        for linea in lineas:
            y += 40
            body += b.SEMI.path(linea, MARGEN, y, 36, b.MIST, tracking=0.01)
        y += 26

    y_cierre = H - 180
    body += f'<rect x="{MARGEN}" y="{y_cierre - 70}" width="{W - 2 * MARGEN}" height="2" fill="{b.NAVY_SOFT}"/>'
    for linea in spec["cierre"]:
        texto = linea.lstrip("*")
        if linea.startswith("*"):
            body += b.BOLD.path(texto, MARGEN, y_cierre, 52, b.YELLOW, tracking=0.06)
        else:
            body += b.SEMI.path(texto, MARGEN, y_cierre, 40, b.WHITE, tracking=0.02)
        y_cierre += 56
    body += _firma(b)
    return b.svg(W, H, body)


def piezas(b) -> dict[str, str]:
    return {f"infografia-{nombre}-1080x1350": infografia(b, spec) for nombre, spec in INFOGRAFIAS.items()}
