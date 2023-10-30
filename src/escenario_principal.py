import pygame
from pygame.locals import *
from creacion_elementos import *
from dibujar_elementos import *
from config import *
from calculos import *
from utilidades import *
from menus import *

# ------------------  Menu Principal  ------------------
def escenario_juego(pantalla:pygame.Surface):

    global musica_activa

    CLOCK = pygame.time.Clock()

    contador_segundos = 0
    contador_ticks = FPS
    duracion_frame_animacion = FPS // 4
    contador_animaciones = duracion_frame_animacion
    frame_animacion_seleccionada = 0

    ancho_pantalla = pantalla.get_width()
    alto_pantalla = pantalla.get_height()

    altura_hud = 100

    

    limite_superior = altura_hud + 110
    limite_inferior = alto_pantalla - 25
    limite_izquierdo = 5
    limite_derecho = ancho_pantalla - 5

    # Background
    fondo_escenario = pygame.image.load("assets/backgrounds/main-background.jpg")
    fondo_escenario = pygame.transform.scale(fondo_escenario, (ancho_pantalla, alto_pantalla - altura_hud))
    # HUD
    fondo_hud = pygame.image.load("assets/backgrounds/hud-background.jpg")
    fondo_hud = pygame.transform.scale(fondo_hud, (ancho_pantalla, altura_hud))
    # Texto segundos
    texto_contador_segundos = escribir_texto((0, 0), f"{contador_segundos:03}", AMARILLO)
    texto_contador_segundos['rect'].center = (ancho_pantalla //2, altura_hud // 2)
    
    print(musica_activa)
    # Música del juego
    pygame.mixer.music.load("assets\musica\OurLordIsNotReady.mp3")
    if musica_activa:
        pygame.mixer.music.play(start=0, loops=-1)
    

    # Personaje principal
    img_personaje = pygame.image.load("assets/sprites/personaje/knight_idle_0.png")
    personaje = crear_entidad((0, 0), 90, 70, 200, 20, 100, 50, imagen=img_personaje)
    personaje['rect'].center = (ancho_pantalla / 2, alto_pantalla - 50)
    personaje['velocidad'] = 1
    personaje['hitbox'].width = personaje['rect'].width // 2 

    pj_mover_arriba = False
    pj_mover_abajo = False
    pj_mover_derecha = False
    pj_mover_izquierda = False

    

    # Animaciones
    animaciones = {'quieto': [], 'moviendo_arriba':[], 'moviendo_abajo':[], 'moviendo_izquierda':[], 'moviendo_derecha':[]}
    for i in range(4):
        animaciones['quieto'].append(crear_superficie((0, 0), 90, 70, imagen=pygame.image.load(f"assets/sprites/personaje/knight_idle_{i}.png")))
        animaciones['moviendo_abajo'].append(crear_superficie((0, 0), 90, 70, imagen=pygame.image.load(f"assets/sprites/personaje/knight_run_down_{i}.png")))
        animaciones['moviendo_arriba'].append(crear_superficie((0, 0), 90, 70, imagen=pygame.image.load(f"assets/sprites/personaje/knight_run_up_{i}.png")))
        animaciones['moviendo_izquierda'].append(crear_superficie((0, 0), 90, 70, imagen=pygame.image.load(f"assets/sprites/personaje/knight_run_left_{i}.png")))
        animaciones['moviendo_derecha'].append(crear_superficie((0, 0), 90, 70, imagen=pygame.image.load(f"assets/sprites/personaje/knight_run_right_{i}.png")))

    movimiento_animacion_seleccionada = 'quieto'

    # Enemigos
    img_zombie = img_personaje = pygame.image.load("assets/sprites/enemigos/zombie.png")
    zombie = crear_entidad((400, 400), 75, 100, 100, 10, imagen=img_zombie)
    img_esqueleto = img_personaje = pygame.image.load("assets/sprites/enemigos/skeleton.png")
    esqueleto = crear_entidad((500, 400), 70, 100, 100, 10, imagen=img_esqueleto)

    enemigos = [zombie, esqueleto]

    entidades = [personaje, zombie, esqueleto]

    i = 0
    # Loop del juego
    while True:
        CLOCK.tick(FPS)
        for evento in pygame.event.get():
            if evento.type == QUIT:
                terminar_juego()

            if evento.type == KEYDOWN:
                if evento.key == K_p or evento.key == K_ESCAPE:
                    print("pausa")
                    menu_opciones(pantalla)
                    
                if evento.key == K_w:
                    pj_mover_arriba = True
                if evento.key == K_a:
                    pj_mover_izquierda = True
                if evento.key == K_s:
                    pj_mover_abajo = True
                if evento.key == K_d:
                    pj_mover_derecha = True

                if evento.key == K_LSHIFT:
                    personaje['velocidad'] = 2

            if evento.type == KEYUP:
                if evento.key == K_w:
                    pj_mover_arriba = False
                if evento.key == K_a:
                    pj_mover_izquierda = False
                if evento.key == K_s:
                    pj_mover_abajo = False
                if evento.key == K_d:
                    pj_mover_derecha = False

                if evento.key == K_LSHIFT:
                    personaje['velocidad'] = 1
                
        

        if pj_mover_izquierda and personaje["rect"].left > limite_izquierdo:
            personaje["rect"].centerx -= personaje['velocidad']
            movimiento_animacion_seleccionada = 'moviendo_izquierda'

        if pj_mover_derecha and personaje["rect"].right < limite_derecho:
            personaje["rect"].centerx += personaje['velocidad']
            movimiento_animacion_seleccionada = 'moviendo_derecha'

        if not (pj_mover_izquierda or pj_mover_derecha or pj_mover_arriba or pj_mover_abajo):
            movimiento_animacion_seleccionada = 'quieto'

        if pj_mover_arriba and personaje["rect"].top > limite_superior:
            personaje["rect"].centery -= personaje['velocidad']
            movimiento_animacion_seleccionada = 'moviendo_arriba'

        if pj_mover_abajo and personaje["rect"].bottom < limite_inferior:
            personaje["rect"].centery += personaje['velocidad']
            movimiento_animacion_seleccionada = 'moviendo_abajo'






        pantalla.blit(fondo_escenario, (0, altura_hud))
        pantalla.blit(fondo_hud, (0, 0))

        

        contador_ticks -= 1
        if contador_ticks == 0:
            contador_segundos += 1
            print(contador_segundos)
            contador_ticks = FPS
            texto_contador_segundos = escribir_texto((0, 0), f"{contador_segundos:03}", AMARILLO)
            texto_contador_segundos['rect'].center = (ancho_pantalla //2, altura_hud // 2)

        contador_animaciones -= 1
        if contador_animaciones == 0:
            contador_animaciones = duracion_frame_animacion
            frame_animacion_seleccionada += 1
        if frame_animacion_seleccionada > 3:
            frame_animacion_seleccionada = 0


        # Movimiento enemigos
        for enemigo in enemigos:
            if calcular_distancia(enemigo['rect'].center, personaje['rect'].center) <= enemigo['radio_deteccion']:
                enemigo['agresivo'] = True
                # print(calcular_distancia(enemigo['rect'].center, personaje['rect'].center))

        for enemigo in enemigos:
            if enemigo['agresivo']:
                if enemigo['rect'].centery > personaje['rect'].centery:
                    enemigo['rect'].centery -= enemigo['velocidad']
                else:
                    enemigo['rect'].centery += enemigo['velocidad']
                if enemigo['rect'].centerx > personaje['rect'].centerx:
                    enemigo['rect'].centerx -= enemigo['velocidad']
                else:
                    enemigo['rect'].centerx += enemigo['velocidad']

                if calcular_distancia(enemigo['rect'].center, personaje['rect'].center) > enemigo['radio_deteccion'] * 3:
                    enemigo['agresivo'] = False


        for entidad in entidades:
            entidad['hitbox'].bottom = entidad['rect'].bottom
            entidad['hitbox'].centerx = entidad['rect'].centerx

        blitear_superficie(pantalla, zombie)
        blitear_superficie(pantalla, esqueleto)

        pantalla.blit(animaciones[movimiento_animacion_seleccionada][frame_animacion_seleccionada]['superficie'], personaje['rect'])

        pygame.draw.rect(pantalla, BLANCO, zombie['rect'], 1)
        pygame.draw.rect(pantalla, BLANCO, esqueleto['rect'], 1)
        pygame.draw.rect(pantalla, BLANCO, zombie['hitbox'], 1)
        pygame.draw.rect(pantalla, BLANCO, esqueleto['hitbox'], 1)

        pygame.draw.rect(pantalla, ROJO, personaje['hitbox'], 1)
        # pygame.draw.rect(pantalla, BLANCO, personaje['rect'], 1)

        blitear_texto(pantalla, texto_contador_segundos)

        i += 1
        if i > 3:
            i = 0

        pygame.display.flip()

# escenario_juego(pygame.display.set_mode(TAMAÑO_PANTALLA))

# TODO 
# agregar barra de vida, barra de stamina/energia y enemigos
# agregar menu de pausa
# agregar eventos personalizados (que aparezca una bruja cada cierto tiempo, hasta 3 veces)     
# agregar iframes