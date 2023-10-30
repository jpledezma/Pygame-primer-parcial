import pygame

def blitear_boton(pantalla:pygame.Surface, boton:dict):
    pantalla.blit(boton['fondo'], boton['rect_superficie'])
    pantalla.blit(boton['texto'], boton['rect_texto'])

def blitear_texto(pantalla:pygame.Surface, texto:dict):
    pantalla.blit(texto['superficie'], texto['rect'])

def blitear_superficie(pantalla:pygame.Surface, superficie:dict):
    pantalla.blit(superficie['superficie'], superficie['rect'])

def dibujar_rectangulo(superficie:pygame.Surface, rectangulo:dict) -> None:
    pygame.draw.rect(superficie, rectangulo['color'], rectangulo["rect"], rectangulo['ancho_borde'], rectangulo['radio_borde'])

def dibujar_circulo(superficie:pygame.Surface, circulo:dict) -> None:
    return pygame.draw.circle(superficie, circulo['color'], circulo['centro'], circulo['radio'], circulo['ancho_borde'])