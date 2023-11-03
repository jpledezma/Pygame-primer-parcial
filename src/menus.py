import pygame
from pygame.locals import *
from creacion_elementos import *
from dibujar_elementos import *
from config import *
from calculos import *
from utilidades import *
from random import randrange

fuente_texto_principal = Font("assets/fuentes/ENDOR___.ttf", 50)

# ------------------  Menu Principal  ------------------
def menu_principal(pantalla:pygame.Surface, musica_activa, volumen_musica, volumen_efectos):
    ancho_pantalla = pantalla.get_width()
    alto_pantalla = pantalla.get_height()
    centro_pantalla = (ancho_pantalla//2, alto_pantalla//2)

    # Background
    fondo_menu = pygame.image.load("assets//backgrounds/main-menu-background.jpg")
    fondo_menu = pygame.transform.scale(fondo_menu, (ancho_pantalla, alto_pantalla))

    # Título del juego en el menu
    texto_titulo = escribir_texto((0, 0), TITULO, AMARILLO, fuente=fuente_texto_principal)
    sombra_titulo = escribir_texto((0, 0), TITULO, ROJO, fuente=fuente_texto_principal)

    texto_titulo['rect'].center = (centro_pantalla[0], alto_pantalla/4)
    sombra_titulo['rect'].center = (centro_pantalla[0] + 3, alto_pantalla/4 + 3)

    # Botones del menu
    btn_iniciar = crear_boton((0, 0), "Iniciar", GRIS_CLARO, BURDEOS, espaciado_y=10, espaciado_x=80)
    btn_salir = crear_boton((0, 0), "Salir del juego", GRIS_CLARO, BURDEOS, espaciado_y=10, espaciado_x=80)
    btn_opciones = crear_boton((0, 0), "Opciones", GRIS_CLARO, BURDEOS, espaciado_y=10, espaciado_x=80)

    btn_iniciar['rect_superficie'].center = centro_pantalla
    btn_iniciar['rect_texto'].center = centro_pantalla

    btn_opciones['rect_superficie'].center = (centro_pantalla[0], btn_iniciar['rect_superficie'].bottom + 50)
    btn_opciones['rect_texto'].center = (centro_pantalla[0], btn_iniciar['rect_superficie'].bottom + 50)

    btn_salir['rect_superficie'].center = (centro_pantalla[0], btn_opciones['rect_superficie'].bottom + 50)
    btn_salir['rect_texto'].center = (centro_pantalla[0], btn_opciones['rect_superficie'].bottom + 50)

    botones = [btn_iniciar, btn_salir, btn_opciones]

    # Música del juego
    pygame.mixer.music.load("assets\musica\The-wanderer.mp3")
    if musica_activa:
        pygame.mixer.music.play(start=0, loops=-1)
    pygame.mixer.music.set_volume(volumen_musica)

    # Loop del menu
    while True:
        for evento in pygame.event.get():
            if evento.type == QUIT:
                terminar_juego()
                
            for boton in botones:
                if hover(boton['rect_superficie'], pygame.mouse.get_pos()):
                    boton['fondo'].fill(NARANJA)
                    if evento.type == MOUSEBUTTONDOWN:
                        if boton == btn_iniciar:
                            return (musica_activa, volumen_musica, volumen_efectos)
                        elif boton == btn_opciones:
                            musica_activa, volumen_musica, volumen_efectos, variable_inservible = menu_opciones(pantalla, musica_activa, volumen_musica, volumen_efectos)
                        elif boton == btn_salir:
                            terminar_juego()
                else:
                    boton['fondo'].fill(BURDEOS)

        pantalla.blit(fondo_menu, (0, 0))

        for boton in botones:
            blitear_boton(pantalla, boton)
            blitear_boton(pantalla, boton)

        blitear_texto(pantalla, sombra_titulo)
        blitear_texto(pantalla, texto_titulo)

        pygame.display.flip()


# ------------------  Menu opciones  ------------------

# def menu_opciones(pantalla:pygame.Surface, musica_activa, volumen_musica, volumen_efectos):
def menu_opciones(pantalla:pygame.Surface, musica_activa, volumen_musica, volumen_efectos):
    ancho_pantalla = pantalla.get_width()
    alto_pantalla = pantalla.get_height()
    centro_pantalla = (ancho_pantalla//2, alto_pantalla//2)

    # Background
    fondo_menu = pygame.image.load("assets/backgrounds/main-menu-background.jpg")
    fondo_menu = pygame.transform.scale(fondo_menu, (ancho_pantalla, alto_pantalla))

    # Texto principal del menú

    texto_opciones = escribir_texto((0, 0), "Opciones", AMARILLO, fuente=fuente_texto_principal)
    sombra_opciones = escribir_texto((0, 0), "Opciones", ROJO, fuente=fuente_texto_principal)

    texto_opciones['rect'].center = (centro_pantalla[0], alto_pantalla/4)
    sombra_opciones['rect'].center = (centro_pantalla[0] + 3, alto_pantalla/4 + 3)


    # Botones
    btn_volver = crear_boton((0, 0), "Volver", GRIS_CLARO, BURDEOS, espaciado_y=10, espaciado_x=80)
    btn_parar_musica = crear_boton((0, 0), "Activar/desactivar música", GRIS_CLARO, BURDEOS, espaciado_y=10, espaciado_x=80)
    btn_salir = crear_boton((0, 0), "Salir del juego", GRIS_CLARO, BURDEOS, espaciado_y=10, espaciado_x=80)
    btn_mostrar_instrucciones = crear_boton((0, 0), "Mostrar teclas", GRIS_CLARO, BURDEOS, espaciado_y=10, espaciado_x=80)

    btn_parar_musica['rect_superficie'].center = centro_pantalla
    btn_parar_musica['rect_texto'].center = centro_pantalla

    btn_mostrar_instrucciones['rect_superficie'].center = (centro_pantalla[0], btn_parar_musica['rect_superficie'].bottom + 50)
    btn_mostrar_instrucciones['rect_texto'].center = (centro_pantalla[0], btn_parar_musica['rect_superficie'].bottom + 50)

    btn_volver['rect_superficie'].center = (centro_pantalla[0], btn_mostrar_instrucciones['rect_superficie'].bottom + 50)
    btn_volver['rect_texto'].center = (centro_pantalla[0], btn_mostrar_instrucciones['rect_superficie'].bottom + 50)

    btn_salir['rect_superficie'].center = (centro_pantalla[0], btn_volver['rect_superficie'].bottom + 50)
    btn_salir['rect_texto'].center = (centro_pantalla[0], btn_volver['rect_superficie'].bottom + 50)

    botones = [btn_parar_musica, btn_mostrar_instrucciones, btn_volver, btn_salir]


    # Selector de volumen de la música
    recta_volumen_musica = crear_rectangulo((50, alto_pantalla - 50), 200, 10, NARANJA, radio_borde=5)
    posicion_volumen_musica_actual = calcular_posicion_recta(volumen_musica * 100, recta_volumen_musica['rect'].left, recta_volumen_musica['rect'].right)
    slider_volumen_musica = crear_circulo((posicion_volumen_musica_actual, recta_volumen_musica['rect'].centery), 20, BURDEOS)

    slider_musica_presionado = False

    # Texto volumen música
    texto_volumen_musica = escribir_texto((0, 0), "Volumen música", AMARILLO)
    texto_volumen_musica['rect'].center = (recta_volumen_musica['rect'].centerx, recta_volumen_musica['rect'].centery - 50)

    # Selector de volumen de los efectos
    recta_volumen_efectos = crear_rectangulo((50, texto_volumen_musica['rect'].centery - 80), 200, 10, NARANJA, radio_borde=5)
    posicion_volumen_efectos_actual = calcular_posicion_recta(volumen_efectos * 100, recta_volumen_efectos['rect'].left, recta_volumen_efectos['rect'].right)
    slider_volumen_efectos = crear_circulo((posicion_volumen_efectos_actual, recta_volumen_efectos['rect'].centery), 20, BURDEOS)

    slider_musica_presionado = False
    slider_efectos_presionado = False

    # Tecto volumen efectos
    texto_volumen_efectos = escribir_texto((0, 0), "Volumen efectos", AMARILLO)
    texto_volumen_efectos['rect'].center = (recta_volumen_efectos['rect'].centerx, recta_volumen_efectos['rect'].centery - 50)

    volumen_minimo = recta_volumen_efectos['rect'].left
    volumen_maximo = recta_volumen_efectos['rect'].right
    

    while True:
        for evento in pygame.event.get():
            # Terminar el juego
            if evento.type == QUIT:
                terminar_juego()

            # Detectar cambio de volumen
            if hover_circulo(slider_volumen_musica, pygame.mouse.get_pos()):
                if evento.type == MOUSEBUTTONDOWN:
                    slider_musica_presionado = True
                if evento.type == MOUSEBUTTONUP:
                    slider_musica_presionado = False
            else:
                slider_musica_presionado = False

            if hover_circulo(slider_volumen_efectos, pygame.mouse.get_pos()):
                if evento.type == MOUSEBUTTONDOWN:
                    slider_efectos_presionado = True
                if evento.type == MOUSEBUTTONUP:
                    slider_efectos_presionado = False
            else:
                slider_efectos_presionado = False
                
            # Detectar si se presionaron los botones
            for boton in botones:
                if hover(boton['rect_superficie'], pygame.mouse.get_pos()):
                    boton['fondo'].fill(NARANJA)
                    if evento.type == MOUSEBUTTONDOWN:
                        if boton == btn_volver:
                            # El último True sirve como flag por si se entra a las opciones desde Pausa,
                            # ya que al pulsar en "volver", se detecta al mismo tiempo una pulsación en el
                            # mismo lugar pero en la pantalla pausa.
                            # Esa posición le corresponda al botón "Ir al menú principal", por lo que sale
                            # Inmediatamente del menú pausa y va al menú principal
                            return (musica_activa, volumen_musica, volumen_efectos, True)
                        elif boton == btn_parar_musica:
                            if musica_activa:
                                musica_activa = False
                                pygame.mixer.music.stop()
                            else:
                                musica_activa = True
                                pygame.mixer.music.play()
                        elif boton == btn_salir:
                            terminar_juego()
                else:
                    boton['fondo'].fill(BURDEOS)

        if slider_musica_presionado:
            slider_volumen_musica['color'] = ROJO
            slider_volumen_musica['centro'] = [pygame.mouse.get_pos()[0], slider_volumen_musica['centro'][1]]
            if slider_volumen_musica['centro'][0] < recta_volumen_musica['rect'].left:
                slider_volumen_musica['centro'][0] = recta_volumen_musica['rect'].left
            if slider_volumen_musica['centro'][0] > recta_volumen_musica['rect'].right:
                slider_volumen_musica['centro'][0] = recta_volumen_musica['rect'].right
        else:
            slider_volumen_musica['color'] = BURDEOS

        if slider_efectos_presionado:
            slider_volumen_efectos['color'] = ROJO
            slider_volumen_efectos['centro'] = [pygame.mouse.get_pos()[0], slider_volumen_efectos['centro'][1]]
            if slider_volumen_efectos['centro'][0] < recta_volumen_musica['rect'].left:
                slider_volumen_efectos['centro'][0] = recta_volumen_musica['rect'].left
            if slider_volumen_efectos['centro'][0] > recta_volumen_musica['rect'].right:
                slider_volumen_efectos['centro'][0] = recta_volumen_musica['rect'].right
        else:
            slider_volumen_efectos['color'] = BURDEOS

        # Cambiar el volumen
        nivel_volumen_musica = calcular_escala(slider_volumen_musica['centro'][0], volumen_minimo, volumen_maximo)
        volumen_musica = nivel_volumen_musica / 100

        nivel_volumen_efectos = calcular_escala(slider_volumen_efectos['centro'][0], volumen_minimo, volumen_maximo)
        volumen_efectos = nivel_volumen_efectos / 100

        pygame.mixer.music.set_volume(volumen_musica)

        pantalla.blit(fondo_menu, (0, 0))

        for boton in botones:
            blitear_boton(pantalla, boton)
            blitear_boton(pantalla, boton)

        blitear_texto(pantalla, sombra_opciones)
        blitear_texto(pantalla, texto_opciones)

        blitear_texto(pantalla, texto_volumen_musica)
        blitear_texto(pantalla, texto_volumen_efectos)

        dibujar_rectangulo(pantalla, recta_volumen_musica)
        dibujar_circulo(pantalla, slider_volumen_musica)

        dibujar_rectangulo(pantalla, recta_volumen_efectos)
        dibujar_circulo(pantalla, slider_volumen_efectos)

        pygame.display.flip()


# ------------------  Menu pausa  ------------------
def menu_pausa(pantalla:pygame.Surface, captura_partida: pygame.Surface, musica_activa, volumen_musica, volumen_efectos):
    ancho_pantalla = pantalla.get_width()
    alto_pantalla = pantalla.get_height()
    centro_pantalla = (ancho_pantalla//2, alto_pantalla//2)

    # Background
    filtro_pantalla = pygame.Surface((ancho_pantalla, alto_pantalla))
    filtro_pantalla = filtro_pantalla.convert_alpha()
    filtro_pantalla.fill((0, 0, 0, 150))

    # Título del juego en el menu pausa

    texto_pausa = escribir_texto((0, 0), "Pausa", AMARILLO, fuente=fuente_texto_principal)
    sombra_pausa = escribir_texto((0, 0), "Pausa", ROJO, fuente=fuente_texto_principal)

    texto_pausa['rect'].center = (centro_pantalla[0], alto_pantalla/4)
    sombra_pausa['rect'].center = (centro_pantalla[0] + 3, alto_pantalla/4 + 3)

    # Botones del menu pausa
    btn_continuar = crear_boton((0, 0), "Continuar", GRIS_CLARO, BURDEOS, espaciado_y=10, espaciado_x=80)
    btn_opciones = crear_boton((0, 0), "Opciones", GRIS_CLARO, BURDEOS, espaciado_y=10, espaciado_x=80)
    btn_volver_menu_principal = crear_boton((0, 0), "Ir al menú principal", GRIS_CLARO, BURDEOS, espaciado_y=10, espaciado_x=80)
    btn_salir = crear_boton((0, 0), "Salir del juego", GRIS_CLARO, BURDEOS, espaciado_y=10, espaciado_x=80)

    btn_continuar['rect_superficie'].center = centro_pantalla
    btn_continuar['rect_texto'].center = centro_pantalla

    btn_opciones['rect_superficie'].center = (centro_pantalla[0], btn_continuar['rect_superficie'].bottom + 50)
    btn_opciones['rect_texto'].center = (centro_pantalla[0], btn_continuar['rect_superficie'].bottom + 50)

    btn_volver_menu_principal['rect_superficie'].center = (centro_pantalla[0], btn_opciones['rect_superficie'].bottom + 50)
    btn_volver_menu_principal['rect_texto'].center = (centro_pantalla[0], btn_opciones['rect_superficie'].bottom + 50)
    # btn_volver_menu_principal['rect_superficie'].center = (100, 100)
    # btn_volver_menu_principal['rect_texto'].center = (100, 100)
    
    btn_salir['rect_superficie'].center = (centro_pantalla[0], btn_volver_menu_principal['rect_superficie'].bottom + 50)
    btn_salir['rect_texto'].center = (centro_pantalla[0], btn_volver_menu_principal['rect_superficie'].bottom + 50)

    botones = [btn_continuar, btn_opciones, btn_volver_menu_principal, btn_salir]

    # Loop del menu pausa
    while True:
        # Flag para volver al menú pausa desde el menú de opciones
        flag_volver_opciones = False
        for evento in pygame.event.get():
            if evento.type == QUIT:
                terminar_juego()
                
            for boton in botones:
                if hover(boton['rect_superficie'], pygame.mouse.get_pos()):
                    boton['fondo'].fill(NARANJA)
                    if evento.type == MOUSEBUTTONDOWN:
                        if boton == btn_continuar:
                            return (musica_activa, volumen_musica, volumen_efectos, False)
                        elif boton == btn_opciones:
                            musica_activa, volumen_musica, volumen_efectos, flag_volver_opciones = menu_opciones(pantalla, musica_activa, volumen_musica, volumen_efectos)
                        elif boton == btn_volver_menu_principal and not flag_volver_opciones:
                            # Flag para salir del escenario y volver al loop principal
                            return (musica_activa, volumen_musica, volumen_efectos, True)
                        elif boton == btn_salir:
                            terminar_juego()
                else:
                    boton['fondo'].fill(BURDEOS)

        pantalla.blit(captura_partida, (0, 0))
        pantalla.blit(filtro_pantalla, (0, 0))

        for boton in botones:
            blitear_boton(pantalla, boton)
            blitear_boton(pantalla, boton)

        blitear_texto(pantalla, sombra_pausa)
        blitear_texto(pantalla, texto_pausa)

        pygame.display.flip()


def menu_game_over(pantalla:pygame.Surface, victoria:bool, puntuacion:int, comentario:str) -> None:
    ancho_pantalla = pantalla.get_width()
    alto_pantalla = pantalla.get_height()
    centro_pantalla = (ancho_pantalla//2, alto_pantalla//2)

    # Leer el archivo de puntaje máximo para comparar las puntuaciones
    # Si no existe, crearlo y escribir la puntuacion recibida por parametro
    try:
        archivo_puntuacion = open('puntuacion.csv', 'r')
        puntaje_maximo = int(archivo_puntuacion.readline())
        if puntuacion > puntaje_maximo:
            puntaje_maximo = puntuacion
    except:
        puntaje_maximo = puntuacion
    finally:
        archivo_puntuacion = open('puntuacion.csv', 'w')
        archivo_puntuacion.write(str(puntaje_maximo))
        archivo_puntuacion.close()

    if victoria:
        color_texto = AMARILLO
        mensaje = "Victoria"
        sonido_finalizacion = pygame.mixer.Sound("./assets/sfx/victory.mp3")
        frases = ("You defeated", "10 dexterity. But don't tell anyone you leveled that up.", 
                  "Giant's, giant's, giant's. Become UNSTOPPABLE.", "Well, what is it? Are you pro yet?",
                  "The legend never dies.", "Bear seek seek lest")

    else:
        color_texto = ROJO
        mensaje = "Game Over"
        sonido_finalizacion = pygame.mixer.Sound("./assets/sfx/game_over.mp3")
        frases = ("Hesitation is defeat.", "git gud", "Just level up adp", 
                  "Unfortunately for you, however, you are maidenless.", 
                  "Shiva the east? More like shiva the deceased", "You were still just a puppy.",
                  "Don't you dare go Hollow.", "So easily forgotten...", 'Is this "too easy" for you?')

    # Textos
    fuente_frase = pygame.font.SysFont('Arial', 32)
    fuente_comentario = pygame.font.SysFont('Arial', 40)

    texto_principal = escribir_texto((0, 0), mensaje, color_texto, fuente=fuente_texto_principal)
    texto_frase_aleatoria = escribir_texto((0, 0), frases[randrange(len(frases))], GRIS_CLARO, fuente=fuente_frase)
    texto_comentario = escribir_texto((0, 0), comentario, BLANCO, fuente=fuente_comentario)
    texto_puntaje = escribir_texto((0, 0), f"Puntaje: {puntuacion}", BLANCO, fuente=fuente_frase)
    texto_puntaje_maximo = escribir_texto((0, 0), f"Puntaje máximo: {puntaje_maximo}", BLANCO, fuente=fuente_frase)

    texto_principal['rect'].center = (centro_pantalla[0], alto_pantalla / 6)
    texto_comentario['rect'].center = (centro_pantalla[0], texto_principal['rect'].centery + 130)
    texto_frase_aleatoria['rect'].center = (centro_pantalla[0], centro_pantalla[1] - 50)
    texto_puntaje['rect'].center = (centro_pantalla[0], centro_pantalla[1] + 50)
    texto_puntaje_maximo['rect'].center = (centro_pantalla[0], texto_puntaje['rect'].centery + 50)

    textos = [texto_principal, texto_comentario, texto_frase_aleatoria, texto_puntaje, texto_puntaje_maximo]

    # Botones
    btn_volver_menu_principal = crear_boton((0, 0), "Volver al menú principal", GRIS_CLARO, AZUL, espaciado_y=15, espaciado_x=80)
    btn_salir = crear_boton((0, 0), "Salir del juego", GRIS_CLARO, AZUL, espaciado_y=15, espaciado_x=80)

    btn_salir['rect_superficie'].midbottom = (centro_pantalla[0], alto_pantalla - 50)
    btn_salir['rect_texto'].center = btn_salir['rect_superficie'].center

    btn_volver_menu_principal['rect_superficie'].center = (centro_pantalla[0], btn_salir['rect_superficie'].top - 50)
    btn_volver_menu_principal['rect_texto'].center = (centro_pantalla[0], btn_salir['rect_superficie'].top - 50)

    botones = [btn_volver_menu_principal, btn_salir]

    sonido_finalizacion.play()

    while True:
        for evento in pygame.event.get():
            if evento.type == QUIT:
                terminar_juego()
                
            for boton in botones:
                if hover(boton['rect_superficie'], pygame.mouse.get_pos()):
                    boton['fondo'].fill(CELESTE)
                    if evento.type == MOUSEBUTTONDOWN:
                        if boton == btn_volver_menu_principal:
                            return
                        elif boton == btn_salir:
                            terminar_juego()
                else:
                    boton['fondo'].fill(AZUL)

        pantalla.fill(NEGRO)

        blitear_boton(pantalla, btn_volver_menu_principal)
        blitear_boton(pantalla, btn_salir)

        for texto in textos:
            blitear_texto(pantalla, texto)

        pygame.display.flip()
