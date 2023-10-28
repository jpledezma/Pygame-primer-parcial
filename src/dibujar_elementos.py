import pygame

def blitear_boton(pantalla:pygame.Surface, boton:dict):
    pantalla.blit(boton['fondo'], boton['rect_superficie'])
    pantalla.blit(boton['texto'], boton['rect_texto'])

def blitear_texto(pantalla:pygame.Surface, texto:dict):
    pantalla.blit(texto['superficie'], texto['rect'])

def blitear_superficie(pantalla:pygame.Surface, superficie:pygame.Surface):
    pantalla.blit(superficie['superficie'], superficie['rect'])

