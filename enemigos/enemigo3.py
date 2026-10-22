import math
from pathlib import Path

import pygame

from config import IMPACTOS_PARA_ELIMINAR, VIDA_ENEMIGOS


class Enemigo3:
    def __init__(self, ancho_mapa, alto_mapa, x_inicial, altura_central, fase=0, direccion=1):
        ruta_imagen = Path(__file__).resolve().parent.parent / "assets" / "Enemigo-3.png"
        imagen = pygame.image.load(str(ruta_imagen)).convert_alpha()
        regiones = pygame.mask.from_surface(imagen).get_bounding_rects()
        area_enemigo = max(regiones, key=lambda rect: rect.width * rect.height)
        imagen = imagen.subsurface(area_enemigo)
        self.ancho = 92
        self.alto = round(self.ancho * imagen.get_height() / imagen.get_width())
        if ancho_mapa < self.ancho or alto_mapa < self.alto:
            raise ValueError("El mapa debe ser suficientemente grande para el enemigo")
        self.imagen = pygame.transform.smoothscale(imagen, (self.ancho, self.alto))
        self.ancho_mapa = ancho_mapa
        self.alto_mapa = alto_mapa
        self.tipo = "enemigo3"
        self.amplitud = 60
        self.frecuencia = 2 * math.pi / 160
        self.fase = fase
        self.altura_minima = self.amplitud
        self.altura_maxima = max(self.altura_minima, alto_mapa // 2 - self.alto)
        self.altura_central = max(self.altura_minima, min(altura_central, self.altura_maxima))
        self.altura_objetivo = self.altura_central
        self.paso_fila = 50
        self.sentido_vertical = 1
        self.velocidad_vertical = 60
        self.x = max(0, min(x_inicial, ancho_mapa - self.ancho))
        self.y = self.calcular_y(self.x)
        self.direccion = 1 if direccion >= 0 else -1
        self.separacion = 10
        self.velocidad = 150
        self.vida_maxima = VIDA_ENEMIGOS[self.tipo]
        self.vida = self.vida_maxima
        self.dano_por_municion = self.calcular_dano_por_municion()

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

    def calcular_y(self, x):
        return self.amplitud * math.sin(self.frecuencia * x + self.fase) + self.altura_central

    def cambiar_fila(self):
        self.altura_objetivo += self.sentido_vertical * self.paso_fila
        if self.altura_objetivo >= self.altura_maxima:
            self.altura_objetivo = self.altura_maxima
            self.sentido_vertical = -1
        elif self.altura_objetivo <= self.altura_minima:
            self.altura_objetivo = self.altura_minima
            self.sentido_vertical = 1

    def acercar_altura(self, tiempo_transcurrido):
        diferencia = self.altura_objetivo - self.altura_central
        paso = self.velocidad_vertical * tiempo_transcurrido
        if abs(diferencia) <= paso:
            self.altura_central = self.altura_objetivo
        elif diferencia > 0:
            self.altura_central += paso
        else:
            self.altura_central -= paso

    def calcular_movimiento(self, tiempo_transcurrido):
        nueva_x = self.x + self.direccion * self.velocidad * tiempo_transcurrido
        if nueva_x <= 0:
            nueva_x = 0
            self.direccion = 1
            self.cambiar_fila()
        elif nueva_x >= self.ancho_mapa - self.ancho:
            nueva_x = self.ancho_mapa - self.ancho
            self.direccion = -1
            self.cambiar_fila()
        return nueva_x, self.calcular_y(nueva_x)

    def actualizar(self, tiempo_transcurrido, otros_enemigos=()):
        if not self.vivo or tiempo_transcurrido <= 0:
            return
        self.acercar_altura(tiempo_transcurrido)
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
