import pygame

def blitear_boton(pantalla:pygame.Surface, boton:dict):
    """ 'Estampar' un boton encima de la pantalla """
    try:
        pantalla.blit(boton['fondo'], boton['rect_superficie'])
    except:
        print('Los valores del botón están en un formato inválido')

    try:
        pantalla.blit(boton['texto'], boton['rect_texto'])
    except:
        print('Los valores del texto están en un formato inválido')
    

def blitear_texto(pantalla:pygame.Surface, texto:dict):
    """ 'Estampar' un texto encima de la pantalla """
    try:
        pantalla.blit(texto['superficie'], texto['rect'])
    except:
        print('Los valores del texto están en un formato inválido')
    

def blitear_superficie(pantalla:pygame.Surface, superficie:dict):
    """ 'Estampar' una superficie encima de la pantalla """
    try:
        pantalla.blit(superficie['superficie'], superficie['rect'])
    except:
        print('Los valores de la superficie están en un formato inválido')
    

def dibujar_rectangulo(superficie:pygame.Surface, rectangulo:dict) -> None:
    """ Dibujar un rectangulo en la pantalla """
    try:
        pygame.draw.rect(superficie, rectangulo['color'], rectangulo["rect"], rectangulo['ancho_borde'], rectangulo['radio_borde'])
    except:
        print('Los valores del rectángulo están en un formato inválido')
    

def dibujar_circulo(superficie:pygame.Surface, circulo:dict) -> None:
    """ Dibujar un circulo en la pantalla """
    try:
        return pygame.draw.circle(superficie, circulo['color'], circulo['centro'], circulo['radio'], circulo['ancho_borde'])
    except:
        print('Los valores del círculo están en un formato inválido')
    