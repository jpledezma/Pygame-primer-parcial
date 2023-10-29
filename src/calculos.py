from math import sqrt, pow

def calcular_hipotenusa(cateto_1:int | float, cateto_2:int | float) -> float:
    hipotenusa = sqrt((pow(cateto_1, 2) + pow(cateto_2, 2)))

    return hipotenusa

def calcular_distancia(punto_1:tuple[int, int], punto_2:tuple[int, int]) -> float:
    distancia_x = abs(punto_1[0] - punto_2[0])
    distancia_y = abs(punto_1[1] - punto_2[1])

    distancia_total = calcular_hipotenusa(distancia_x, distancia_y)

    return distancia_total

def calcular_escala(valor:int | float, inicio:int | float, fin:int | float) -> float:
    if inicio != 0:
        # "Desplazar" la recta hacia la izquierda o derecha, para que el inicio quede en 0
        fin = fin - inicio
        valor = valor - inicio
        inicio = 0

    # Regla de 3 simple
    porcentaje_valor = valor * 100 / fin

    return porcentaje_valor

def calcular_posicion_recta(porcentaje: int | float, inicio: int | float, fin: int | float):
    porcentaje /= 100
    posicion = inicio + porcentaje * (fin - inicio)
    
    return posicion