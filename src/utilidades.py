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
