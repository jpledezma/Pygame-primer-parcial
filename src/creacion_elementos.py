import pygame
from pygame import Rect, Surface
from pygame.font import Font
from config import FUENTE_DEFAULT

pygame.font.init()
# Rectángulo
def crear_rectangulo(origen:tuple[int, int], 
                     ancho:int, 
                     alto:int, 
                     color:tuple[int, int, int], 
                     ancho_borde:int=-1, 
                     radio_borde:int=0
                    ) -> dict:
    
    rectangulo = Rect(*origen, ancho, alto)

    bloque_rectangulo = {'rect': rectangulo,
                  'color': color,
                  'ancho_borde':ancho_borde,
                  'radio_borde': radio_borde
                 }
    
    return bloque_rectangulo

# Texto
def escribir_texto(origen:tuple[int, int], 
                   texto:str, 
                   color_texto:tuple[int, int, int],
                   fuente:pygame.font.Font = FUENTE_DEFAULT,
                   antialias:bool = True,
                  ) -> dict:
    
    superficie_texto = fuente.render(texto, antialias, color_texto)
    rectangulo_texto = superficie_texto.get_rect()
    rectangulo_texto = Rect(*origen, rectangulo_texto.width, rectangulo_texto.height)

    bloque_texto = {'superficie':superficie_texto, 'rect':rectangulo_texto}

    return bloque_texto

# Superficie
def crear_superficie(origen:tuple[int, int],
                     ancho:int,
                     alto:int,
                     color:tuple[int, int, int],
                     imagen:Surface | None = None
                    ) -> dict:
    
    if imagen:
        superficie = pygame.transform.scale(imagen, (ancho, alto))
        
    else:
        superficie = Surface((ancho, alto))
        superficie.fill(color)

    rectangulo_superficie = Rect(*origen, ancho, alto)

    bloque_superficie = {'origen':origen,
                         'superficie':superficie,
                         'rect':rectangulo_superficie,
                         'imagen':imagen
                        }

    return bloque_superficie

# Botón
def crear_boton(origen:tuple[int, int],
                texto:str,
                color_texto:tuple[int, int, int] = (255, 255, 255),
                color_fondo:tuple[int, int, int] = (0, 0, 0),
                fuente:pygame.font.Font = FUENTE_DEFAULT,
                antialias:bool = True,
                espaciado_x:int = 0,
                espaciado_y:int = 0,
                imagen:Surface | None = None
               ):
    
    btn_texto = escribir_texto((0, 0),texto, color_texto, fuente, antialias)
    rect_texto:Rect = btn_texto['rect']

    btn_superficie = crear_superficie(origen,
                                      rect_texto.width + espaciado_x,
                                      rect_texto.height + espaciado_y,
                                      color_fondo,
                                      imagen)
    
    rect_superficie = btn_superficie['rect']

    rect_texto.center = rect_superficie.center

    
    bloque_boton = {'fondo':btn_superficie['superficie'],
                    'rect_superficie':rect_superficie,
                    'texto':btn_texto['superficie'],
                    'rect_texto':rect_texto,
                   }

    return bloque_boton

# TODO: validar datos