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
def escenario_juego(pantalla:pygame.Surface, musica_activa:bool, volumen_musica:float, volumen_efectos:float):

    # Control de tiempo
    CLOCK = pygame.time.Clock()

    temporizador = 200
    contador_ticks = FPS

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

    # Trucos
    texto_trucos_activos = escribir_texto((0, 0), f"Trucos activos", AQUA)
    texto_trucos_activos['rect'].center = (ancho_pantalla //2, altura_hud // 2 + 80)      
    trucos_activos = False
    trucos = {'mostrar_hitboxes': False,
              'vida_infinita': False,
              'energia_infinita': False,
              'mana_infinita': False,
              'invisible': False,
              'one-shot': False,
              'super_velocidad':False
             }

    # Música del juego
    try:
        pygame.mixer.music.load("assets\musica\OurLordIsNotReady.mp3")
        if musica_activa:
            pygame.mixer.music.play(start=0, loops=-1)
            pygame.mixer.music.set_volume(volumen_musica)
    except:
        print("No se conectó ningún dispositivo de salida de audio")
    # Sonidos
    try:
        sfx_pj_ataque = pygame.mixer.Sound("./assets/sfx/sword_attack.wav")
        sfx_usar_pocion = pygame.mixer.Sound("./assets/sfx/potion_pickup.wav")
        sfx_pj_ataque_especial = pygame.mixer.Sound("./assets/sfx/special_attack.wav")
        sfx_pj_dañado = pygame.mixer.Sound("./assets/sfx/damage_taken.wav")
        sfx_ataque_bruja = pygame.mixer.Sound("./assets/sfx/witch_attack.wav")
        sfx_enemigo_muerto = pygame.mixer.Sound("./assets/sfx/enemy_death.wav")
        sfx_enemigo_dañado = pygame.mixer.Sound("./assets/sfx/enemy_damaged.wav")
        sonidos = [sfx_pj_ataque, sfx_usar_pocion, sfx_pj_ataque_especial, sfx_pj_dañado, sfx_ataque_bruja, sfx_enemigo_muerto, sfx_enemigo_dañado]

        for sonido in sonidos:
            sonido.set_volume(volumen_efectos)
    except:
            print("No se conectó ningún dispositivo de salida de audio")
    

    # ---- Personaje principal ----
    # Atributos
    multiplicador_sprint = 1
    pj_vida_maxima = 200
    pj_mana_maxima = 100
    pj_energia_maxima = FPS * 3
    flag_sfx_ataque = False
    pj_atacando = False
    pj_cd_ataque = FPS // 2
    pj_contador_cd_ataque = pj_cd_ataque
    flag_pj_cd_ataque = True
    # Movimiento personaje
    pj_mover_arriba = False
    pj_mover_abajo = False
    pj_mover_derecha = False
    pj_mover_izquierda = False
    pj_sprint = False
    # Ataques
    pj_ataque_arriba = False
    pj_ataque_abajo = False
    pj_ataque_derecha = False
    pj_ataque_izquierda = False
    # Ataque especial
    pj_ataque_especial = False
    # Animaciones
    animaciones = {'quieto': [], 'moviendo_arriba':[], 'moviendo_abajo':[], 'moviendo_izquierda':[], 'moviendo_derecha':[], 
                   'atacando_arriba':[], 'atacando_abajo':[], 'atacando_derecha':[], 'atacando_izquierda':[]}
    for i in range(4):
        animaciones['quieto'].append(crear_superficie((0, 0), 90, 70, imagen=pygame.image.load(f"assets/sprites/personaje/knight_idle_{i}.png")))
        animaciones['moviendo_abajo'].append(crear_superficie((0, 0), 90, 70, imagen=pygame.image.load(f"assets/sprites/personaje/knight_run_down_{i}.png")))
        animaciones['moviendo_arriba'].append(crear_superficie((0, 0), 90, 70, imagen=pygame.image.load(f"assets/sprites/personaje/knight_run_up_{i}.png")))
        animaciones['moviendo_izquierda'].append(crear_superficie((0, 0), 90, 70, imagen=pygame.image.load(f"assets/sprites/personaje/knight_run_left_{i}.png")))
        animaciones['moviendo_derecha'].append(crear_superficie((0, 0), 90, 70, imagen=pygame.image.load(f"assets/sprites/personaje/knight_run_right_{i}.png")))
        animaciones['atacando_arriba'].append(crear_superficie((0, 0), 90, 70, imagen=pygame.image.load(f"assets/sprites/personaje/knight_slice_up_{i}.png")))
        animaciones['atacando_abajo'].append(crear_superficie((0, 0), 90, 70, imagen=pygame.image.load(f"assets/sprites/personaje/knight_slice_down_{i}.png")))
        animaciones['atacando_derecha'].append(crear_superficie((0, 0), 90, 70, imagen=pygame.image.load(f"assets/sprites/personaje/knight_slice_right_{i}.png")))
        animaciones['atacando_izquierda'].append(crear_superficie((0, 0), 90, 70, imagen=pygame.image.load(f"assets/sprites/personaje/knight_slice_left_{i}.png")))

    pj_animacion_seleccionada = 'quieto'
    duracion_frame_animacion = FPS // 4
    contador_animaciones = duracion_frame_animacion
    frame_animacion_seleccionada = 0
    # Superficie
    personaje = crear_entidad((0, 0), 90, 70, vida=pj_vida_maxima, poder_ataque=50, mana=pj_mana_maxima, energia=pj_energia_maxima, iframes=FPS, vulnerable=True, imagen=animaciones['quieto'][0]['imagen'])
    personaje['rect'].center = (ancho_pantalla / 2, alto_pantalla - 50)
    img_ataque_especial = pygame.image.load(f"assets\sprites\efectos\magic_spell.png")
    ataques_especiales = []

    # ---- Enemigos ----
    img_zombie = pygame.image.load("assets/sprites/enemigos/zombie.png")
    img_esqueleto = pygame.image.load("assets/sprites/enemigos/skeleton.png")
    img_bruja = pygame.image.load("assets/sprites/enemigos/witch.png")
    img_ataque_bruja = pygame.image.load("assets/sprites/efectos/witch_spell.png")
    tipos_enemigos = [img_zombie, img_esqueleto]

    ataque_bruja = FPS * 2
    cd_ataque_bruja = ataque_bruja
    flag_ataque_bruja = True

    enemigos = []
    for i in range(8):
        enemigo = crear_entidad((randint(limite_izquierdo, limite_derecho - 75), randint(limite_superior, limite_inferior//2)), ancho=75, alto=100, vida=randint(80, 240), poder_ataque=randint(20, 50), iframes=FPS//2, imagen=tipos_enemigos[randint(0, 1)])
        enemigos.append(enemigo)

    # ---- Consumibles ----
    img_pocion_vida = pygame.image.load("assets/sprites/consumibles/health_potion.png")
    img_pocion_mana = pygame.image.load("assets/sprites/consumibles/mana_potion.png")
    pociones = []

    entidades = enemigos.copy()
    entidades.append(personaje)

    for entidad in entidades:
        entidad['hitbox'].bottom = entidad['rect'].bottom
        entidad['hitbox'].centerx = entidad['rect'].centerx

    # Evento personalizados
    EVENTO_ENEMIGO_ESPECIAL = pygame.USEREVENT + 1
    pygame.time.set_timer(EVENTO_ENEMIGO_ESPECIAL, 20000)

    EVENTO_POCION_VIDA = pygame.USEREVENT + 2
    pygame.time.set_timer(EVENTO_POCION_VIDA, 10000)

    EVENTO_POCION_MANA = pygame.USEREVENT + 3
    pygame.time.set_timer(EVENTO_POCION_MANA, 10000)

    # Bonus de puntuacion por si no se recibe daño
    bonus_no_hit = 2000
    # Multiplicador para detectar la activacion de trucos
    bonus_sin_trucos = 1

    # Loop del juego
    while True:
        CLOCK.tick(FPS)
        # Ajustar el sonido de los efectos
        for sonido in sonidos:
            sonido.set_volume(volumen_efectos)

        # ------ Detectar eventos ------
        for evento in pygame.event.get():
            # Salir del juego
            if evento.type == QUIT:
                terminar_juego()

            # -- Presionar teclas --
            if evento.type == KEYDOWN:
                # Pausa
                if evento.key == K_p or evento.key == K_ESCAPE:
                    # Captura de la pantalla actual, para que se muestre el estado de la partida
                    # en el menú pausa
                    captura_pantalla = pygame.Surface((ancho_pantalla, alto_pantalla))
                    captura_pantalla.blit(pantalla, (0, 0))
                    musica_activa, volumen_musica, volumen_efectos, terminar_partida = menu_pausa(pantalla, captura_pantalla, musica_activa, volumen_musica, volumen_efectos)
                    if terminar_partida:
                        return musica_activa, volumen_musica, volumen_efectos

                # Iniciar movimiento personaje
                if evento.key == K_w or evento.key == K_a or evento.key == K_s or evento.key == K_d:
                    pj_atacando = False
                if evento.key == K_w:
                    pj_mover_arriba = True
                if evento.key == K_a:
                    pj_mover_izquierda = True
                if evento.key == K_s:
                    pj_mover_abajo = True
                if evento.key == K_d:
                    pj_mover_derecha = True
                # Sprint
                if evento.key == K_LSHIFT:
                    pj_sprint = True

                if evento.key == K_i or evento.key == K_k or evento.key == K_j or evento.key == K_l:
                    flag_sfx_ataque = True
                    pj_atacando = True
                # Ataque personaje
                if evento.key == K_i:
                    pj_ataque_arriba = True
                if evento.key == K_k:
                    pj_ataque_abajo = True
                if evento.key == K_l:
                    pj_ataque_derecha = True
                if evento.key == K_j:
                    pj_ataque_izquierda = True
                # Ataque especial
                if evento.key == K_SPACE:
                    pj_ataque_especial = True

                # Trucos
                if evento.key == K_F1:
                    bonus_sin_trucos = 0
                    if trucos_activos:
                        trucos_activos = False
                    else:
                        trucos_activos = True

                if trucos_activos:

                    if evento.key == K_1:
                        if trucos['mostrar_hitboxes']:
                            trucos['mostrar_hitboxes'] = False
                        else:
                            trucos['mostrar_hitboxes'] = True
                            

                    if evento.key == K_2:
                        if trucos['vida_infinita']:
                            trucos['vida_infinita'] = False
                        else:
                            trucos['vida_infinita'] = True

                    if evento.key == K_3:
                        if trucos['mana_infinita']:
                            trucos['mana_infinita'] = False
                        else:
                            trucos['mana_infinita'] = True

                    if evento.key == K_4:
                        if trucos['energia_infinita']:
                            trucos['energia_infinita'] = False
                        else:
                            trucos['energia_infinita'] = True

                    if evento.key == K_5:
                        if trucos['one-shot']:
                            trucos['one-shot'] = False
                        else:
                            trucos['one-shot'] = True

                    if evento.key == K_6:
                        if trucos['invisible']:
                            trucos['invisible'] = False
                        else:
                            trucos['invisible'] = True

                    if evento.key == K_7:
                        if trucos['super_velocidad']:
                            trucos['super_velocidad'] = False
                        else:
                            trucos['super_velocidad'] = True

            # -- Soltar teclas --
            if evento.type == KEYUP:
                # Detener movimiento personaje
                if evento.key == K_i or evento.key == K_k or evento.key == K_j or evento.key == K_l:
                    pj_atacando = False
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

                # Ataque personaje
                if evento.key == K_i:
                    pj_ataque_arriba = False
                if evento.key == K_k:
                    pj_ataque_abajo = False
                if evento.key == K_l:
                    pj_ataque_derecha = False
                if evento.key == K_j:
                    pj_ataque_izquierda = False
                # Ataque especial
                if evento.key == K_SPACE:
                    pj_ataque_especial = False

            # Spawn bruja
            if evento.type == EVENTO_ENEMIGO_ESPECIAL:
                bruja = crear_entidad((randint(limite_izquierdo, limite_derecho - 75), limite_superior), ancho=75, alto=100, vida=300, radio_deteccion=0, poder_ataque=100,iframes=FPS//2, imagen=img_bruja)
                enemigos.append(bruja)
                entidades.append(bruja)
            
            # Spawn pociones
            if evento.type == EVENTO_POCION_VIDA and len(pociones) < 2:
                pocion_vida = crear_entidad((randint(limite_izquierdo + 50, limite_derecho - 50), randint(limite_superior + 50, limite_inferior - 50)), ancho=25, alto=25, vida=1, mana=0, radio_deteccion=0, poder_ataque=0, imagen=img_pocion_vida)
                pociones.append(pocion_vida)
                entidades.append(pocion_vida)
            if evento.type == EVENTO_POCION_MANA and len(pociones) < 2:
                pocion_mana = crear_entidad((randint(limite_izquierdo + 50, limite_derecho - 50), randint(limite_superior + 50, limite_inferior - 50)), ancho=25, alto=25, vida=0, mana=1, radio_deteccion=0, poder_ataque=0, imagen=img_pocion_mana)
                pociones.append(pocion_mana)
                entidades.append(pocion_mana)
                

        # ------ Actualizar elementos ------

        # Ataque personaje
        if pj_atacando and personaje['energia'] > 15:
            pj_mover_abajo = False
            pj_mover_arriba = False
            pj_mover_derecha = False
            pj_mover_izquierda = False
            if flag_sfx_ataque:
                try:
                    sfx_pj_ataque.play()
                except:
                    print("No se conectó ningún dispositivo de salida de audio")
                flag_sfx_ataque = False
            # Reproducir el sonido de nuevo si se completa la animacion
            if contador_ticks == FPS:
                flag_sfx_ataque = True

            if pj_ataque_arriba:
                pj_animacion_seleccionada = 'atacando_arriba'
                hitbox_ataque = crear_rectangulo((0, 0), personaje['rect'].width, personaje['hitbox'].height, VERDE)
                hitbox_ataque['rect'].midtop = personaje['rect'].midtop

            if pj_ataque_abajo:
                pj_animacion_seleccionada = 'atacando_abajo'
                hitbox_ataque = crear_rectangulo((0, 0), personaje['rect'].width, personaje['hitbox'].height, VERDE)
                hitbox_ataque['rect'].midbottom = personaje['rect'].midbottom

            if pj_ataque_derecha:
                pj_animacion_seleccionada = 'atacando_derecha'
                hitbox_ataque = crear_rectangulo((0, 0), personaje['rect'].width//4*3, personaje['hitbox'].height, VERDE)
                hitbox_ataque['rect'].midleft = (personaje['rect'].centerx - 20, personaje['rect'].centery + 10)

            if pj_ataque_izquierda:
                pj_animacion_seleccionada = 'atacando_izquierda'
                hitbox_ataque = crear_rectangulo((0, 0), personaje['rect'].width//4*3, personaje['hitbox'].height, VERDE)
                hitbox_ataque['rect'].midright = (personaje['rect'].centerx + 20, personaje['rect'].centery + 10)

            if flag_pj_cd_ataque:
                personaje['energia'] -= 30
                flag_pj_cd_ataque = False
        else:
            pj_atacando = False
            pj_animacion_seleccionada = 'quieto'

        if not flag_pj_cd_ataque and pj_contador_cd_ataque > 0:
            pj_contador_cd_ataque -= 1
        else:
            pj_contador_cd_ataque = pj_cd_ataque
            flag_pj_cd_ataque = True

        # Ataque especial personaje
        if pj_ataque_especial and personaje['mana'] >= 20:
            try:
                sfx_pj_ataque_especial.play()
            except:
                print("No se conectó ningún dispositivo de salida de audio")
            pj_ataque_especial = False
            personaje['mana'] -= 40
            ataque_especial = crear_entidad((personaje['rect'].left + 17, personaje['rect'].top), 50, 50, vida=1, velocidad=3, poder_ataque=100, radio_deteccion=0, imagen=img_ataque_especial)
            ataques_especiales.append(ataque_especial)
            entidades.append(ataque_especial)
        if personaje['mana'] <= 0:
            personaje['mana'] = 0
        for ataque in ataques_especiales[:]:
            ataque['rect'].top -= ataque['velocidad']
            if ataque['rect'].bottom <= 0:
                entidades.remove(ataque)
                ataques_especiales.remove(ataque)

        # Estado de los enemigos
        for enemigo in enemigos[:]:
            # Detectar al personaje
            if calcular_distancia(enemigo['rect'].center, personaje['rect'].center) <= enemigo['radio_deteccion']:
                enemigo['agresivo'] = True

            if enemigo['agresivo'] and not trucos['invisible']:
                # Mover al enemigo hacia el jugador
                if enemigo['rect'].centery > personaje['rect'].centery:
                    enemigo['rect'].centery -= enemigo['velocidad']
                else:
                    enemigo['rect'].centery += enemigo['velocidad']
                if enemigo['rect'].centerx > personaje['rect'].centerx:
                    enemigo['rect'].centerx -= enemigo['velocidad']
                else:
                    enemigo['rect'].centerx += enemigo['velocidad']

            # Dañar al personaje
            if personaje['hitbox'].colliderect(enemigo['hitbox']) and personaje['vulnerable']:
                personaje['vida'] -= enemigo['poder_ataque']
                try:
                    sfx_pj_dañado.play()
                except:
                    print("No se conectó ningún dispositivo de salida de audio")
                personaje['vulnerable'] = False
                bonus_no_hit = 0
                if enemigo['imagen'] == img_ataque_bruja:
                    enemigo['vida'] = 0

            # Si el jugador se aleja mucho, el enemigo deja de perseguirlo
            if calcular_distancia(enemigo['rect'].center, personaje['rect'].center) > enemigo['radio_deteccion'] * 1.5:
                enemigo['agresivo'] = False

            # Daño al enemigo
            if enemigo['vulnerable'] and pj_atacando and hitbox_ataque['rect'].colliderect(enemigo['hitbox']):
                enemigo["vida"] -= personaje['poder_ataque']
                enemigo['vulnerable'] = False
                try:
                    sfx_pj_ataque.stop()
                    sfx_enemigo_dañado.play()
                except:
                    print("No se conectó ningún dispositivo de salida de audio")
            for ataque in ataques_especiales:
                if enemigo['vulnerable'] and ataque['rect'].colliderect(enemigo['hitbox']):
                    enemigo["vida"] -= ataque['poder_ataque']
                    enemigo['vulnerable'] = False
                    try:
                        sfx_enemigo_dañado.play()
                    except:
                        print("No se conectó ningún dispositivo de salida de audio")

            # Ataque especial de la bruja
            if enemigo['imagen'] == img_bruja:
                if flag_ataque_bruja and len(enemigos) < 10 and not trucos['invisible']:
                    flag_ataque_bruja = False
                    ataque = crear_entidad(enemigo['rect'].center, 50, 50, vida=1, velocidad=randint(1, 3), poder_ataque=15, radio_deteccion=1000, imagen=img_ataque_bruja)
                    enemigos.append(ataque)
                    entidades.append(ataque)
                    try:
                        sfx_ataque_bruja.play()
                    except:
                        print("No se conectó ningún dispositivo de salida de audio")
                if not flag_ataque_bruja and cd_ataque_bruja > 0:
                    cd_ataque_bruja -= 1
                else:
                    cd_ataque_bruja = ataque_bruja
                    flag_ataque_bruja = True

            # Muerte del enemigo
            if enemigo["vida"] <= 0:
                try:
                    sfx_enemigo_muerto.play()
                except:
                    print("No se conectó ningún dispositivo de salida de audio")
                enemigos.remove(enemigo)
                entidades.remove(enemigo)
                if enemigo['imagen'] != img_ataque_bruja:
                    enemigos_derrotados += 1
                    texto_contador_enemigos = escribir_texto((0, 0), f"Enemigos derrotados: {enemigos_derrotados:02}", AMARILLO)
                    texto_contador_enemigos['rect'].center = (ancho_pantalla // 4 * 3, altura_hud // 2)

        # Consumir pociones
        for pocion in pociones[:]:
            if personaje['rect'].colliderect(pocion['rect']):
                pociones.remove(pocion)
                entidades.remove(pocion)
                try:
                    sfx_usar_pocion.play()
                except:
                    print("No se conectó ningún dispositivo de salida de audio")
                if pocion["vida"]:
                    personaje['vida'] += 50
                if personaje['vida'] > pj_vida_maxima:
                    personaje['vida'] = pj_vida_maxima
                if pocion["mana"]:
                    personaje['mana'] += 50
                if personaje['mana'] > pj_mana_maxima:
                    personaje['mana'] = pj_mana_maxima


        # Daño a las entidades
        # Se agregan iframes (frames de invulnerabilidad) para que solo
        # reciban daño cada cierto tiempo, y que no sea de manera continua
        for entidad in entidades:
            if not entidad['vulnerable'] and entidad['cd_iframes'] > 0:
                entidad['cd_iframes'] -= 1
            else:
                entidad['cd_iframes'] = entidad['iframes']
                entidad['vulnerable'] = True
        
            
        # Movimiento personaje
        if pj_mover_izquierda and personaje["rect"].left > limite_izquierdo:
            personaje["rect"].centerx -= personaje['velocidad'] * multiplicador_sprint
            pj_animacion_seleccionada = 'moviendo_izquierda'

        if pj_mover_derecha and personaje["rect"].right < limite_derecho:
            personaje["rect"].centerx += personaje['velocidad'] * multiplicador_sprint
            pj_animacion_seleccionada = 'moviendo_derecha'

        if pj_mover_arriba and personaje["rect"].top > limite_superior:
            personaje["rect"].centery -= personaje['velocidad'] * multiplicador_sprint
            pj_animacion_seleccionada = 'moviendo_arriba'

        if pj_mover_abajo and personaje["rect"].bottom < limite_inferior:
            personaje["rect"].centery += personaje['velocidad'] * multiplicador_sprint
            pj_animacion_seleccionada = 'moviendo_abajo'

        if not (pj_mover_izquierda or pj_mover_derecha or pj_mover_arriba or pj_mover_abajo 
                or pj_ataque_arriba or pj_ataque_abajo or pj_ataque_derecha or pj_ataque_izquierda):
            pj_animacion_seleccionada = 'quieto'

        # Sprint
        if pj_sprint and personaje['energia'] > 0:
            personaje['energia'] -= 1
            multiplicador_sprint = 2
        # Hay que poner esto si se activa el truco energia infinita, idk why
        if not pj_sprint:
            multiplicador_sprint = 1
        if not pj_sprint and not pj_atacando and personaje['energia'] < pj_energia_maxima:
            personaje['energia'] += 1
            multiplicador_sprint = 1

        if personaje['energia'] <= 0:
            pj_sprint = False
            pj_atacando = False
        
        # Animaciones

        # Cuenta atrás del tiempo que dura cada imagen de la animacion
        contador_animaciones -= 1
        # Si en contador llega a 0, se reinicia y vuelve a contar
        # Además, pasa a la siguiente imagen de la animacion
        if contador_animaciones == 0:
            contador_animaciones = duracion_frame_animacion
            frame_animacion_seleccionada += 1
        # Cuando llega a la ultima imagen de la animacion, se reinicia
        #  y vuelve a la primera en el proximo ciclo
        if frame_animacion_seleccionada > 3:
            frame_animacion_seleccionada = 0
        

        # -- Tiempo --
        contador_ticks -= 1
        if contador_ticks == 0:
            temporizador -= 1
            contador_ticks = FPS
            texto_contador_segundos = escribir_texto((0, 0), f"{temporizador:03}", AMARILLO)
            texto_contador_segundos['rect'].center = (ancho_pantalla //2, altura_hud // 2)      


        # Hitboxes
        for entidad in entidades:
            entidad['hitbox'].bottom = entidad['rect'].bottom
            entidad['hitbox'].centerx = entidad['rect'].centerx

        if pj_ataque_abajo:
            personaje['hitbox'].centery -= 20
        if pj_ataque_derecha:
            personaje['hitbox'].centerx -= 20
        if pj_ataque_izquierda:
            personaje['hitbox'].centerx += 20

        
        # HUD
        barra_energia['rect'].width = regla_3_simple(personaje['energia'], pj_energia_maxima, fondo_barra_energia['rect'].width - 10)
        barra_energia['rect'].midleft = (fondo_barra_energia['rect'].left + 5, fondo_barra_energia['rect'].centery)

        barra_mana['rect'].width = regla_3_simple(personaje['mana'], pj_mana_maxima, fondo_barra_mana['rect'].width - 10)
        barra_mana['rect'].midleft = (fondo_barra_mana['rect'].left + 5, fondo_barra_mana['rect'].centery)

        barra_vida['rect'].width = regla_3_simple(personaje['vida'], pj_vida_maxima, fondo_barra_vida['rect'].width - 10)
        barra_vida['rect'].midleft = (fondo_barra_vida['rect'].left + 5, fondo_barra_vida['rect'].centery)

        # Trucos
        if trucos['vida_infinita']:
            pj_vida_maxima = 1000000
            personaje['vida'] = pj_vida_maxima
        if trucos['energia_infinita']:
            pj_energia_maxima = 100000
            personaje['energia'] = pj_energia_maxima
        if trucos['mana_infinita']:
            pj_mana_maxima = 100000
            personaje['mana'] = pj_mana_maxima
        if trucos['one-shot']:
            personaje['poder_ataque'] = 100000
        if trucos['super_velocidad'] and pj_sprint:
            multiplicador_sprint = 5


        # Terminar partida
        if len(enemigos) == 0:
            puntaje = (enemigos_derrotados * 100 + temporizador * 10 + bonus_no_hit) * bonus_sin_trucos
            for truco in trucos.values():
                if truco:
                    puntaje = 0
                    break
            menu_game_over(pantalla, True, puntaje, "Has derrotado a todos los enemigos")
            return musica_activa, volumen_musica, volumen_efectos
        
        if personaje['vida'] <= 0:
            menu_game_over(pantalla, False, 0, "Has muerto")
            return musica_activa, volumen_musica, volumen_efectos
        
        if temporizador <= 0:
            menu_game_over(pantalla, False, 0, "Se ha agotado el tiempo")
            return musica_activa, volumen_musica, volumen_efectos


        # ------ Dibujar elementos ------

        # Escenario
        pantalla.blit(fondo_escenario, (0, altura_hud))
        pantalla.blit(fondo_hud, (0, 0))

        # Enemigos
        for enemigo in enemigos:
            blitear_superficie(pantalla, enemigo)

        # Ataques especiales del jugador
        for ataque in ataques_especiales:
            blitear_superficie(pantalla, ataque)

        if trucos_activos:
            blitear_texto(pantalla, texto_trucos_activos)
            if trucos['mostrar_hitboxes']:
                # Hitboxes
                if pj_atacando:
                    dibujar_rectangulo(pantalla, hitbox_ataque)
                for entidad in entidades:
                    pygame.draw.rect(pantalla, AMARILLO, entidad['hitbox'], 1)
                    pygame.draw.rect(pantalla, BLANCO, entidad['rect'], 1)

        # Personaje
        pantalla.blit(animaciones[pj_animacion_seleccionada][frame_animacion_seleccionada]['superficie'], personaje['rect'])

        # Consumibles
        for pocion in pociones:
            blitear_superficie(pantalla, pocion)

        # HUD
        blitear_texto(pantalla, texto_contador_segundos)
        blitear_texto(pantalla, texto_contador_enemigos)

        dibujar_rectangulo(pantalla, fondo_barra_vida)
        dibujar_rectangulo(pantalla, barra_vida)
        dibujar_rectangulo(pantalla, fondo_barra_mana)
        dibujar_rectangulo(pantalla, barra_mana)
        dibujar_rectangulo(pantalla, fondo_barra_energia)
        dibujar_rectangulo(pantalla, barra_energia)

        pygame.display.flip()
