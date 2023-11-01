import pygame
from pygame.locals import *
from creacion_elementos import *
from dibujar_elementos import *
from config import *
from calculos import *
from utilidades import *
from menus import *
from random import randint

# ------------------  Menu Principal  ------------------
def escenario_juego(pantalla:pygame.Surface):

    global musica_activa

    # Control de tiempo
    CLOCK = pygame.time.Clock()

    temporizador = 200
    contador_ticks = FPS
    duracion_frame_animacion = FPS // 4
    contador_animaciones = duracion_frame_animacion
    frame_animacion_seleccionada = 0

    # Dimensiones
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

    fondo_barra_vida = crear_rectangulo((60, altura_hud // 4 - 7), 300, altura_hud // 7, DORADO, radio_borde=10)
    barra_vida = crear_rectangulo((0, 0), fondo_barra_vida['rect'].width - 10, fondo_barra_vida['rect'].height - 6, ROJO)

    fondo_barra_mana = crear_rectangulo((60, altura_hud // 2 - 7), 300, altura_hud // 7, DORADO, radio_borde=10)
    barra_mana = crear_rectangulo((0, 0), fondo_barra_mana['rect'].width - 10, fondo_barra_mana['rect'].height - 6, AZUL)

    fondo_barra_energia = crear_rectangulo((60, altura_hud // 4 * 3 - 7), 300, altura_hud // 7, DORADO, radio_borde=10)
    barra_energia = crear_rectangulo((0, 0), fondo_barra_energia['rect'].width - 10, fondo_barra_energia['rect'].height - 6, VERDE)

    # Texto segundos
    texto_contador_segundos = escribir_texto((0, 0), f"{temporizador:03}", AMARILLO)
    texto_contador_segundos['rect'].center = (ancho_pantalla //2, altura_hud // 2)

    # Contador enemigos derrotados
    enemigos_derrotados = 0
    texto_contador_enemigos = escribir_texto((0, 0), f"Enemigos derrotados: {enemigos_derrotados:02}", AMARILLO)
    texto_contador_enemigos['rect'].center = (ancho_pantalla // 4 * 3, altura_hud // 2)
    # Música del juego
    pygame.mixer.music.load("assets\musica\OurLordIsNotReady.mp3")
    if musica_activa:
        pygame.mixer.music.play(start=0, loops=-1)
    

    # Personaje principal
    # Atributos
    multiplicador_sprint = 1
    pj_vida_maxima = 200
    pj_mana_maxima = 100
    pj_energia_maxima = FPS * 3
    pj_vulnerable = True
    pj_dañado = False
    iframes = FPS #// 2
    cooldown_iframes = iframes
    pj_daño_recibido = 0
    # Imagen
    img_personaje = pygame.image.load("assets/sprites/personaje/knight_idle_0.png")
    personaje = crear_entidad((0, 0), 90, 70, vida=pj_vida_maxima, poder_ataque=20, mana=pj_mana_maxima, energia=pj_energia_maxima, imagen=img_personaje)
    personaje['rect'].center = (ancho_pantalla / 2, alto_pantalla - 50)
    personaje['velocidad'] = 1
    personaje['hitbox'].width = personaje['rect'].width // 2 
    # Movimiento personaje
    pj_mover_arriba = False
    pj_mover_abajo = False
    pj_mover_derecha = False
    pj_mover_izquierda = False
    pj_sprint = False
    # Animaciones
    animaciones = {'quieto': [], 'moviendo_arriba':[], 'moviendo_abajo':[], 'moviendo_izquierda':[], 'moviendo_derecha':[]}
    for i in range(4):
        animaciones['quieto'].append(crear_superficie((0, 0), 90, 70, imagen=pygame.image.load(f"assets/sprites/personaje/knight_idle_{i}.png")))
        animaciones['moviendo_abajo'].append(crear_superficie((0, 0), 90, 70, imagen=pygame.image.load(f"assets/sprites/personaje/knight_run_down_{i}.png")))
        animaciones['moviendo_arriba'].append(crear_superficie((0, 0), 90, 70, imagen=pygame.image.load(f"assets/sprites/personaje/knight_run_up_{i}.png")))
        animaciones['moviendo_izquierda'].append(crear_superficie((0, 0), 90, 70, imagen=pygame.image.load(f"assets/sprites/personaje/knight_run_left_{i}.png")))
        animaciones['moviendo_derecha'].append(crear_superficie((0, 0), 90, 70, imagen=pygame.image.load(f"assets/sprites/personaje/knight_run_right_{i}.png")))

    pj_animacion_seleccionada = 'quieto'

    # Enemigos
    img_zombie = pygame.image.load("assets/sprites/enemigos/zombie.png")
    img_esqueleto = pygame.image.load("assets/sprites/enemigos/skeleton.png")
    tipos_enemigos = [img_zombie, img_esqueleto]

    # enemigos = [zombie, esqueleto]
    enemigos = []
    for i in range(8):
        enemigo = crear_entidad((0, 0), ancho=75, alto=100, vida=randint(80, 240), poder_ataque=randint(20, 50), imagen=tipos_enemigos[randint(0, 1)])
        enemigo['rect'].right = randint(limite_izquierdo, limite_derecho)
        enemigo['rect'].top = randint(limite_superior, limite_inferior//2)
        enemigos.append(enemigo)
    # entidades = [zombie, esqueleto, personaje]
    entidades = enemigos.copy()
    entidades.append(personaje)

    for entidad in entidades:
        entidad['hitbox'].bottom = entidad['rect'].bottom
        entidad['hitbox'].centerx = entidad['rect'].centerx

    # Loop del juego
    while True:
        CLOCK.tick(FPS)
        # ------ Detectar eventos ------
        for evento in pygame.event.get():
            if evento.type == QUIT:
                terminar_juego()

            if evento.type == KEYDOWN:
                if evento.key == K_p or evento.key == K_ESCAPE:
                    print("pausa")
                    # Captura de la pantalla actual, para que se muestre el estado de la partida
                    # en el menú pausa
                    captura_pantalla = pygame.Surface((ancho_pantalla, alto_pantalla))
                    captura_pantalla.blit(pantalla, (0, 0))
                    terminar_partida = menu_pausa(pantalla, captura_pantalla)
                    if terminar_partida:
                        return
                    
                if evento.key == K_w:
                    pj_mover_arriba = True
                if evento.key == K_a:
                    pj_mover_izquierda = True
                if evento.key == K_s:
                    pj_mover_abajo = True
                if evento.key == K_d:
                    pj_mover_derecha = True

                if evento.key == K_LSHIFT:
                    pj_sprint = True

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
                    pj_sprint = False
                


        for enemigo in enemigos:
            if calcular_distancia(enemigo['rect'].center, personaje['rect'].center) <= enemigo['radio_deteccion']:
                enemigo['agresivo'] = True

            if personaje['hitbox'].colliderect(enemigo['hitbox']) and pj_vulnerable:
                pj_dañado = True
                pj_daño_recibido = enemigo['poder_ataque']

            # Si el jugador se aleja mucho, el enemigo deja de perseguirlo
            if calcular_distancia(enemigo['rect'].center, personaje['rect'].center) > enemigo['radio_deteccion'] * 3:
                enemigo['agresivo'] = False

                
        # ------ Actualizar elementos ------
        # Daño al personaje
        if pj_dañado:
            pj_dañado = False
            personaje['vida'] -= pj_daño_recibido
            pj_vulnerable = False

        if not pj_vulnerable and cooldown_iframes > 0:
            cooldown_iframes -= 1
        else:
            cooldown_iframes = iframes
            pj_vulnerable = True


        # Movimiento personaje

        if pj_mover_izquierda and personaje["rect"].left > limite_izquierdo:
            personaje["rect"].centerx -= personaje['velocidad'] * multiplicador_sprint
            pj_animacion_seleccionada = 'moviendo_izquierda'

        if pj_mover_derecha and personaje["rect"].right < limite_derecho:
            personaje["rect"].centerx += personaje['velocidad'] * multiplicador_sprint
            pj_animacion_seleccionada = 'moviendo_derecha'

        if not (pj_mover_izquierda or pj_mover_derecha or pj_mover_arriba or pj_mover_abajo):
            pj_animacion_seleccionada = 'quieto'

        if pj_mover_arriba and personaje["rect"].top > limite_superior:
            personaje["rect"].centery -= personaje['velocidad'] * multiplicador_sprint
            pj_animacion_seleccionada = 'moviendo_arriba'

        if pj_mover_abajo and personaje["rect"].bottom < limite_inferior:
            personaje["rect"].centery += personaje['velocidad'] * multiplicador_sprint
            pj_animacion_seleccionada = 'moviendo_abajo'

        # Sprint
        if pj_sprint and personaje['energia'] > 0:
            personaje['energia'] -= 1
            multiplicador_sprint = 2
        if not pj_sprint and personaje['energia'] < pj_energia_maxima:
            personaje['energia'] += 1
            multiplicador_sprint = 1

        if personaje['energia'] <= 0:
            pj_sprint = False
        

        # Tiempo
        contador_ticks -= 1
        if contador_ticks == 0:
            temporizador -= 1
            print(temporizador)
            contador_ticks = FPS
            texto_contador_segundos = escribir_texto((0, 0), f"{temporizador:03}", AMARILLO)
            texto_contador_segundos['rect'].center = (ancho_pantalla //2, altura_hud // 2)

        # Animaciones
        contador_animaciones -= 1
        if contador_animaciones == 0:
            contador_animaciones = duracion_frame_animacion
            frame_animacion_seleccionada += 1
        if frame_animacion_seleccionada > 3:
            frame_animacion_seleccionada = 0


        # Movimiento enemigos

        for enemigo in enemigos:
            if enemigo['agresivo']:
                # Mover al enemigo hacia el jugador
                if enemigo['rect'].centery > personaje['rect'].centery:
                    enemigo['rect'].centery -= enemigo['velocidad']
                else:
                    enemigo['rect'].centery += enemigo['velocidad']
                if enemigo['rect'].centerx > personaje['rect'].centerx:
                    enemigo['rect'].centerx -= enemigo['velocidad']
                else:
                    enemigo['rect'].centerx += enemigo['velocidad']


        for entidad in entidades:
            entidad['hitbox'].bottom = entidad['rect'].bottom
            entidad['hitbox'].centerx = entidad['rect'].centerx

        
        # HUD
        barra_energia['rect'].width = regla_3_simple(personaje['energia'], pj_energia_maxima, fondo_barra_energia['rect'].width - 10)
        barra_energia['rect'].midleft = (fondo_barra_energia['rect'].left + 5, fondo_barra_energia['rect'].centery)

        barra_mana['rect'].width = regla_3_simple(personaje['mana'], pj_mana_maxima, fondo_barra_mana['rect'].width - 10)
        barra_mana['rect'].midleft = (fondo_barra_mana['rect'].left + 5, fondo_barra_mana['rect'].centery)

        barra_vida['rect'].width = regla_3_simple(personaje['vida'], pj_vida_maxima, fondo_barra_vida['rect'].width - 10)
        barra_vida['rect'].midleft = (fondo_barra_vida['rect'].left + 5, fondo_barra_vida['rect'].centery)


        # ------ Dibujar elementos ------

        # Escenario
        pantalla.blit(fondo_escenario, (0, altura_hud))
        pantalla.blit(fondo_hud, (0, 0))

        # HUD
        blitear_texto(pantalla, texto_contador_segundos)
        blitear_texto(pantalla, texto_contador_enemigos)

        dibujar_rectangulo(pantalla, fondo_barra_vida)
        dibujar_rectangulo(pantalla, barra_vida)
        dibujar_rectangulo(pantalla, fondo_barra_mana)
        dibujar_rectangulo(pantalla, barra_mana)
        dibujar_rectangulo(pantalla, fondo_barra_energia)
        dibujar_rectangulo(pantalla, barra_energia)


        # Entidades
        for enemigo in enemigos:
            blitear_superficie(pantalla, enemigo)

        pantalla.blit(animaciones[pj_animacion_seleccionada][frame_animacion_seleccionada]['superficie'], personaje['rect'])

        # Hitboxes
        for entidad in entidades:
            pygame.draw.rect(pantalla, BLANCO, entidad['hitbox'], 1)
        # pygame.draw.rect(pantalla, BLANCO, zombie['rect'], 1)
        # pygame.draw.rect(pantalla, BLANCO, esqueleto['rect'], 1)
        # pygame.draw.rect(pantalla, BLANCO, zombie['hitbox'], 1)
        # pygame.draw.rect(pantalla, BLANCO, esqueleto['hitbox'], 1)
        # pygame.draw.rect(pantalla, ROJO, personaje['hitbox'], 1)

        
        pygame.display.flip()

# pygame.init()
# escenario_juego(pygame.display.set_mode(TAMAÑO_PANTALLA))

# TODO 
# agregar eventos personalizados (que aparezca una bruja cada cierto tiempo, hasta 3 veces)     
# Agregar ataques
# Agregar objetos consumibles (vida, mana)