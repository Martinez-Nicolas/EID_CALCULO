import sys
import pygame
from config import ANCHO, ALTO, FPS, TITULO, COLOR_FONDO
from enemigos.enemigo1 import Enemigo1
from enemigos.enemigo2 import Enemigo2
from enemigos.enemigo3 import Enemigo3
from enemigos.jefe import Jefe
from nucleo.colisiones import GestorColisiones
from nucleo.mapa import Mapa
from nucleo.oleadas import GestorOleadas
from nave.nave import Nave


def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption(TITULO)
    reloj = pygame.time.Clock()
    mapa = Mapa(ANCHO, ALTO)
    nave = Nave(ANCHO, ALTO)
    fabricas = {
        1: lambda x, y: Enemigo1(ANCHO, ALTO, x, 170),
        2: lambda x, y: Enemigo2(ANCHO, ALTO, x),
        3: lambda x, y: Enemigo3(ANCHO, ALTO, x, 120),
        "jefe": lambda x, y: Jefe(ANCHO, ALTO),
    }
    gestor_oleadas = GestorOleadas(mapa, fabricas)
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
        gestor_oleadas.actualizar(dt)
        gestor_colisiones.actualizar(nave, gestor_oleadas.enemigos)
        if not nave.viva or gestor_oleadas.terminado:
            ejecutando = False

        pantalla.fill(COLOR_FONDO)
        mapa.dibujar(pantalla)
        gestor_oleadas.dibujar(pantalla)
        nave.dibujar(pantalla)
        nave.dibujar_vida(pantalla)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
