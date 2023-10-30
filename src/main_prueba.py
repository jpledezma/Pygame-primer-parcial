import pygame
from pygame.locals import *
from config import *
from creacion_elementos import *
from dibujar_elementos import *
from utilidades import terminar_juego
from menus import *


pygame.init()

CLOCK = pygame.time.Clock()

pantalla = pygame.display.set_mode(TAMAÑO_PANTALLA)


pygame.display.set_caption(TITULO)


img_fondo = FONDO_PRINCIPAL

fuente = pygame.font.Font("assets/fuentes/ENDOR___.ttf", 30)

button = crear_boton((300, 300), "Once, the lord of light banished dark...", BURDEOS, OSCURO, fuente, True, 10, imagen=img_fondo)

sup = crear_superficie((400, 50), 50, 100, AMARILLO)

txt = escribir_texto((50, 50),"asdfghjkl", NEGRO)

# menu_principal(pantalla)
pj_mover_arriba = False
pj_mover_abajo = False
pj_mover_derecha = False
pj_mover_izquierda = False

rectangulo = crear_rectangulo((300, 300), 50, 50, VERDE)


fondo_escenario = pygame.image.load("assets/backgrounds/main-background.jpg")
fondo_escenario = pygame.transform.scale(fondo_escenario, (ANCHO, ALTO - 100))

hud = pygame.image.load("assets/backgrounds/hud-background.jpg")
hud = pygame.transform.scale(hud, (ANCHO, 100))

pygame.mixer.music.load("assets\musica\OurLordIsNotReady.mp3")
pygame.mixer.music.play(start=0, loops=-1)

vel_rectangulo = 1


limite_superior = 10
limite_inferior = ALTO - 25
limite_izquierdo = 5
limite_derecho = ANCHO - 5

is_running = True

while is_running:
    
    CLOCK.tick(FPS)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            is_running = False

        if evento.type == KEYDOWN:
            if evento.key == K_p:
                print("pausa")
            if evento.key == K_w:
                pj_mover_arriba = True
            if evento.key == K_a:
                pj_mover_izquierda = True
            if evento.key == K_s:
                pj_mover_abajo = True
            if evento.key == K_d:
                pj_mover_derecha = True

        if evento.type == KEYUP:
            if evento.key == K_w:
                pj_mover_arriba = False
            if evento.key == K_a:
                pj_mover_izquierda = False
            if evento.key == K_s:
                pj_mover_abajo = False
            if evento.key == K_d:
                pj_mover_derecha = False
        
        
# ---> actualizar los elementos    
    if pj_mover_arriba and rectangulo["rect"].top > limite_superior:
        rectangulo["rect"].centery -= vel_rectangulo
    if pj_mover_abajo and rectangulo["rect"].bottom < limite_inferior:
        rectangulo["rect"].centery += vel_rectangulo
    if pj_mover_izquierda and rectangulo["rect"].left > limite_izquierdo:
        rectangulo["rect"].centerx -= vel_rectangulo
    if pj_mover_derecha and rectangulo["rect"].right < limite_derecho:
        rectangulo["rect"].centerx += vel_rectangulo


# ---> Dibujar la pantalla
    pantalla.blit(fondo_escenario, (0, 100))
    pantalla.blit(hud, (0, 0))

    blitear_boton(pantalla, button)

    blitear_texto(pantalla, txt)
    blitear_superficie(pantalla, sup)

    dibujar_rectangulo(pantalla, rectangulo)
# ---> actualizar pantalla

    # con flip se actualiza/dibuja toda la pantalla
    pygame.display.flip()




pygame.quit()