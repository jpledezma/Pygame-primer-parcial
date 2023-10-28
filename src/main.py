import pygame
from pygame.locals import *
from config import *
from creacion_elementos import *
from dibujar_elementos import *


pygame.init()

CLOCK = pygame.time.Clock()

pantalla = pygame.display.set_mode(TAMAÑO_PANTALLA)


def terminar():
    pygame.quit()
    exit()


img_fondo = pygame.image.load("assets/paisaje-1.jpg")

fuente = pygame.font.SysFont("serif", 26)

button = crear_boton((300, 300), "Once, the lord of light banished dark...", BURDEOS, OSCURO, fuente, True, 10, img_fondo)

# Colisiones pygame

is_running = True

while is_running:
    CLOCK.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        
        
# ---> actualizar los elementos    



# ---> Dibujar la pantalla
    pantalla.fill(GRIS_OSCURO)

    blitear_boton(pantalla, button)

# ---> actualizar pantalla

    # con flip se actualiza/dibuja toda la pantalla
    pygame.display.flip()




pygame.quit()