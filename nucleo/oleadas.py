import random
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
        self.enemigos.append(self.fabricas[tipo](x, y))

    def mantener_dentro(self, enemigo):
        if enemigo in self.ingresados:
            self.mapa.limitar(enemigo.rect)
        elif self.mapa.contiene(enemigo.rect):
            self.ingresados.add(enemigo)

    def actualizar(self, dt):
        if self.terminado:
            return

        self.temporizador += dt
        if self.pendientes and self.temporizador >= INTERVALO_APARICION:
            self.temporizador = 0.0
            self.aparecer(self.pendientes.pop(0))

        for enemigo in self.enemigos:
            enemigo.actualizar(dt, self.enemigos)
            self.mantener_dentro(enemigo)

        self.enemigos = [e for e in self.enemigos if e.vida > 0]
        self.ingresados.intersection_update(self.enemigos)

        if not self.pendientes and not self.enemigos:
            self.avanzar()

    def dibujar(self, pantalla):
        for enemigo in self.enemigos:
            enemigo.dibujar(pantalla)
