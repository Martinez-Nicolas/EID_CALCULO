import pygame

from config import ANCHO, ALTO, FPS, TITULO, COLOR_FONDO, PUNTOS_ENEMIGOS
from enemigos.enemigo1 import Enemigo1
from enemigos.enemigo2 import Enemigo2
from enemigos.enemigo3 import Enemigo3
from enemigos.jefe import Jefe
from nucleo.colisiones import GestorColisiones
from nucleo.efectos import GestorEfectos
from nucleo.fondo import FondoEstelar
from nucleo.mapa import Mapa
from nucleo.oleadas import GestorOleadas
from nucleo.sonido import GestorSonido
from nave.nave import Nave


def crear_partida(mapa):
    nave = Nave(ANCHO, ALTO)
    fabricas = {
        1: lambda x, y: Enemigo1(ANCHO, ALTO, x, 280),
        2: lambda x, y: Enemigo2(ANCHO, ALTO, x),
        3: lambda x, y: Enemigo3(ANCHO, ALTO, x, 300),
        "jefe": lambda x, y: Jefe(ANCHO, ALTO),
    }
    gestor_oleadas = GestorOleadas(mapa, fabricas)
    gestor_colisiones = GestorColisiones()
    return nave, gestor_oleadas, gestor_colisiones


def crear_fuentes():
    return {
        "titulo": pygame.font.Font(None, 86),
        "grande": pygame.font.Font(None, 100),
        "subtitulo": pygame.font.Font(None, 42),
        "texto": pygame.font.Font(None, 30),
        "pequena": pygame.font.Font(None, 24),
    }


def dibujar_capa(pantalla, transparencia=190):
    capa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    capa.fill((0, 0, 0, transparencia))
    pantalla.blit(capa, (0, 0))


def dibujar_inicio(pantalla, fuentes):
    dibujar_capa(pantalla, 205)
    titulo = fuentes["titulo"].render("JUEGO ARCADE", True, (110, 210, 255))
    pantalla.blit(titulo, titulo.get_rect(center=(ANCHO // 2, 105)))
    controles = (
        "FLECHAS  -  MOVER",
        "ESPACIO  -  DISPARO BASICO",
        "X  -  DISPARO PARABOLICO",
        "C  -  DISPARO HIPERBOLICO",
        "P  -  PAUSA",
    )
    for indice, texto in enumerate(controles):
        imagen = fuentes["texto"].render(texto, True, (225, 230, 255))
        pantalla.blit(imagen, imagen.get_rect(center=(ANCHO // 2, 220 + indice * 42)))
    comenzar = fuentes["subtitulo"].render("ENTER - COMENZAR", True, (80, 230, 130))
    pantalla.blit(comenzar, comenzar.get_rect(center=(ANCHO // 2, 490)))


def dibujar_pausa(pantalla, fuentes):
    dibujar_capa(pantalla, 220)
    panel = pygame.Rect(200, 205, 400, 185)
    pygame.draw.rect(pantalla, (10, 10, 30), panel, border_radius=12)
    pygame.draw.rect(pantalla, (110, 210, 255), panel, 2, border_radius=12)
    titulo = fuentes["grande"].render("PAUSA", True, (110, 210, 255))
    opcion = fuentes["texto"].render("P - CONTINUAR     ESC - SALIR", True, (235, 235, 245))
    pantalla.blit(titulo, titulo.get_rect(center=(ANCHO // 2, ALTO // 2 - 35)))
    pantalla.blit(opcion, opcion.get_rect(center=(ANCHO // 2, ALTO // 2 + 45)))


def dibujar_puntaje(pantalla, puntaje, fuentes):
    texto = fuentes["pequena"].render(f"PUNTOS {puntaje:06d}", True, (255, 230, 120))
    pantalla.blit(texto, texto.get_rect(midtop=(ANCHO // 2, 12)))


def dibujar_resultado(pantalla, mensaje, puntaje, fuentes):
    dibujar_capa(pantalla, 175)
    color = (80, 230, 130) if mensaje == "YOU WIN" else (240, 70, 80)
    titulo = fuentes["grande"].render(mensaje, True, color)
    puntos = fuentes["subtitulo"].render(f"PUNTAJE: {puntaje}", True, (255, 230, 120))
    opcion = fuentes["texto"].render("R - REINICIAR     ESC - SALIR", True, (235, 235, 245))
    pantalla.blit(titulo, titulo.get_rect(center=(ANCHO // 2, ALTO // 2 - 70)))
    pantalla.blit(puntos, puntos.get_rect(center=(ANCHO // 2, ALTO // 2 + 10)))
    pantalla.blit(opcion, opcion.get_rect(center=(ANCHO // 2, ALTO // 2 + 70)))


def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption(TITULO)
    reloj = pygame.time.Clock()
    fuentes = crear_fuentes()
    mapa = Mapa(ANCHO, ALTO)
    fondo = FondoEstelar(ANCHO, ALTO)
    efectos = GestorEfectos()
    nave, gestor_oleadas, gestor_colisiones = crear_partida(mapa)
    sonido = GestorSonido()
    estado = "inicio"
    puntaje = 0
    sonido.reproducir_musica("juego")

    ejecutando = True
    while ejecutando:
        dt = reloj.tick(FPS) / 1000

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False
                elif evento.key == pygame.K_RETURN and estado == "inicio":
                    estado = "jugando"
                elif evento.key == pygame.K_p and estado == "jugando":
                    estado = "pausa"
                    sonido.pausar()
                elif evento.key == pygame.K_p and estado == "pausa":
                    estado = "jugando"
                    sonido.reanudar()
                elif evento.key == pygame.K_r and estado in ("YOU WIN", "YOU LOSE"):
                    nave, gestor_oleadas, gestor_colisiones = crear_partida(mapa)
                    efectos = GestorEfectos()
                    puntaje = 0
                    estado = "jugando"
                    sonido.reproducir_musica("juego")

        if estado != "pausa":
            fondo.actualizar(dt)
            efectos.actualizar(dt)
        if estado == "jugando":
            disparos = nave.actualizar(pygame.key.get_pressed(), dt)
            for tipo_disparo in disparos:
                sonido.reproducir_disparo(tipo_disparo)
            disparos_enemigos = gestor_oleadas.actualizar(dt)
            for tipo_disparo in disparos_enemigos:
                sonido.reproducir_disparo(tipo_disparo)
            vida_anterior = nave.vida
            eliminados = gestor_colisiones.actualizar(nave, gestor_oleadas.enemigos)
            for enemigo in eliminados:
                efectos.crear_explosion(enemigo.rect.center, enemigo.tipo)
                puntaje += PUNTOS_ENEMIGOS[enemigo.tipo]
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
        if estado != "inicio":
            gestor_oleadas.dibujar(pantalla)
            nave.dibujar(pantalla)
            nave.dibujar_vida(pantalla)
            dibujar_puntaje(pantalla, puntaje, fuentes)
            efectos.dibujar(pantalla)
        if estado == "inicio":
            dibujar_inicio(pantalla, fuentes)
        elif estado == "pausa":
            dibujar_pausa(pantalla, fuentes)
        elif estado in ("YOU WIN", "YOU LOSE"):
            dibujar_resultado(pantalla, estado, puntaje, fuentes)
        pygame.display.flip()

    sonido.detener_musica()
    pygame.quit()


if __name__ == "__main__":
    main()
