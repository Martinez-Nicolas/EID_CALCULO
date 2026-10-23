import math
import random
from pathlib import Path

import pygame

from config import (
    DANO_BALA_JEFE,
    IMPACTOS_PARA_ELIMINAR,
    INTERVALO_MAX_DISPARO_JEFE,
    INTERVALO_MIN_DISPARO_JEFE,
    VIDA_ENEMIGOS,
)
from municiones.basica import MunicionBasicaEnemiga


class Jefe:
    def __init__(self, ancho_mapa, alto_mapa, fase=0):
        ruta_imagen = Path(__file__).resolve().parent.parent / "assets" / "Jefe-Final.png"
        imagen = pygame.image.load(str(ruta_imagen)).convert_alpha()
        regiones = pygame.mask.from_surface(imagen).get_bounding_rects()
        area_jefe = max(regiones, key=lambda rect: rect.width * rect.height)
        imagen = imagen.subsurface(area_jefe)
        self.ancho = 150
        self.alto = round(self.ancho * imagen.get_height() / imagen.get_width())
        self.margen = 20
        if ancho_mapa < self.ancho + 2 * self.margen or alto_mapa < self.alto + 2 * self.margen:
            raise ValueError("El mapa debe ser suficientemente grande para el jefe")
        self.imagen = pygame.transform.smoothscale(imagen, (self.ancho, self.alto))
        self.ancho_mapa = ancho_mapa
        self.alto_mapa = alto_mapa
        self.tipo = "jefe"
        self.amplitud_x = (ancho_mapa - self.ancho) / 2 - self.margen
        self.centro_x = (ancho_mapa - self.ancho) / 2
        self.amplitud_y = 40
        self.centro_y = self.amplitud_y + self.margen
        self.frecuencia = 2 * math.pi / 8
        self.fase = fase
        self.tiempo = 0
        self.x, self.y = self.calcular_posicion(self.tiempo)
        self.direccion = 1
        self.separacion = 10
        self.vida_maxima = VIDA_ENEMIGOS[self.tipo]
        self.vida = self.vida_maxima
        self.dano_por_municion = self.calcular_dano_por_municion()
        self.municiones = []
        self.tiempo_hasta_disparo = random.uniform(
            INTERVALO_MIN_DISPARO_JEFE, INTERVALO_MAX_DISPARO_JEFE
        )

    def calcular_dano_por_municion(self):
        dano_por_municion = {}
        for tipo_municion, impactos in IMPACTOS_PARA_ELIMINAR[self.tipo].items():
            dano_por_municion[tipo_municion] = math.ceil(self.vida_maxima / impactos)
        return dano_por_municion

    @property
    def vivo(self):
        return self.vida > 0

    @property
    def rect(self):
        return pygame.Rect(round(self.x), round(self.y), self.ancho, self.alto)

    def calcular_x(self, t):
        return self.amplitud_x * math.sin(self.frecuencia * t + self.fase) + self.centro_x

    def calcular_y(self, t):
        return self.amplitud_y * math.sin(2 * self.frecuencia * t + self.fase) + self.centro_y

    def calcular_posicion(self, t):
        return self.calcular_x(t), self.calcular_y(t)

    def calcular_movimiento(self, tiempo_transcurrido):
        nuevo_tiempo = self.tiempo + self.direccion * tiempo_transcurrido
        return nuevo_tiempo, self.calcular_posicion(nuevo_tiempo)

    def actualizar(self, tiempo_transcurrido, otros_enemigos=()):
        for municion in self.municiones:
            municion.actualizar(tiempo_transcurrido)
        self.municiones = [municion for municion in self.municiones if municion.activa]
        if not self.vivo or tiempo_transcurrido <= 0:
            return False
        self.tiempo_hasta_disparo -= tiempo_transcurrido
        disparo_realizado = False
        if self.tiempo_hasta_disparo <= 0:
            self.disparar()
            self.tiempo_hasta_disparo = random.uniform(
                INTERVALO_MIN_DISPARO_JEFE, INTERVALO_MAX_DISPARO_JEFE
            )
            disparo_realizado = True
        nuevo_tiempo, (nueva_x, nueva_y) = self.calcular_movimiento(tiempo_transcurrido)
        if self.choca_con(nueva_x, nueva_y, otros_enemigos):
            self.direccion *= -1
            nuevo_tiempo, (nueva_x, nueva_y) = self.calcular_movimiento(tiempo_transcurrido)
            if self.choca_con(nueva_x, nueva_y, otros_enemigos):
                return disparo_realizado
        self.tiempo = nuevo_tiempo
        self.x = nueva_x
        self.y = nueva_y
        return disparo_realizado

    def disparar(self):
        margen = self.ancho * 0.2
        centro_x = random.uniform(self.x + margen, self.x + self.ancho - margen)
        municion = MunicionBasicaEnemiga(
            centro_x, self.y + self.alto, self.alto_mapa, DANO_BALA_JEFE
        )
        self.municiones.append(municion)
        return municion

    def choca_con(self, x, y, otros_enemigos):
        rect_nuevo = pygame.Rect(round(x), round(y), self.ancho, self.alto)
        rect_nuevo.inflate_ip(self.separacion, self.separacion)
        for otro in otros_enemigos:
            if otro is not self and otro.vivo and rect_nuevo.colliderect(otro.rect):
                return True
        return False

    def recibir_impacto(self, tipo_municion):
        dano = self.dano_por_municion[tipo_municion]
        self.vida = max(0, self.vida - dano)

    def dibujar(self, pantalla):
        for municion in self.municiones:
            municion.dibujar(pantalla)
        if not self.vivo:
            return
        pantalla.blit(self.imagen, self.rect)
        self.dibujar_vida(pantalla)

    def dibujar_vida(self, pantalla):
        ancho_vida = round(self.ancho * self.vida / self.vida_maxima)
        x = round(self.x)
        y = round(self.y) - 12
        pygame.draw.rect(pantalla, (60, 60, 70), (x, y, self.ancho, 8))
        if ancho_vida > 0:
            pygame.draw.rect(pantalla, (220, 60, 60), (x, y, ancho_vida, 8))
