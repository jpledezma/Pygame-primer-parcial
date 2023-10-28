import pygame

def blitear_boton(superficie:pygame.Surface, boton:dict):
    superficie.blit(boton['fondo'], boton['rect_superficie'])
    superficie.blit(boton['texto'], boton['rect_texto'])

