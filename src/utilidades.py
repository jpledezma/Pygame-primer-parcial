import pygame
from pygame.locals import *
from creacion_elementos import *
from dibujar_elementos import *
from config import *

def terminar_juego():
    pygame.quit()
    exit()

def hover(rect:pygame.Rect, punto:tuple[int, int]) -> bool:
    if rect.collidepoint(punto):
        return True
    return False


def menu_principal(pantalla:pygame.Surface):
    ancho_pantalla = pantalla.get_width()
    alto_pantalla = pantalla.get_height()
    centro_pantalla = (ancho_pantalla//2, alto_pantalla//2)

    fondo_menu = pygame.image.load("assets/main-menu-background.jpg")
    fondo_menu = pygame.transform.scale(fondo_menu, (ancho_pantalla, alto_pantalla))

    btn_iniciar = crear_boton((centro_pantalla), "Iniciar", BLANCO, ROJO, espaciado_y=10, espaciado_x=40)
    btn_iniciar['rect_superficie'].center = centro_pantalla
    btn_iniciar['rect_texto'].center = centro_pantalla

    while True:
        for evento in pygame.event.get():
            if evento.type == QUIT:
                terminar_juego()
                
            if btn_iniciar['rect_superficie'].collidepoint(pygame.mouse.get_pos()):
                btn_iniciar['fondo'].fill(VERDE)
                if evento.type == MOUSEBUTTONDOWN:
                    print("Iniciar")
                    return
            else:
                btn_iniciar['fondo'].fill(ROJO)

        pantalla.blit(fondo_menu, (0, 0))
        blitear_boton(pantalla, btn_iniciar)

        pygame.display.flip()