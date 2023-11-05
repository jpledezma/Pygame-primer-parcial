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
                     ancho_borde:int=0, 
                     radio_borde:int=-1
                    ) -> dict:
    """ Crear un rectangulo y guardar sus propiedades en un diccionario

    Args:
        origen (tuple[int, int]): Coordenada de la esquina superior izquierda
        ancho (int): Ancho del rectangulo
        alto (int): Altura del rectangulo
        color (tuple[int, int, int]): Color del rectangulo
        ancho_borde (int, optional): Ancho del borde del rectangulo. Defaults to 0.
        radio_borde (int, optional): Radio de las esquinas del rectangulo. Defaults to -1.

    Returns:
        dict: Diccionario que contiene las propiedades del rectangulo
    """
    
    rectangulo = Rect(*origen, ancho, alto)

    bloque_rectangulo = {'rect': rectangulo,
                  'color': color,
                  'ancho_borde':ancho_borde,
                  'radio_borde': radio_borde
                 }
    
    return bloque_rectangulo

def crear_circulo(centro:tuple, 
                  radio:int, 
                  color:tuple, 
                  ancho_borde:int=0) -> dict:
    """ Crear un circulo y guardar sus propiedades en un diccionario

    Args:
        centro (tuple): Centro del circulo
        radio (int): Radio del circulo
        color (tuple): Color del circulo
        ancho_borde (int, optional): Ancho del borde del circulo. Defaults to 0.

    Returns:
        dict: Diccionario que contiene las propiedades del circulo
    """
    
    circulo = {'tipo': "circulo",
                'centro': list(centro), # Se convierte a list para poder modificar su valor
                'radio': radio,
                'color': color,
                'ancho_borde':ancho_borde }
    
    return circulo

# Texto
def escribir_texto(origen:tuple[int, int], 
                   texto:str, 
                   color_texto:tuple[int, int, int],
                   fuente:pygame.font.Font = FUENTE_DEFAULT,
                   antialias:bool = True,
                  ) -> dict:
    """Crear una superficie a partir de un texto y guardar sus propiedades en un diccionario

    Args:
        origen (tuple[int, int]): Coordenada de la esquina superior izquierda
        texto (str): Texto
        color_texto (tuple[int, int, int]): Color del texto
        fuente (pygame.font.Font, optional): Fuente del texto. Defaults to FUENTE_DEFAULT.
        antialias (bool, optional): Antialiasing. Defaults to True.

    Returns:
        dict: Diccionario que contiene las propiedades de la superficie del texto
    """
    
    # Crear la superficie del texto
    superficie_texto = fuente.render(texto, antialias, color_texto)
    # Obtener las dimensiones de la superficie creada
    rectangulo_texto = superficie_texto.get_rect()
    # Establecer la coordenada de origen del rectangulo de la superficie
    rectangulo_texto = Rect(*origen, rectangulo_texto.width, rectangulo_texto.height)

    bloque_texto = {'superficie':superficie_texto, 'rect':rectangulo_texto}

    return bloque_texto

# Superficie
def crear_superficie(origen:tuple[int, int],
                     ancho:int,
                     alto:int,
                     color:tuple[int, int, int] = (0, 0, 0),
                     imagen:Surface | None = None
                    ) -> dict:
    """Crear una superficie

    Args:
        origen (tuple[int, int]): Coordenada de la esquina superior izquierda
        ancho (int): Ancho de la superficie
        alto (int): Altura de la superficie
        color (tuple[int, int, int], optional): Color de la superficie. Defaults to (0, 0, 0).
        imagen (Surface | None, optional): Imagen de la superficie. Defaults to None.

    Returns:
        dict: Diccionario que contiene las propiedades de la superficie
    """
    
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
               ) -> dict:
    """Crear la superficie de un texto y la suporficie de su fondo/background

    Args:
        origen (tuple[int, int]): Coordenada de la esquina superior izquierda
        texto (str): Texto del botón
        color_texto (tuple[int, int, int], optional): Color del texto. Defaults to (255, 255, 255).
        color_fondo (tuple[int, int, int], optional): Color del botón. Defaults to (0, 0, 0).
        fuente (pygame.font.Font, optional): Fuente del texto. Defaults to FUENTE_DEFAULT.
        antialias (bool, optional): Antialiasing. Defaults to True.
        espaciado_x (int, optional): Espaciado horizontal. Defaults to 0.
        espaciado_y (int, optional): Espaciado vertical. Defaults to 0.
        imagen (Surface | None, optional): Imagen del boton. Defaults to None.

    Returns:
        dict: Diccionario que contiene las propiedades del boton
    """
    
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

# Entidades
def crear_entidad(origen:tuple[int, int],
                  ancho:int,
                  alto:int,
                  vida:int,
                  poder_ataque:int = 0,
                  energia:int = 0,
                  mana:int = 0,
                  velocidad:int = 1,
                  radio_deteccion:int = 150,
                  color:tuple[int, int, int] = (0, 0, 0),
                  iframes:int = 0,
                  vulnerable:bool = True,
                  imagen:Surface | None = None
                 ) -> dict:
    """ Crear una superficie y agregarle propiedades especiales"""
    entidad = crear_superficie(origen, ancho, alto, color, imagen)
    hitbox = Rect(*origen, ancho // 1.5, alto // 2)
    hitbox.bottom = entidad['rect'].bottom
    hitbox.centerx = entidad['rect'].centerx

    entidad['vida'] = vida
    entidad['poder_ataque'] = poder_ataque
    entidad['energia'] = energia
    entidad['mana'] = mana
    entidad['velocidad'] = velocidad
    entidad['hitbox'] = hitbox
    entidad['agresivo'] = False
    entidad['radio_deteccion'] = radio_deteccion
    entidad['iframes'] = iframes
    entidad['cd_iframes'] = iframes
    entidad['vulnerable'] = vulnerable

    return entidad
