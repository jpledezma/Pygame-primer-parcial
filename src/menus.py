import pygame
from pygame.locals import *
from creacion_elementos import *
from dibujar_elementos import *
from config import *
from calculos import *
from utilidades import *

# ------------------  Menu Principal  ------------------
def menu_principal(pantalla:pygame.Surface):
    ancho_pantalla = pantalla.get_width()
    alto_pantalla = pantalla.get_height()
    centro_pantalla = (ancho_pantalla//2, alto_pantalla//2)

    # Background
    fondo_menu = pygame.image.load("assets//backgrounds/main-menu-background.jpg")
    fondo_menu = pygame.transform.scale(fondo_menu, (ancho_pantalla, alto_pantalla))

    # Título del juego en el menu
    fuente_titulo = Font("assets/fuentes/ENDOR___.ttf", 50)

    texto_titulo = escribir_texto((0, 0), TITULO, AMARILLO, fuente=fuente_titulo)
    sombra_titulo = escribir_texto((0, 0), TITULO, ROJO, fuente=fuente_titulo)

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
    pygame.mixer.music.play(start=0, loops=-1)
    pygame.mixer.music.set_volume(volumen_musica_global)

    # Loop del menu
    while True:
        for evento in pygame.event.get():
            if evento.type == QUIT:
                terminar_juego()
                
            for boton in botones:
                # if boton['rect_superficie'].collidepoint(pygame.mouse.get_pos()):
                if hover(boton['rect_superficie'], pygame.mouse.get_pos()):
                    boton['fondo'].fill(NARANJA)
                    if evento.type == MOUSEBUTTONDOWN:
                        if boton == btn_iniciar:
                            print("Iniciar")
                            return
                        elif boton == btn_opciones:
                            print("Opciones")
                            menu_opciones(pantalla)
                        elif boton == btn_salir:
                            print("Salir")
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

def menu_opciones(pantalla:pygame.Surface):
    # Variables globales de configuracion
    global musica_activa
    global volumen_musica_global
    global volumen_efectos_global

    ancho_pantalla = pantalla.get_width()
    alto_pantalla = pantalla.get_height()
    centro_pantalla = (ancho_pantalla//2, alto_pantalla//2)

    # Background
    fondo_menu = pygame.image.load("assets/backgrounds/main-menu-background.jpg")
    fondo_menu = pygame.transform.scale(fondo_menu, (ancho_pantalla, alto_pantalla))

    # Texto principal del menú
    fuente_titulo = Font("assets/fuentes/ENDOR___.ttf", 50)

    texto_opciones = escribir_texto((0, 0), "Opciones", AMARILLO, fuente=fuente_titulo)
    sombra_opciones = escribir_texto((0, 0), "Opciones", ROJO, fuente=fuente_titulo)

    texto_opciones['rect'].center = (centro_pantalla[0], alto_pantalla/4)
    sombra_opciones['rect'].center = (centro_pantalla[0] + 3, alto_pantalla/4 + 3)


    # Botones
    btn_volver = crear_boton((0, 0), "Volver", GRIS_CLARO, BURDEOS, espaciado_y=10, espaciado_x=80)
    btn_parar_musica = crear_boton((0, 0), "Activar/desactivar música", GRIS_CLARO, BURDEOS, espaciado_y=10, espaciado_x=80)
    btn_salir = crear_boton((0, 0), "Salir del juego", GRIS_CLARO, BURDEOS, espaciado_y=10, espaciado_x=80)
    btn_activar_cheats = crear_boton((0, 0), "Activar Trucos", GRIS_CLARO, BURDEOS, espaciado_y=10, espaciado_x=80)

    btn_parar_musica['rect_superficie'].center = centro_pantalla
    btn_parar_musica['rect_texto'].center = centro_pantalla

    btn_activar_cheats['rect_superficie'].center = (centro_pantalla[0], btn_parar_musica['rect_superficie'].bottom + 50)
    btn_activar_cheats['rect_texto'].center = (centro_pantalla[0], btn_parar_musica['rect_superficie'].bottom + 50)

    btn_volver['rect_superficie'].center = (centro_pantalla[0], btn_activar_cheats['rect_superficie'].bottom + 50)
    btn_volver['rect_texto'].center = (centro_pantalla[0], btn_activar_cheats['rect_superficie'].bottom + 50)

    btn_salir['rect_superficie'].center = (centro_pantalla[0], btn_volver['rect_superficie'].bottom + 50)
    btn_salir['rect_texto'].center = (centro_pantalla[0], btn_volver['rect_superficie'].bottom + 50)

    botones = [btn_parar_musica, btn_activar_cheats, btn_volver, btn_salir]


    # Selector de volumen de la música
    recta_volumen_musica = crear_rectangulo((50, alto_pantalla - 50), 200, 10, NARANJA, radio_borde=5)
    posicion_volumen_musica_actual = calcular_posicion_recta(volumen_musica_global * 100, recta_volumen_musica['rect'].left, recta_volumen_musica['rect'].right)
    slider_volumen_musica = crear_circulo((posicion_volumen_musica_actual, recta_volumen_musica['rect'].centery), 20, BURDEOS)

    slider_musica_presionado = False

    # Texto volumen música
    texto_volumen_musica = escribir_texto((0, 0), "Volumen música", AMARILLO)
    texto_volumen_musica['rect'].center = (recta_volumen_musica['rect'].centerx, recta_volumen_musica['rect'].centery - 50)

    # Selector de volumen de los efectos
    recta_volumen_efectos = crear_rectangulo((50, texto_volumen_musica['rect'].centery - 80), 200, 10, NARANJA, radio_borde=5)
    posicion_volumen_efectos_actual = calcular_posicion_recta(volumen_efectos_global * 100, recta_volumen_efectos['rect'].left, recta_volumen_efectos['rect'].right)
    slider_volumen_efectos = crear_circulo((posicion_volumen_efectos_actual, recta_volumen_efectos['rect'].centery), 20, BURDEOS)

    slider_musica_presionado = False
    slider_efectos_presionado = False

    sliders = [slider_volumen_musica, slider_volumen_efectos]

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
                            print("Volver")
                            return
                        elif boton == btn_parar_musica:
                            if musica_activa:
                                musica_activa = False
                                # print("Parar musica")
                                pygame.mixer.music.stop()
                            else:
                                musica_activa = True
                                # print("Activar música")
                                pygame.mixer.music.play()
                        elif boton == btn_salir:
                            print("Salir")
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

        # Cambiar el volumen global
        nivel_volumen_musica = calcular_escala(slider_volumen_musica['centro'][0], volumen_minimo, volumen_maximo)
        volumen_musica_global = nivel_volumen_musica / 100

        nivel_volumen_efectos = calcular_escala(slider_volumen_efectos['centro'][0], volumen_minimo, volumen_maximo)
        volumen_efectos_global = nivel_volumen_efectos / 100

        pygame.mixer.music.set_volume(volumen_musica_global)

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

        # print(volumen_musica_global, volumen_efectos_global)
        pygame.display.flip()

