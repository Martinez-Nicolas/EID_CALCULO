import math

import pygame

from config import (
    COOLDOWN_PARABOLICA,
    DANO_ENEMIGOS,
    DURACION_DESTELLO_DANO,
    MAXIMO_PARABOLICAS,
    VIDA_NAVE,
)
from municiones.basica import MunicionBasica
from municiones.conica import LanzadorConica
from municiones.parabolica import MunicionParabolica


class Nave:
    def __init__(self, ancho_mapa, alto_mapa):
        imagen = pygame.image.load("assets/nave.png")
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
        self.imagen_dano = self.imagen.copy()
        self.imagen_dano.fill((255, 70, 70), special_flags=pygame.BLEND_RGB_MULT)
        self.ancho_mapa = ancho_mapa
        self.alto_mapa = alto_mapa
        self.x = (ancho_mapa - self.ancho) / 2
        self.y = max(0, alto_mapa - self.alto - 20)
        self.velocidad = 300
        self.vida_maxima = VIDA_NAVE
        self.vida = self.vida_maxima
        self.municiones_basicas = []
        self.lanzador_conica = LanzadorConica()
        self.municiones_parabolicas = []
        self.maximo_parabolicas = MAXIMO_PARABOLICAS
        self.cargas_parabolicas = self.maximo_parabolicas
        self.cooldown_parabolica = COOLDOWN_PARABOLICA
        self.tiempo_recarga_parabolica = 0
        self.recargando_parabolicas = False
        self.tecla_parabolica_pulsada = False
        self.dano_por_enemigo = DANO_ENEMIGOS.copy()
        self.duracion_destello_dano = DURACION_DESTELLO_DANO
        self.tiempo_destello_dano = 0
        self.fuente_hud = pygame.font.Font(None, 20)

    @property
    def viva(self):
        return self.vida > 0

    @property
    def rect(self):
        return pygame.Rect(round(self.x), round(self.y), self.ancho, self.alto)

    def actualizar(self, teclas, tiempo_transcurrido):
        disparos = []
        if tiempo_transcurrido <= 0:
            return disparos
        self.tiempo_destello_dano = max(
            0, self.tiempo_destello_dano - tiempo_transcurrido
        )
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
            return disparos
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
            if self.disparar_basica():
                disparos.append("basica")
        if teclas[pygame.K_c]:
            if self.lanzador_conica.disparar(self.x + self.ancho / 2, self.y):
                disparos.append("conica")
        if teclas[pygame.K_x] and not self.tecla_parabolica_pulsada:
            if self.disparar_parabolica():
                disparos.append("parabolica")
        self.tecla_parabolica_pulsada = bool(teclas[pygame.K_x])
        return disparos

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
        self.recibir_dano(self.dano_por_enemigo[tipo_enemigo])

    def recibir_dano(self, dano):
        self.vida = max(0, self.vida - dano)
        self.tiempo_destello_dano = self.duracion_destello_dano

    def dibujar(self, pantalla):
        for municion in self.municiones_basicas:
            municion.dibujar(pantalla)
        self.lanzador_conica.dibujar(pantalla)
        for municion in self.municiones_parabolicas:
            municion.dibujar(pantalla)
        if not self.viva:
            return
        mostrar_dano = (
            self.tiempo_destello_dano > 0
            and int(self.tiempo_destello_dano * 24) % 2 == 0
        )
        imagen = self.imagen_dano if mostrar_dano else self.imagen
        pantalla.blit(imagen, self.rect)

    def dibujar_vida(self, pantalla):
        ancho_barra = min(160, self.ancho_mapa - 20)
        ancho_vida = round(ancho_barra * self.vida / self.vida_maxima)
        pygame.draw.rect(pantalla, (60, 60, 70), (10, 10, ancho_barra, 12))
        if ancho_vida > 0:
            pygame.draw.rect(pantalla, (60, 210, 100), (10, 10, ancho_vida, 12))
        pantalla.blit(
            self.fuente_hud.render("VIDA", True, (225, 230, 255)), (176, 7)
        )
        self.lanzador_conica.dibujar_recarga(pantalla)
        self.dibujar_municiones(pantalla)
        pantalla.blit(
            self.fuente_hud.render("HIPERBOLA", True, (210, 160, 255)), (176, 54)
        )

    def dibujar_municiones(self, pantalla):
        ancho_indicador = min(14, (self.ancho_mapa - 28) // self.maximo_parabolicas)
        for indice in range(self.maximo_parabolicas):
            color = (255, 140, 50) if indice < self.cargas_parabolicas else (60, 60, 70)
            pygame.draw.rect(pantalla, color, (
                10 + indice * (ancho_indicador + 4), 30, ancho_indicador, 10
            ))
        x_etiqueta = 14 + self.maximo_parabolicas * (ancho_indicador + 4)
        pantalla.blit(
            self.fuente_hud.render("PARABOLA", True, (255, 170, 80)),
            (x_etiqueta, 27),
        )
        if self.recargando_parabolicas:
            ancho_barra = self.maximo_parabolicas * (ancho_indicador + 4) - 4
            progreso = self.tiempo_recarga_parabolica / self.cooldown_parabolica
            pygame.draw.rect(pantalla, (60, 60, 70), (10, 44, ancho_barra, 4))
            if progreso > 0:
                pygame.draw.rect(pantalla, (255, 140, 50), (
                    10, 44, round(ancho_barra * progreso), 4
                ))
