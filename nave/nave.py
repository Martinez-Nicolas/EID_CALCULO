import math

import pygame

from municiones.basica import MunicionBasica


class Nave:
    def __init__(self, ancho_mapa, alto_mapa):
        self.ancho = 40
        self.alto = 48
        if ancho_mapa < self.ancho or alto_mapa < self.alto:
            raise ValueError("El mapa debe ser suficientemente grande para la nave")
        self.ancho_mapa = ancho_mapa
        self.alto_mapa = alto_mapa
        self.x = (ancho_mapa - self.ancho) / 2
        self.y = max(0, alto_mapa - self.alto - 20)
        self.velocidad = 300
        self.vida_maxima = 100
        self.vida = self.vida_maxima
        self.municiones_basicas = []
        self.dano_por_enemigo = {
            "enemigo1": 20,
            "enemigo2": 35,
            "enemigo3": 50,
            "jefe": 100,
        }

    @property
    def viva(self):
        return self.vida > 0

    @property
    def rect(self):
        return pygame.Rect(round(self.x), round(self.y), self.ancho, self.alto)

    def actualizar(self, teclas, tiempo_transcurrido):
        if tiempo_transcurrido <= 0:
            return
        for municion in self.municiones_basicas:
            municion.actualizar(tiempo_transcurrido)
        self.municiones_basicas = [
            municion for municion in self.municiones_basicas if municion.activa
        ]
        if not self.viva:
            return
        direccion_x = int(teclas[pygame.K_RIGHT]) - int(teclas[pygame.K_LEFT])
        direccion_y = int(teclas[pygame.K_DOWN]) - int(teclas[pygame.K_UP])
        longitud = math.sqrt(direccion_x ** 2 + direccion_y ** 2)
        if longitud > 0:
            distancia = self.velocidad * tiempo_transcurrido
            self.x += direccion_x / longitud * distancia
            self.y += direccion_y / longitud * distancia
        self.x = max(0, min(self.x, self.ancho_mapa - self.ancho))
        self.y = max(0, min(self.y, self.alto_mapa - self.alto))
        if teclas[pygame.K_SPACE]:
            self.disparar_basica()

    def disparar_basica(self):
        if not self.viva:
            return None
        municion = MunicionBasica(self.x + self.ancho / 2, self.y)
        self.municiones_basicas.append(municion)
        return municion

    def recibir_impacto(self, tipo_enemigo):
        dano = self.dano_por_enemigo[tipo_enemigo]
        self.vida = max(0, self.vida - dano)

    def dibujar(self, pantalla):
        for municion in self.municiones_basicas:
            municion.dibujar(pantalla)
        if not self.viva:
            return
        x = round(self.x)
        y = round(self.y)
        pygame.draw.polygon(pantalla, (80, 190, 240), [
            (x + 20, y),
            (x + 40, y + 42),
            (x + 27, y + 36),
            (x + 27, y + 48),
            (x + 13, y + 48),
            (x + 13, y + 36),
            (x, y + 42),
        ])
        pygame.draw.polygon(pantalla, (220, 245, 255), [
            (x + 20, y + 10),
            (x + 26, y + 28),
            (x + 14, y + 28),
        ])

    def dibujar_vida(self, pantalla):
        ancho_barra = min(160, self.ancho_mapa - 20)
        ancho_vida = round(ancho_barra * self.vida / self.vida_maxima)
        pygame.draw.rect(pantalla, (60, 60, 70), (10, 10, ancho_barra, 12))
        if ancho_vida > 0:
            pygame.draw.rect(pantalla, (60, 210, 100), (10, 10, ancho_vida, 12))
