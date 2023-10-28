import pygame
from pygame.locals import *
from config import *
from creacion_elementos import *
from dibujar_elementos import *
from utilidades import *


pygame.init()

CLOCK = pygame.time.Clock()

pantalla = pygame.display.set_mode(TAMAÑO_PANTALLA)





img_fondo = FONDO_PRINCIPAL

fuente = pygame.font.SysFont("Arial", 26)

button = crear_boton((300, 300), "Once, the lord of light banished dark...", BURDEOS, OSCURO, fuente, True, 10, imagen=img_fondo)

sup = crear_superficie((400, 50), 50, 100, AMARILLO)

txt = escribir_texto((50, 50),"asdfghjkl", NEGRO)

menu_principal(pantalla)



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

    blitear_texto(pantalla, txt)
    blitear_superficie(pantalla, sup)
# ---> actualizar pantalla

    # con flip se actualiza/dibuja toda la pantalla
    pygame.display.flip()




pygame.quit()