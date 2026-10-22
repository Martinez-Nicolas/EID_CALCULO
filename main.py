import sys

import pygame

from config import ANCHO, ALTO, FPS, TITULO, COLOR_FONDO
from enemigos.enemigo1 import Enemigo1
from enemigos.enemigo2 import Enemigo2
from enemigos.enemigo3 import Enemigo3
from enemigos.jefe import Jefe
from nucleo.colisiones import GestorColisiones
from nucleo.fondo import FondoEstelar
from nucleo.mapa import Mapa
from nucleo.oleadas import GestorOleadas
from nucleo.sonido import GestorSonido
from nave.nave import Nave


def crear_partida(mapa):
    nave = Nave(ANCHO, ALTO)
    fabricas = {
        1: lambda x, y: Enemigo1(ANCHO, ALTO, x, 170),
        2: lambda x, y: Enemigo2(ANCHO, ALTO, x),
        3: lambda x, y: Enemigo3(ANCHO, ALTO, x, 120),
        "jefe": lambda x, y: Jefe(ANCHO, ALTO),
    }
    gestor_oleadas = GestorOleadas(mapa, fabricas)
    gestor_colisiones = GestorColisiones()
    return nave, gestor_oleadas, gestor_colisiones


def dibujar_resultado(pantalla, mensaje):
    capa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    capa.fill((0, 0, 0, 175))
    pantalla.blit(capa, (0, 0))
    fuente_titulo = pygame.font.Font(None, 100)
    fuente_opcion = pygame.font.Font(None, 34)
    color = (80, 230, 130) if mensaje == "YOU WIN" else (240, 70, 80)
    titulo = fuente_titulo.render(mensaje, True, color)
    opcion = fuente_opcion.render("R - REINICIAR     ESC - SALIR", True, (235, 235, 245))
    pantalla.blit(titulo, titulo.get_rect(center=(ANCHO // 2, ALTO // 2 - 35)))
    pantalla.blit(opcion, opcion.get_rect(center=(ANCHO // 2, ALTO // 2 + 45)))


def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption(TITULO)
    reloj = pygame.time.Clock()
    mapa = Mapa(ANCHO, ALTO)
    fondo = FondoEstelar(ANCHO, ALTO)
    nave, gestor_oleadas, gestor_colisiones = crear_partida(mapa)
    sonido = GestorSonido()
    estado = "jugando"
    sonido.reproducir_musica("juego")

    ejecutando = True
    while ejecutando:
        dt = reloj.tick(FPS) / 1000

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_r and estado != "jugando":
                nave, gestor_oleadas, gestor_colisiones = crear_partida(mapa)
                estado = "jugando"
                sonido.reproducir_musica("juego")

        fondo.actualizar(dt)
        if estado == "jugando":
            disparos = nave.actualizar(pygame.key.get_pressed(), dt)
            for tipo_disparo in disparos:
                sonido.reproducir_disparo(tipo_disparo)
            gestor_oleadas.actualizar(dt)
            vida_anterior = nave.vida
            gestor_colisiones.actualizar(nave, gestor_oleadas.enemigos)
            if nave.vida < vida_anterior:
                sonido.reproducir_dano()
            if not nave.viva:
                estado = "YOU LOSE"
                sonido.reproducir_musica("derrota")
            elif gestor_oleadas.terminado:
                estado = "YOU WIN"
                sonido.reproducir_musica("victoria")

        pantalla.fill(COLOR_FONDO)
        fondo.dibujar(pantalla)
        mapa.dibujar(pantalla)
        gestor_oleadas.dibujar(pantalla)
        nave.dibujar(pantalla)
        nave.dibujar_vida(pantalla)
        if estado != "jugando":
            dibujar_resultado(pantalla, estado)
        pygame.display.flip()

    sonido.detener_musica()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
