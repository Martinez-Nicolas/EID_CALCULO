import math
from pathlib import Path

import pygame


class Enemigo2:
    def __init__(self, ancho_mapa, alto_mapa, x_central, fase=0):
        ruta_imagen = Path(__file__).resolve().parent.parent / "assets" / "Enemigo-2.png"
        imagen = pygame.image.load(str(ruta_imagen)).convert_alpha()
        regiones = pygame.mask.from_surface(imagen).get_bounding_rects()
        area_enemigo = max(regiones, key=lambda rect: rect.width * rect.height)
        imagen = imagen.subsurface(area_enemigo)
        self.ancho = 74
        self.alto = round(self.ancho * imagen.get_height() / imagen.get_width())
        if ancho_mapa < self.ancho or alto_mapa < self.alto:
            raise ValueError("El mapa debe ser suficientemente grande para el enemigo")
        self.imagen = pygame.transform.smoothscale(imagen, (self.ancho, self.alto))
        self.ancho_mapa = ancho_mapa
        self.alto_mapa = alto_mapa
        self.tipo = "enemigo2"
        self.amplitud = 80
        self.frecuencia = 2 * math.pi / 200
        self.fase = fase
        columna_minima = self.amplitud
        columna_maxima = ancho_mapa - self.ancho - self.amplitud
        self.columna_central = max(columna_minima, min(x_central, columna_maxima))
        self.y_minima = 0
        self.y_maxima = max(0, alto_mapa // 2 - self.alto)
        self.y = self.y_minima
        self.x = self.calcular_x(self.y)
        self.direccion = 1
        self.separacion = 10
        self.velocidad = 70
        self.vida_maxima = 60
        self.vida = self.vida_maxima
        self.dano_por_municion = {
            "basica": 10,
            "parabolica": 20,
            "conica": 30,
        }

    @property
    def vivo(self):
        return self.vida > 0

    @property
    def rect(self):
        return pygame.Rect(round(self.x), round(self.y), self.ancho, self.alto)

    def calcular_x(self, y):
        return self.amplitud * math.sin(self.frecuencia * y + self.fase) + self.columna_central

    def calcular_movimiento(self, tiempo_transcurrido):
        nueva_y = self.y + self.direccion * self.velocidad * tiempo_transcurrido
        if nueva_y <= self.y_minima:
            nueva_y = self.y_minima
            self.direccion = 1
        elif nueva_y >= self.y_maxima:
            nueva_y = self.y_maxima
            self.direccion = -1
        return self.calcular_x(nueva_y), nueva_y

    def actualizar(self, tiempo_transcurrido, otros_enemigos=()):
        if not self.vivo or tiempo_transcurrido <= 0:
            return
        nueva_x, nueva_y = self.calcular_movimiento(tiempo_transcurrido)
        if self.choca_con(nueva_x, nueva_y, otros_enemigos):
            self.direccion *= -1
            nueva_x, nueva_y = self.calcular_movimiento(tiempo_transcurrido)
            if self.choca_con(nueva_x, nueva_y, otros_enemigos):
                return
        self.x = nueva_x
        self.y = nueva_y

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
        if not self.vivo:
            return
        pantalla.blit(self.imagen, self.rect)
        self.dibujar_vida(pantalla)

    def dibujar_vida(self, pantalla):
        ancho_vida = round(self.ancho * self.vida / self.vida_maxima)
        x = round(self.x)
        y = round(self.y) - 8
        pygame.draw.rect(pantalla, (60, 60, 70), (x, y, self.ancho, 5))
        if ancho_vida > 0:
            pygame.draw.rect(pantalla, (220, 60, 60), (x, y, ancho_vida, 5))
