from math import sqrt, pow

def calcular_hipotenusa(cateto_1:int | float, cateto_2:int | float) -> float:
    """Calcular la hipotenusa de un triangulo rectangulo

    Args:
        cateto_1 (int | float): primer cateto del triangulo
        cateto_2 (int | float): segundo cateto del triangulo

    Returns:
        float: hipotenusa del triangulo
    """
    hipotenusa = sqrt((pow(cateto_1, 2) + pow(cateto_2, 2)))

    return hipotenusa

def calcular_distancia(punto_1:tuple[int, int], punto_2:tuple[int, int]) -> float:
    """Calcular la distancia entre 2 puntos

    Args:
        punto_1 (tuple[int, int]): Coordenada del primer punto
        punto_2 (tuple[int, int]): Coordenada del segundo punto

    Returns:
        float: distancia total entre los puntos
    """
    distancia_x = abs(punto_1[0] - punto_2[0])
    distancia_y = abs(punto_1[1] - punto_2[1])

    distancia_total = calcular_hipotenusa(distancia_x, distancia_y)

    return distancia_total

def calcular_porcentaje_recta(valor:int | float, inicio:int | float, fin:int | float) -> float:
    """Calcular el porcentaje de la posicion de un punto en una recta

    Args:
        valor (int | float): Posicion absoluta del punto
        inicio (int | float): Punto de inicio de la recta
        fin (int | float): Punto final de la recta

    Returns:
        float: Porcentaje de la posicion del punto en la recta
    """
    if inicio == fin:
        return 0
    if inicio != 0:
        # "Desplazar" la recta hacia la izquierda o derecha, para que el inicio quede en 0
        fin = fin - inicio
        valor = valor - inicio
        inicio = 0

    # Regla de 3 simple
    porcentaje_valor = valor * 100 / fin

    return porcentaje_valor

def calcular_posicion_recta(porcentaje: int | float, inicio: int | float, fin: int | float) -> float:
    """Calcula la coordenada absoluta de un punto de una recta en base al porcentaje de su posicion en la misma

    Args:
        porcentaje (int | float): Porcentaje de la posicion del punto en la recta
        inicio (int | float): Punto de inicio de la recta
        fin (int | float): Punto final de la recta

    Returns:
        float: Posicion absoluta del punto
    """
    porcentaje /= 100
    posicion = inicio + porcentaje * (fin - inicio)
    
    return posicion

def regla_3_simple(valor:int | float, maximo_valor:int | float, maximo_equivalente:int | float) -> float:
    """Regla de 3 simple para calcular un valor"""
    return valor * maximo_equivalente / maximo_valor