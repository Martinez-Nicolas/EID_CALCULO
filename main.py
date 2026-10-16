import sys
import pygame
from config import ANCHO, ALTO, FPS, TITULO, COLOR_FONDO
from enemigos.enemigo1 import Enemigo1
from enemigos.enemigo2 import Enemigo2
from nucleo.colisiones import GestorColisiones
from nucleo.mapa import Mapa
from nave.nave import Nave


def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption(TITULO)
    reloj = pygame.time.Clock()
    mapa = Mapa(ANCHO, ALTO)
    nave = Nave(ANCHO, ALTO)
    enemigos = [
        Enemigo1(ANCHO, ALTO, 80, 170),
        Enemigo2(ANCHO, ALTO, 550),
    ]
    gestor_colisiones = GestorColisiones()

    ejecutando = True
    while ejecutando:
        dt = reloj.tick(FPS) / 1000

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                ejecutando = False

        nave.actualizar(pygame.key.get_pressed(), dt)
        for enemigo in enemigos:
            enemigo.actualizar(dt, enemigos)
        gestor_colisiones.actualizar(nave, enemigos)
        enemigos = [enemigo for enemigo in enemigos if enemigo.vivo]
        if not nave.viva:
            ejecutando = False

        pantalla.fill(COLOR_FONDO)
        mapa.dibujar(pantalla)
        for enemigo in enemigos:
            enemigo.dibujar(pantalla)
        nave.dibujar(pantalla)
        nave.dibujar_vida(pantalla)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
