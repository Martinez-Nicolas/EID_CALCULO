import random

import pygame


class FondoEstelar:
    def __init__(self, ancho, alto, cantidad=90):
        self.ancho = ancho
        self.alto = alto
        self.estrellas = []
        for _ in range(cantidad):
            self.estrellas.append(self.crear_estrella(random.uniform(0, alto)))

    def crear_estrella(self, y=0):
        profundidad = random.choice((1, 2, 3))
        colores = ((100, 110, 150), (160, 170, 210), (225, 230, 255))
        return [
            random.uniform(0, self.ancho),
            y,
            35 + profundidad * 45,
            profundidad,
            colores[profundidad - 1],
        ]

    def actualizar(self, tiempo_transcurrido):
        for estrella in self.estrellas:
            estrella[1] += estrella[2] * tiempo_transcurrido
            if estrella[1] >= self.alto:
                estrella[0] = random.uniform(0, self.ancho)
                estrella[1] -= self.alto

    def dibujar(self, pantalla):
        for x, y, _, radio, color in self.estrellas:
            pygame.draw.circle(pantalla, color, (round(x), round(y)), radio)
