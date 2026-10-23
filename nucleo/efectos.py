import random

import pygame


class GestorEfectos:
    def __init__(self):
        self.particulas = []

    def crear_explosion(self, centro, tipo):
        colores = {
            "enemigo1": ((150, 80, 255), (90, 230, 255)),
            "enemigo2": ((255, 80, 60), (255, 190, 60)),
            "enemigo3": ((255, 130, 40), (255, 230, 100)),
            "jefe": ((255, 40, 50), (255, 180, 40)),
        }
        cantidad = 55 if tipo == "jefe" else 20
        velocidad = 240 if tipo == "jefe" else 150
        for _ in range(cantidad):
            vida = random.uniform(0.35, 0.9 if tipo == "jefe" else 0.65)
            self.particulas.append([
                float(centro[0]),
                float(centro[1]),
                random.uniform(-velocidad, velocidad),
                random.uniform(-velocidad, velocidad),
                vida,
                vida,
                random.choice(colores[tipo]),
                random.randint(2, 6 if tipo == "jefe" else 4),
            ])

    def actualizar(self, tiempo_transcurrido):
        for particula in self.particulas:
            particula[0] += particula[2] * tiempo_transcurrido
            particula[1] += particula[3] * tiempo_transcurrido
            particula[3] += 80 * tiempo_transcurrido
            particula[4] -= tiempo_transcurrido
        self.particulas = [particula for particula in self.particulas if particula[4] > 0]

    def dibujar(self, pantalla):
        for x, y, _, _, vida, vida_maxima, color, radio in self.particulas:
            proporcion = vida / vida_maxima
            color_actual = tuple(round(componente * proporcion) for componente in color)
            radio_actual = max(1, round(radio * proporcion))
            pygame.draw.circle(pantalla, color_actual, (round(x), round(y)), radio_actual)
