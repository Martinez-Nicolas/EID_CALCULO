import pygame
from config import COLOR_BORDE, GROSOR_BORDE


class Mapa:
    def __init__(self, ancho, alto):
        self.rect = pygame.Rect(0, 0, ancho, alto)

    def contiene(self, rect):
        return self.rect.contains(rect)

    def fuera_por_completo(self, rect):
        return not self.rect.colliderect(rect)

    def limitar(self, rect):
        rect.clamp_ip(self.rect)
        return rect

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, COLOR_BORDE, self.rect, GROSOR_BORDE)
