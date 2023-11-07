import pygame
import random
import math
from pygame import mixer
import io


# Inicializar pygame
pygame.init()

# crear la pantalla
pantalla = pygame.display.set_mode((800, 600))

# Titulo e icono
pygame.display.set_caption('Invasión Espacial')
icono = pygame.image.load("dist/images/spaceship.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load("dist/images/fondo.png")

# agregar musica
'''mixer.music.load('sonidos/8bit.mp3')
mixer.music.set_volume(0.3)
mixer.music.play(-1)'''

# variables del Jugador
img_jugador = pygame.image.load("dist/images/rocket.png")
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0

# variables del Enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 2

for e in range(cantidad_enemigos):

    img_enemigo.append(pygame.image.load("dist/images/cthulhu.png"))
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(50, 200))
    enemigo_x_cambio.append(1)
    enemigo_y_cambio.append(50)

# variables de la bala
balas = []
img_bala = pygame.image.load("dist/images/bullet.png")
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 4
bala_visible = False


def fuente_bytes(fuente):
    with open(fuente, 'rb') as f:

        ttf_bytes = f.read()
    return io.BytesIO(ttf_bytes)


# puntaje
puntaje = 0
fuente_como_bytes = fuente_bytes("dist/fuentes/From Cartoon Blocks.ttf")
fuente = pygame.font.Font('dist/fuentes/From Cartoon Blocks.ttf', 32)
texto_x = 10
texto_y = 10

# texto final de juego
final = pygame.font.Font(fuente_como_bytes, 40)


# funcio fin juego


def texto_final():
    mi_fuente_final = final.render(
        "JUEGO TERMINADO", True, (255, 255, 255))
    pantalla.blit(mi_fuente_final, (250, 250))


# funcion mostrar puntaje
def mostrar_puntaje(x, y):
    texto = fuente.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
    pantalla.blit(texto, (x, y))
# funcion jugador


def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))


# funcion Enemigo
def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))

# funcion disparar bala


def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x+23, y+10))


# detectar colisiones

def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_1-x_2, 2) + math.pow(y_2-y_1, 2))
    if distancia < 27:
        return True
    else:
        return False


# Loop del juego
ejecucion = True
while ejecucion:

    # pantalla
    pantalla.blit(fondo, (0, 0))
    # iterar eventos
    for e in pygame.event.get():
        # evento cerrar
        if e.type == pygame.QUIT:
            ejecucion = False
        # evento presionar flechas
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_LEFT:
                jugador_x_cambio = -2

            if e.key == pygame.K_RIGHT:
                jugador_x_cambio = 2
            # evento de disparo
            if e.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound('dist/sonidos/disparo.mp3')
                sonido_bala.play()
                nueva_bala = {
                    "x": jugador_x,
                    "y": jugador_y,
                    "velocidad": -5
                }
                balas.append(nueva_bala)
        # eventos soltar flechas
        if e.type == pygame.KEYUP:
            if e.key == pygame.K_LEFT or e.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    # modificar ubicación del jugador
    jugador_x += jugador_x_cambio

    # mantener dentro del borde el jugador
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736

    # modificar ubicación del enemigo
    for e in range(cantidad_enemigos):

        # fin del juego
        if enemigo_y[e] > 450:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break

        enemigo_x[e] += enemigo_x_cambio[e]

        # mantener dentro del borde al enemigo
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 1.5
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -1.5
            enemigo_y[e] += enemigo_y_cambio[e]
          # verificar colision

        for bala in balas:
            colision_bala_enemigo = hay_colision(
                enemigo_x[e], enemigo_y[e], bala["x"], bala["y"])

            colision = hay_colision(enemigo_x[e], enemigo_y[e], bala_x, bala_y)
            if colision_bala_enemigo:
                sonido_colision = mixer.Sound('dist/sonidos/Golpe.mp3')
                sonido_colision.play()
                balas.remove(bala)
                puntaje += 1
                enemigo_x[e] = random.randint(0, 736)
                enemigo_y[e] = random.randint(20, 200)
                break

        enemigo(enemigo_x[e], enemigo_y[e], e)

    # movimiento de la bala
    for bala in balas:
        bala["y"] += bala["velocidad"]
        pantalla.blit(img_bala, (bala["x"] + 16, bala["y"] + 10))
        if bala["y"] < 0:
            balas.remove(bala)
    for bala in balas:
        bala["y"] += bala["velocidad"]
        pantalla.blit(img_bala, (bala["x"] + 16, bala["y"] + 10))
        if bala["y"] < 0:
            balas.remove(bala)

    jugador(jugador_x, jugador_y)

    # mostrar puntake
    mostrar_puntaje(texto_x, texto_y)
    # actualizar
    pygame.display.update()
