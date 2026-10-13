import pygame


class MunicionParabolica:
    def __init__(self, centro_x, origen_y, ancho_mapa, alto_mapa):
        self.ancho = 10
        self.alto = 10
        self.origen_x = centro_x - self.ancho / 2
        self.origen_y = origen_y - self.alto
        self.x = self.origen_x
        self.y = self.origen_y
        self.ancho_mapa = ancho_mapa
        self.alto_mapa = alto_mapa
        self.velocidad_x = 100
        self.velocidad_y = -600
        self.gravedad = 360
        self.tiempo = 0
        self.tipo = "parabolica"
        self.activa = origen_y > 0

    @property
    def rect(self):
        return pygame.Rect(round(self.x), round(self.y), self.ancho, self.alto)

    def actualizar(self, tiempo_transcurrido):
        if not self.activa or tiempo_transcurrido <= 0:
            return
        self.tiempo += tiempo_transcurrido
        self.x = self.origen_x + self.velocidad_x * self.tiempo
        self.y = (
            self.origen_y
            + self.velocidad_y * self.tiempo
            + self.gravedad * self.tiempo ** 2 / 2
        )
        if (
            self.x + self.ancho <= 0
            or self.x >= self.ancho_mapa
            or self.y + self.alto <= 0
            or self.y >= self.alto_mapa
        ):
            self.activa = False

    def dibujar(self, pantalla):
        if self.activa:
            rect = self.rect
            pygame.draw.polygon(pantalla, (255, 140, 50), [
                rect.midtop,
                rect.midright,
                rect.midbottom,
                rect.midleft,
            ])
