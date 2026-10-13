import pygame


class MunicionBasica:
    def __init__(self, centro_x, origen_y):
        self.ancho = 4
        self.alto = 6
        self.x = centro_x - self.ancho / 2
        self.y = origen_y - self.alto
        self.velocidad = 600
        self.tipo = "basica"
        self.activa = origen_y > 0

    @property
    def rect(self):
        return pygame.Rect(round(self.x), round(self.y), self.ancho, self.alto)

    def actualizar(self, tiempo_transcurrido):
        if not self.activa or tiempo_transcurrido <= 0:
            return
        self.y -= self.velocidad * tiempo_transcurrido
        if self.y + self.alto <= 0:
            self.activa = False

    def dibujar(self, pantalla):
        if self.activa:
            pygame.draw.rect(pantalla, (255, 230, 100), self.rect)
