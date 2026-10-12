# Juego arcade – MATE1133 (EID N°1)

> **ESTE ARCHIVO ES SOLO PARA EL EQUIPO. ELIMINAR `README.md` DEL REPO ANTES DE GRABAR EL VIDEO Y ENTREGAR.**
> El enunciado dice que cualquier documentación deja el elemento en 0 puntos.

Entrega: **domingo 25 de octubre, 17:00 hrs** (código + video de defensa sin cortes).

## Cómo ejecutar

1. Instalar pygame: `pip install pygame`
2. Ejecutar desde la carpeta del proyecto: `python main.py`

## Librerías

- **Permitidas:** `pygame`, `math`, `random`.
- **Prohibidas:** `numpy`, `sympy`, `scipy`, y cualquier librería que haga cálculos por nosotros. Si se usa una, el proyecto queda con nota mínima.
- Impactos, vida, colisiones y trayectorias los programamos nosotros.

## Reglas del código

- **Sin comentarios, sin docstrings y sin documentación** en ningún archivo `.py`.
- Los `__init__.py` van vacíos.
- Nombres de variables y funciones claros para poder explicarlos en la defensa.
- El código que se entrega debe ser **el mismo** que se usa en el video.

## Estructura de carpetas

- `main.py` y `config.py`: ventana, bucle principal y valores del juego.
- `nave/`: nave principal, movimiento con flechas y vida.
- `municiones/`: básica, parabólica y otra cónica.
- `enemigos/`: enemigos 1, 2, 3 y jefe.
- `nucleo/`: oleadas, colisiones y mapa.
- `assets/`: imágenes y recursos.

## Requisitos clave del juego

- Nave: solo flechas; vida según el enemigo que choca (el jefe es el más letal).
- Municiones: básica sin límite; parabólica y cónica con cooldown o cantidad finita.
- Enemigos: 3 tipos + jefe, diseños distintos (no solo color), cada uno con su propia ecuación `A·sen(Bx + C) + D` escrita en el código.
- Vida de enemigos según la munición: las municiones más complejas hacen más daño.
- 3 oleadas + jefe: oleada 1 (un tipo), oleada 2 (tipos 1 y 2), oleada 3 (tipos 1, 2 y 3), jefe con al menos un tipo de enemigo.
- Los enemigos no salen del mapa y no se eliminan entre ellos.

## Cómo trabajamos en Git (todos en `main`)

1. Antes de empezar: `git pull`
2. Trabajar solo en los archivos propios (ver reparto).
3. Commits pequeños y frecuentes: `git add .` → `git commit -m "mensaje claro"` → `git pull` → `git push`
4. Si hay que tocar `main.py` o `config.py`, avisar al grupo antes.

## Reparto

- **Nico:** `main.py`, `config.py`, mapa, oleadas, colisiones, munición cónica.
- **Martin:** nave, munición básica y parabólica.
- **xelo:** enemigos 1, 2, 3, jefe y su vida según la munición.

## Defensa en video

- Reunión en Meet (o similar) con **cámara encendida** y **nombre y apellido** de cada integrante.
- **Sin ediciones ni cortes**. Participan los tres, explicando la matemática y el código, y probando el juego.
- Subir con permisos de acceso y comprobar que se vea antes de entregar.
