class GestorColisiones:
    def __init__(self):
        self.contactos_nave = set()

    def obtener_municiones(self, nave):
        return (
            nave.municiones_basicas
            + nave.municiones_parabolicas
            + nave.lanzador_conica.municiones
        )

    def procesar_municiones(self, nave, enemigos):
        for municion in self.obtener_municiones(nave):
            if not municion.activa:
                continue
            for enemigo in enemigos:
                if enemigo.vida > 0 and municion.rect.colliderect(enemigo.rect):
                    enemigo.recibir_impacto(municion.tipo)
                    municion.activa = False
                    break

    def procesar_nave(self, nave, enemigos):
        contactos_actuales = set()
        if nave.viva:
            for enemigo in enemigos:
                if enemigo.vida <= 0 or not nave.rect.colliderect(enemigo.rect):
                    continue
                identificador = id(enemigo)
                contactos_actuales.add(identificador)
                if identificador not in self.contactos_nave:
                    nave.recibir_impacto(enemigo.tipo)
        self.contactos_nave = contactos_actuales

    def procesar_municiones_enemigas(self, nave, enemigos):
        if not nave.viva:
            return
        for enemigo in enemigos:
            for municion in getattr(enemigo, "municiones", ()):
                if municion.activa and municion.rect.colliderect(nave.rect):
                    nave.recibir_dano(municion.dano)
                    municion.activa = False
                    return

    def actualizar(self, nave, enemigos):
        self.procesar_municiones(nave, enemigos)
        self.procesar_municiones_enemigas(nave, enemigos)
        self.procesar_nave(nave, enemigos)
