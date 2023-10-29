from math import sqrt, pow

def calcular_hipotenusa(cateto_1:int | float, cateto_2:int | float) -> float:
    hipotenusa = sqrt((pow(cateto_1, 2) + pow(cateto_2, 2)))

    return hipotenusa

def calcular_distancia(punto_1:tuple[int, int], punto_2:tuple[int, int]) -> float:
    distancia_x = abs(punto_1[0] - punto_2[0])
    distancia_y = abs(punto_1[1] - punto_2[1])

    distancia_total = calcular_hipotenusa(distancia_x, distancia_y)

    return distancia_total