ANCHO = 800
ALTO = 600
FPS = 60
TITULO = "Juego Arcade"

COLOR_FONDO = (10, 10, 30)
COLOR_BORDE = (200, 200, 220)
GROSOR_BORDE = 2

VIDA_NAVE = 100
DANO_ENEMIGOS = {
    "enemigo1": 20,
    "enemigo2": 35,
    "enemigo3": 50,
    "jefe": 100,
}
IMPACTOS_PARA_ELIMINAR = {
    "enemigo1": {"basica": 30, "parabolica": 2, "conica": 1},
    "enemigo2": {"basica": 60, "parabolica": 3, "conica": 2},
    "enemigo3": {"basica": 90, "parabolica": 5, "conica": 3},
    "jefe": {"basica": 180, "parabolica": 9, "conica": 4},
}
VIDA_ENEMIGOS = {
    "enemigo1": 30,
    "enemigo2": 60,
    "enemigo3": 90,
    "jefe": 180,
}
PUNTOS_ENEMIGOS = {
    "enemigo1": 100,
    "enemigo2": 250,
    "enemigo3": 500,
    "jefe": 2000,
}

MAXIMO_PARABOLICAS = 3
COOLDOWN_PARABOLICA = 10.0
DURACION_DESTELLO_DANO = 0.35
DANO_BALA_JEFE = 15
INTERVALO_MIN_DISPARO_JEFE = 0.8
INTERVALO_MAX_DISPARO_JEFE = 1.6

MARGEN_APARICION = 40
ALTURA_APARICION = 60
INTERVALO_APARICION = 1.0
PAUSA_ENTRE_OLEADAS = 2.0

OLEADAS = [
    {1: 6},
    {1: 5, 2: 4},
    {1: 4, 2: 4, 3: 3},
]
JEFE_ACOMPANANTES = {1: 3}

COOLDOWN_CONICA = 10.0
CONICA_A = 50
CONICA_B = 120
CONICA_VELOCIDAD = 2.2
CONICA_RADIO = 7
