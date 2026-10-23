import random

import pygame

from config import (
    ANCHO,
    MARGEN_APARICION,
    ALTURA_APARICION,
    INTERVALO_APARICION,
    PAUSA_ENTRE_OLEADAS,
    OLEADAS,
    JEFE_ACOMPANANTES,
)


class GestorOleadas:
    def __init__(self, mapa, fabricas):
        self.mapa = mapa
        self.fabricas = fabricas
        self.enemigos = []
        self.ingresados = set()
        self.indice = -1
        self.pendientes = []
        self.temporizador = 0.0
        self.estado = "oleada"
        self.fuente_indicador = None
        self.avanzar()

    @property
    def numero_oleada(self):
        return min(self.indice + 1, len(OLEADAS))

    @property
    def terminado(self):
        return self.estado == "victoria"

    def armar_cola(self, composicion):
        cola = []
        for tipo, cantidad in composicion.items():
            if tipo in self.fabricas:
                cola.extend([tipo] * cantidad)
        random.shuffle(cola)
        return cola

    def avanzar(self):
        self.indice += 1
        if self.indice < len(OLEADAS):
            self.pendientes = self.armar_cola(OLEADAS[self.indice])
            self.estado = "oleada"
        elif self.indice == len(OLEADAS) and "jefe" in self.fabricas:
            self.pendientes = ["jefe"] + self.armar_cola(JEFE_ACOMPANANTES)
            self.estado = "jefe"
        else:
            self.pendientes = []
            self.estado = "victoria"
        self.temporizador = INTERVALO_APARICION - PAUSA_ENTRE_OLEADAS

    def aparecer(self, tipo):
        if tipo == "jefe":
            x = ANCHO // 2
        else:
            x = random.randint(MARGEN_APARICION, ANCHO - MARGEN_APARICION)
        y = -ALTURA_APARICION
        enemigo = self.fabricas[tipo](x, y)
        rect_aparicion = enemigo.rect.inflate(enemigo.separacion, enemigo.separacion)
        for otro in self.enemigos:
            if otro.vivo and rect_aparicion.colliderect(otro.rect):
                return False
        self.enemigos.append(enemigo)
        return True

    def mantener_dentro(self, enemigo):
        if enemigo in self.ingresados:
            self.mapa.limitar(enemigo.rect)
        elif self.mapa.contiene(enemigo.rect):
            self.ingresados.add(enemigo)

    def actualizar(self, dt):
        if self.terminado:
            return []

        disparos = []

        self.temporizador += dt
        if self.pendientes and self.temporizador >= INTERVALO_APARICION:
            self.temporizador = 0.0
            if self.aparecer(self.pendientes[0]):
                self.pendientes.pop(0)

        for enemigo in self.enemigos:
            if enemigo.actualizar(dt, self.enemigos):
                disparos.append("basica")
            self.mantener_dentro(enemigo)

        self.enemigos = [e for e in self.enemigos if e.vida > 0]
        self.ingresados.intersection_update(self.enemigos)

        if not self.pendientes and not self.enemigos:
            self.avanzar()
        return disparos

    def dibujar(self, pantalla):
        for enemigo in self.enemigos:
            enemigo.dibujar(pantalla)
        self.dibujar_indicador(pantalla)

    def dibujar_indicador(self, pantalla):
        if self.estado == "victoria":
            return
        if self.estado == "jefe":
            texto = "JEFE"
            color = (240, 80, 90)
        else:
            texto = f"OLEADA {self.numero_oleada} / {len(OLEADAS)}"
            color = (225, 230, 255)
        if self.fuente_indicador is None:
            self.fuente_indicador = pygame.font.Font(None, 30)
        imagen = self.fuente_indicador.render(texto, True, color)
        rect = imagen.get_rect(topright=(pantalla.get_width() - 14, 12))
        fondo = rect.inflate(18, 10)
        pygame.draw.rect(pantalla, (20, 20, 45), fondo, border_radius=6)
        pygame.draw.rect(pantalla, color, fondo, 1, border_radius=6)
        pantalla.blit(imagen, rect)
