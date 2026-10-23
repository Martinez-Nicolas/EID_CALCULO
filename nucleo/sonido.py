import pygame


class GestorSonido:
    def __init__(self):
        self.carpeta = "assets"
        self.sonidos = {}
        self.ultimo_sonido_basico = -1000
        if not pygame.mixer.get_init():
            return
        archivos = {
            "basica": "disparo_basico.wav",
            "parabolica": "disparo_parabolico.wav",
            "conica": "disparo_conico.wav",
            "dano": "dano.wav",
        }
        for nombre, archivo in archivos.items():
            try:
                self.sonidos[nombre] = pygame.mixer.Sound(
                    f"{self.carpeta}/{archivo}"
                )
            except pygame.error:
                pass
        volumenes = {
            "basica": 0.12,
            "parabolica": 0.3,
            "conica": 0.35,
            "dano": 0.45,
        }
        for nombre, volumen in volumenes.items():
            if nombre in self.sonidos:
                self.sonidos[nombre].set_volume(volumen)

    def reproducir_disparo(self, tipo):
        if tipo == "basica":
            ahora = pygame.time.get_ticks()
            if ahora - self.ultimo_sonido_basico < 70:
                return
            self.ultimo_sonido_basico = ahora
        sonido = self.sonidos.get(tipo)
        if sonido:
            sonido.play()

    def reproducir_dano(self):
        sonido = self.sonidos.get("dano")
        if sonido:
            sonido.play()

    def reproducir_musica(self, estado):
        if not pygame.mixer.get_init():
            return
        archivos = {
            "juego": "musica.wav",
            "victoria": "musica_victoria.wav",
            "derrota": "musica_derrota.wav",
        }
        try:
            pygame.mixer.music.load(f"{self.carpeta}/{archivos[estado]}")
            pygame.mixer.music.set_volume(0.25)
            pygame.mixer.music.play(-1)
        except pygame.error:
            pass

    def detener_musica(self):
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()

    def pausar(self):
        if pygame.mixer.get_init():
            pygame.mixer.pause()
            pygame.mixer.music.pause()

    def reanudar(self):
        if pygame.mixer.get_init():
            pygame.mixer.unpause()
            pygame.mixer.music.unpause()
