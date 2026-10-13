import math
import pygame
from config import (
    ANCHO,
    COOLDOWN_CONICA,
    CONICA_A,
    CONICA_B,
    CONICA_VELOCIDAD,
    CONICA_RADIO,
)


class MunicionConica:
    def __init__(self, origen_x, origen_y, lado):
        self.a = CONICA_A
        self.b = CONICA_B
        self.lado = lado
        self.h = origen_x - lado * self.a
        self.k = origen_y
        self.t = 0.0
        self.x = origen_x
        self.y = origen_y
        self.radio = CONICA_RADIO
        self.tipo = "conica"
        self.activa = True

    @property
    def rect(self):
        lado = self.radio * 2
        return pygame.Rect(
            round(self.x - self.radio), round(self.y - self.radio), lado, lado
        )

    def actualizar(self, tiempo_transcurrido):
        if not self.activa or tiempo_transcurrido <= 0:
            return
        self.t += CONICA_VELOCIDAD * tiempo_transcurrido
        self.x = self.h + self.lado * self.a * math.cosh(self.t)
        self.y = self.k - self.b * math.sinh(self.t)
        if (
            self.y + self.radio < 0
            or self.x - self.radio > ANCHO
            or self.x + self.radio < 0
        ):
            self.activa = False

    def dibujar(self, pantalla):
        if not self.activa:
            return
        centro = (round(self.x), round(self.y))
        pygame.draw.circle(pantalla, (255, 140, 60), centro, self.radio)
        pygame.draw.circle(pantalla, (255, 230, 180), centro, self.radio // 2)


class LanzadorConica:
    def __init__(self):
        self.municiones = []
        self.espera = 0.0
        self.lado = 1

    @property
    def disponible(self):
        return self.espera <= 0

    @property
    def carga(self):
        return 1 - self.espera / COOLDOWN_CONICA

    def disparar(self, origen_x, origen_y):
        if not self.disponible:
            return None
        municion = MunicionConica(origen_x, origen_y, self.lado)
        self.lado = -self.lado
        self.municiones.append(municion)
        self.espera = COOLDOWN_CONICA
        return municion

    def actualizar(self, tiempo_transcurrido):
        if tiempo_transcurrido <= 0:
            return
        self.espera = max(0.0, self.espera - tiempo_transcurrido)
        for municion in self.municiones:
            municion.actualizar(tiempo_transcurrido)
        self.municiones = [m for m in self.municiones if m.activa]

    def dibujar(self, pantalla):
        for municion in self.municiones:
            municion.dibujar(pantalla)

    def dibujar_recarga(self, pantalla):
        ancho_barra = min(160, pantalla.get_width() - 20)
        pygame.draw.rect(pantalla, (60, 60, 70), (10, 58, ancho_barra, 8))
        ancho_carga = round(ancho_barra * self.carga)
        if ancho_carga > 0:
            color = (150, 90, 220) if not self.disponible else (210, 160, 255)
            pygame.draw.rect(pantalla, color, (10, 58, ancho_carga, 8))
