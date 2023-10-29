from pygame import font, image

font.init() 

ANCHO = 1200
ALTO = 800
TAMAÑO_PANTALLA = (ANCHO, ALTO)
FPS = 120

ROJO = (217, 4, 41)
VERDE = (0, 128, 0)
AZUL = (0, 80, 157)
AMARILLO = (255, 210, 39)
NARANJA = (201, 115, 10)
AQUA = (68, 255, 209)
CELESTE = (0, 168, 232)
VIOLETA = (90, 24, 154)
BURDEOS = (102, 7, 8)
GRIS_OSCURO = (61, 61, 61)
GRIS_CLARO = (211, 211, 211)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
OSCURO = (25, 25, 25)

TITULO = "In Tenebris"

# FUENTE_DEFAULT = font.SysFont("serif", 30)
FUENTE_DEFAULT = font.Font("assets/fuentes/ENDOR___.ttf", 30)

FONDO_PRINCIPAL = image.load("assets/paisaje-1.jpg")

musica_activa = True
volumen_general = 1