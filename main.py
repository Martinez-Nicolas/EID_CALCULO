import sys
import pygame
from config import ANCHO, ALTO, FPS, TITULO, COLOR_FONDO
from nucleo.mapa import Mapa


def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption(TITULO)
    reloj = pygame.time.Clock()
    mapa = Mapa(ANCHO, ALTO)

    ejecutando = True
    while ejecutando:
        dt = reloj.tick(FPS) / 1000

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                ejecutando = False

        pantalla.fill(COLOR_FONDO)
        mapa.dibujar(pantalla)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
