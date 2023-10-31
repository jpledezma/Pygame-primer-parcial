import pygame
from pygame.locals import *
from config import *
from creacion_elementos import *
from dibujar_elementos import *
from utilidades import terminar_juego
from menus import *
from escenario_principal import *


pygame.init()

CLOCK = pygame.time.Clock()

pantalla = pygame.display.set_mode(TAMAÑO_PANTALLA)


pygame.display.set_caption(TITULO)


is_running = True

while is_running:
    
    CLOCK.tick(FPS)

    menu_principal(pantalla)
    escenario_juego(pantalla)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        
    pygame.display.flip()

terminar_juego()
