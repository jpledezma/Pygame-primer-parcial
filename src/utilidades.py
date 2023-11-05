from pygame import Rect, quit
from calculos import calcular_distancia

def terminar_juego():
    """ Des-inicializar los modulos de pygame y finalizar el programa """
    # Salir de pygame
    quit()
    # Salir del programa
    exit()

def hover(rect:Rect, punto:tuple[int, int]) -> bool:
    """ Detectar si un punto esta dentro de un rectangulo """
    if rect.collidepoint(punto):
        return True
    return False

def hover_circulo(circulo:dict, punto:tuple[int, int]) -> bool:
    """ Detectar si un punto esta dentro de un circulo """
    distancia = calcular_distancia(circulo['centro'], punto)
    if distancia <= circulo['radio']:
        return True
    return False
