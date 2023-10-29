import pygame
from pygame.locals import *
from creacion_elementos import *
from dibujar_elementos import *
from config import *
from calculos import *

def terminar_juego():
    pygame.quit()
    exit()

def hover(rect:pygame.Rect, punto:tuple[int, int]) -> bool:
    if rect.collidepoint(punto):
        return True
    return False

def hover_circulo(circulo:dict, punto:tuple[int, int]) -> bool:
    distancia = calcular_distancia(circulo['centro'], punto)
    if distancia <= circulo['radio']:
        return True
    return False

# ------------------  Menu Principal  ------------------
def menu_principal(pantalla:pygame.Surface):
    ancho_pantalla = pantalla.get_width()
    alto_pantalla = pantalla.get_height()
    centro_pantalla = (ancho_pantalla//2, alto_pantalla//2)

    fondo_menu = pygame.image.load("assets/main-menu-background.jpg")
    fondo_menu = pygame.transform.scale(fondo_menu, (ancho_pantalla, alto_pantalla))

    fuente_titulo = Font("assets/fuentes/ENDOR___.ttf", 50)

    texto_titulo = escribir_texto((0, 0), TITULO, AMARILLO, fuente=fuente_titulo)
    sombra_titulo = escribir_texto((0, 0), TITULO, ROJO, fuente=fuente_titulo)

    btn_iniciar = crear_boton((0, 0), "Iniciar", GRIS_CLARO, BURDEOS, espaciado_y=10, espaciado_x=80)
    btn_salir = crear_boton((0, 0), "Salir del juego", GRIS_CLARO, BURDEOS, espaciado_y=10, espaciado_x=80)
    btn_opciones = crear_boton((0, 0), "Opciones", GRIS_CLARO, BURDEOS, espaciado_y=10, espaciado_x=80)

    texto_titulo['rect'].center = (centro_pantalla[0], alto_pantalla/4)
    sombra_titulo['rect'].center = (centro_pantalla[0] + 3, alto_pantalla/4 + 3)

    btn_iniciar['rect_superficie'].center = centro_pantalla
    btn_iniciar['rect_texto'].center = centro_pantalla

    btn_opciones['rect_superficie'].center = (centro_pantalla[0], btn_iniciar['rect_superficie'].bottom + 50)
    btn_opciones['rect_texto'].center = (centro_pantalla[0], btn_iniciar['rect_superficie'].bottom + 50)

    btn_salir['rect_superficie'].center = (centro_pantalla[0], btn_opciones['rect_superficie'].bottom + 50)
    btn_salir['rect_texto'].center = (centro_pantalla[0], btn_opciones['rect_superficie'].bottom + 50)

    botones = [btn_iniciar, btn_salir, btn_opciones]

    #pygame.mixer.music.load("assets\musica\OurLordIsNotReady.mp3")
    pygame.mixer.music.load("assets\musica\The-wanderer.mp3")
    pygame.mixer.music.play(start=0, loops=-1)
    pygame.mixer.music.set_volume(0.1)

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
    ancho_pantalla = pantalla.get_width()
    alto_pantalla = pantalla.get_height()
    centro_pantalla = (ancho_pantalla//2, alto_pantalla//2)

    fondo_menu = pygame.image.load("assets/main-menu-background.jpg")
    fondo_menu = pygame.transform.scale(fondo_menu, (ancho_pantalla, alto_pantalla))

    fuente_titulo = Font("assets/fuentes/ENDOR___.ttf", 50)

    texto_opciones = escribir_texto((0, 0), "Opciones", AMARILLO, fuente=fuente_titulo)
    sombra_opciones = escribir_texto((0, 0), "Opciones", ROJO, fuente=fuente_titulo)

    btn_volver = crear_boton((0, 0), "Volver", GRIS_CLARO, BURDEOS, espaciado_y=10, espaciado_x=80)
    btn_parar_musica = crear_boton((0, 0), "Activar/desactivar música", GRIS_CLARO, BURDEOS, espaciado_y=10, espaciado_x=80)
    btn_salir = crear_boton((0, 0), "Salir del juego", GRIS_CLARO, BURDEOS, espaciado_y=10, espaciado_x=80)
    btn_activar_cheats = crear_boton((0, 0), "Activar trucos", GRIS_CLARO, BURDEOS, espaciado_y=10, espaciado_x=80)

    texto_opciones['rect'].center = (centro_pantalla[0], alto_pantalla/4)
    sombra_opciones['rect'].center = (centro_pantalla[0] + 3, alto_pantalla/4 + 3)

    btn_parar_musica['rect_superficie'].center = centro_pantalla
    btn_parar_musica['rect_texto'].center = centro_pantalla

    btn_activar_cheats['rect_superficie'].center = (centro_pantalla[0], btn_parar_musica['rect_superficie'].bottom + 50)
    btn_activar_cheats['rect_texto'].center = (centro_pantalla[0], btn_parar_musica['rect_superficie'].bottom + 50)

    btn_volver['rect_superficie'].center = (centro_pantalla[0], btn_activar_cheats['rect_superficie'].bottom + 50)
    btn_volver['rect_texto'].center = (centro_pantalla[0], btn_activar_cheats['rect_superficie'].bottom + 50)

    btn_salir['rect_superficie'].center = (centro_pantalla[0], btn_volver['rect_superficie'].bottom + 50)
    btn_salir['rect_texto'].center = (centro_pantalla[0], btn_volver['rect_superficie'].bottom + 50)

    nivel_volumen = crear_rectangulo((50, alto_pantalla - 50), 200, 10, NARANJA, radio_borde=5)
    slider_volumen = crear_circulo((nivel_volumen['rect'].right, nivel_volumen['rect'].centery), 20, BURDEOS)

    botones = [btn_parar_musica, btn_activar_cheats, btn_volver, btn_salir]

    slider_presionado = False

    global musica_activa
    global volumen_general

    while True:
        for evento in pygame.event.get():
            if evento.type == QUIT:
                terminar_juego()
            if hover_circulo(slider_volumen, pygame.mouse.get_pos()):
                if evento.type == MOUSEBUTTONDOWN:
                    slider_presionado = True
                    # slider_volumen['color'] = ROJO
                    # slider_volumen['centro'] = [pygame.mouse.get_pos()[0], slider_volumen['centro'][1]]
                if evento.type == MOUSEBUTTONUP:
                    slider_presionado = False
                    # slider_volumen['color'] = BURDEOS
            else:
                # slider_volumen['color'] = BURDEOS
                slider_presionado = False

            if slider_presionado:
                slider_volumen['color'] = ROJO
                slider_volumen['centro'] = [pygame.mouse.get_pos()[0], slider_volumen['centro'][1]]
                if slider_volumen['centro'][0] < nivel_volumen['rect'].left:
                    slider_volumen['centro'][0] = nivel_volumen['rect'].left
                if slider_volumen['centro'][0] > nivel_volumen['rect'].right:
                    slider_volumen['centro'][0] = nivel_volumen['rect'].right
            else:
                slider_volumen['color'] = BURDEOS
                
            for boton in botones:
                # if boton['rect_superficie'].collidepoint(pygame.mouse.get_pos()):
                if hover(boton['rect_superficie'], pygame.mouse.get_pos()):
                    boton['fondo'].fill(NARANJA)
                    if evento.type == MOUSEBUTTONDOWN:
                        if boton == btn_volver:
                            print("Volver")
                            return
                        elif boton == btn_parar_musica:
                            if musica_activa:
                                musica_activa = False
                                print("Parar musica")
                                pygame.mixer.music.stop()
                            else:
                                musica_activa = True
                                print("Activar música")
                                pygame.mixer.music.play()
                        elif boton == btn_salir:
                            print("Salir")
                            terminar_juego()
                else:
                    boton['fondo'].fill(BURDEOS)

        pantalla.blit(fondo_menu, (0, 0))

        for boton in botones:
            blitear_boton(pantalla, boton)
            blitear_boton(pantalla, boton)

        blitear_texto(pantalla, sombra_opciones)
        blitear_texto(pantalla, texto_opciones)

        dibujar_rectangulo(pantalla, nivel_volumen)
        dibujar_circulo(pantalla, slider_volumen)

        pygame.display.flip()

# TODO intentar calcular la escala/map del volumen