import pygame
from config import TITULO, FPS, TAMAÑO_PANTALLA
from utilidades import terminar_juego
from menus import menu_principal
from escenario_principal import escenario_juego


pygame.init()

CLOCK = pygame.time.Clock()

pantalla = pygame.display.set_mode(TAMAÑO_PANTALLA)

musica_activa, volumen_musica, volumen_efectos = (True, 1, 1)

pygame.display.set_caption(TITULO)


is_running = True

while is_running:
    
    CLOCK.tick(FPS)

    musica_activa, volumen_musica, volumen_efectos = menu_principal(pantalla, musica_activa, volumen_musica, volumen_efectos)
    musica_activa, volumen_musica, volumen_efectos = escenario_juego(pantalla, musica_activa, volumen_musica, volumen_efectos)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        
    pygame.display.flip()

terminar_juego()
