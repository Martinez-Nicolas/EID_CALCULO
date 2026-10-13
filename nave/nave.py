import math
from pathlib import Path

import pygame

from municiones.basica import MunicionBasica
from municiones.conica import LanzadorConica
from municiones.parabolica import MunicionParabolica


class Nave:
    def __init__(self, ancho_mapa, alto_mapa):
        ruta_imagen = Path(__file__).resolve().parent.parent / "assets" / "nave.png"
        imagen = pygame.image.load(str(ruta_imagen))
        regiones = pygame.mask.from_surface(imagen).get_bounding_rects()
        area_nave = max(regiones, key=lambda rect: rect.width * rect.height)
        imagen = imagen.subsurface(area_nave)
        self.ancho = 72
        self.alto = round(self.ancho * area_nave.height / area_nave.width)
        if ancho_mapa < self.ancho or alto_mapa < self.alto:
            raise ValueError("El mapa debe ser suficientemente grande para la nave")
        self.imagen = pygame.transform.smoothscale(
            imagen, (self.ancho, self.alto)
        )
        self.ancho_mapa = ancho_mapa
        self.alto_mapa = alto_mapa
        self.x = (ancho_mapa - self.ancho) / 2
        self.y = max(0, alto_mapa - self.alto - 20)
        self.velocidad = 300
        self.vida_maxima = 100
        self.vida = self.vida_maxima
        self.municiones_basicas = []
        self.lanzador_conica = LanzadorConica()
        self.municiones_parabolicas = []
        self.maximo_parabolicas = 3
        self.cargas_parabolicas = self.maximo_parabolicas
        self.cooldown_parabolica = 5
        self.tiempo_recarga_parabolica = 0
        self.recargando_parabolicas = False
        self.tecla_parabolica_pulsada = False
        self.dano_por_enemigo = {
            "enemigo1": 20,
            "enemigo2": 35,
            "enemigo3": 50,
            "jefe": 100,
        }

    @property
    def viva(self):
        return self.vida > 0

    @property
    def rect(self):
        return pygame.Rect(round(self.x), round(self.y), self.ancho, self.alto)

    def actualizar(self, teclas, tiempo_transcurrido):
        if tiempo_transcurrido <= 0:
            return
        for municion in self.municiones_basicas:
            municion.actualizar(tiempo_transcurrido)
        self.municiones_basicas = [
            municion for municion in self.municiones_basicas if municion.activa
        ]
        self.lanzador_conica.actualizar(tiempo_transcurrido)
        for municion in self.municiones_parabolicas:
            municion.actualizar(tiempo_transcurrido)
        self.municiones_parabolicas = [
            municion for municion in self.municiones_parabolicas if municion.activa
        ]
        if not self.viva:
            return
        self.actualizar_recarga_parabolica(tiempo_transcurrido)
        direccion_x = int(teclas[pygame.K_RIGHT]) - int(teclas[pygame.K_LEFT])
        direccion_y = int(teclas[pygame.K_DOWN]) - int(teclas[pygame.K_UP])
        longitud = math.sqrt(direccion_x**2 + direccion_y**2)
        if longitud > 0:
            distancia = self.velocidad * tiempo_transcurrido
            self.x += direccion_x / longitud * distancia
            self.y += direccion_y / longitud * distancia
        self.x = max(0, min(self.x, self.ancho_mapa - self.ancho))
        self.y = max(0, min(self.y, self.alto_mapa - self.alto))
        if teclas[pygame.K_SPACE]:
            self.disparar_basica()
        if teclas[pygame.K_c]:
            self.lanzador_conica.disparar(self.x + self.ancho / 2, self.y)
        if teclas[pygame.K_x] and not self.tecla_parabolica_pulsada:
            self.disparar_parabolica()
        self.tecla_parabolica_pulsada = bool(teclas[pygame.K_x])

    def disparar_basica(self):
        if not self.viva:
            return None
        municion = MunicionBasica(self.x + self.ancho / 2, self.y)
        self.municiones_basicas.append(municion)
        return municion

    def disparar_parabolica(self):
        if not self.viva or self.cargas_parabolicas <= 0:
            return None
        municion = MunicionParabolica(
            self.x + self.ancho / 2, self.y, self.ancho_mapa, self.alto_mapa
        )
        self.municiones_parabolicas.append(municion)
        self.cargas_parabolicas -= 1
        if self.cargas_parabolicas == 0 and not self.recargando_parabolicas:
            self.recargando_parabolicas = True
            self.tiempo_recarga_parabolica = 0
        return municion

    def actualizar_recarga_parabolica(self, tiempo_transcurrido):
        if not self.viva or not self.recargando_parabolicas or tiempo_transcurrido <= 0:
            return
        self.tiempo_recarga_parabolica += tiempo_transcurrido
        while (
            self.cargas_parabolicas < self.maximo_parabolicas
            and self.tiempo_recarga_parabolica >= self.cooldown_parabolica - 1e-9
        ):
            self.cargas_parabolicas += 1
            self.tiempo_recarga_parabolica = max(
                0, self.tiempo_recarga_parabolica - self.cooldown_parabolica
            )
        if self.cargas_parabolicas == self.maximo_parabolicas:
            self.recargando_parabolicas = False
            self.tiempo_recarga_parabolica = 0

    def recibir_impacto(self, tipo_enemigo):
        dano = self.dano_por_enemigo[tipo_enemigo]
        self.vida = max(0, self.vida - dano)

    def dibujar(self, pantalla):
        for municion in self.municiones_basicas:
            municion.dibujar(pantalla)
        self.lanzador_conica.dibujar(pantalla)
        for municion in self.municiones_parabolicas:
            municion.dibujar(pantalla)
        if not self.viva:
            return
        pantalla.blit(self.imagen, self.rect)

    def dibujar_vida(self, pantalla):
        ancho_barra = min(160, self.ancho_mapa - 20)
        ancho_vida = round(ancho_barra * self.vida / self.vida_maxima)
        pygame.draw.rect(pantalla, (60, 60, 70), (10, 10, ancho_barra, 12))
        if ancho_vida > 0:
            pygame.draw.rect(pantalla, (60, 210, 100), (10, 10, ancho_vida, 12))
        self.lanzador_conica.dibujar_recarga(pantalla)
        self.dibujar_municiones(pantalla)

    def dibujar_municiones(self, pantalla):
        ancho_indicador = min(14, (self.ancho_mapa - 28) // self.maximo_parabolicas)
        for indice in range(self.maximo_parabolicas):
            color = (255, 140, 50) if indice < self.cargas_parabolicas else (60, 60, 70)
            pygame.draw.rect(pantalla, color, (
                10 + indice * (ancho_indicador + 4), 30, ancho_indicador, 10
            ))
        if self.recargando_parabolicas:
            ancho_barra = self.maximo_parabolicas * (ancho_indicador + 4) - 4
            progreso = self.tiempo_recarga_parabolica / self.cooldown_parabolica
            pygame.draw.rect(pantalla, (60, 60, 70), (10, 44, ancho_barra, 4))
            if progreso > 0:
                pygame.draw.rect(pantalla, (255, 140, 50), (
                    10, 44, round(ancho_barra * progreso), 4
                ))
