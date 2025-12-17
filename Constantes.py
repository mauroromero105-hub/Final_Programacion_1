import pygame

pygame.init()

#PANTALLA
ANCHO = 800
ALTO = 600
PANTALLA = (ANCHO,ALTO)
FPS = 30

#COLORES
COLOR_BLANCO = "#FFFFFF"
COLOR_NEGRO = "#000000"
COLOR_RESALTE = "#FFD700"

#ELEMENTOS JUEGO
ANCHO_PREGUNTA = 550
ALTO_PREGUNTA = 180
ANCHO_RESPUESTA = 250
ALTO_RESPUESTA = 60
ANCHO_BOTON = 300
ALTO_BOTON = 70
POS_X_BOTON = (ANCHO - ANCHO_BOTON) / 2
ARCHIVO_RANKING = "Rankings.json"

#LOGICA JUEGO
CANTIDAD_VIDAS = 3
VIDA_ERROR = -1
PUNTUACION_ACIERTO = 30
PUNTUACION_ERROR = -15
TIEMPO_TOTAL = 15

#FUENTES
FUENTE_ARIAL_18 = pygame.font.SysFont("Arial",18,False)
FUENTE_ARIAL_20 = pygame.font.SysFont("Arial", 20, False)
FUENTE_ARIAL_25 = pygame.font.SysFont("Arial",25,False)
FUENTE_ARIAL_30 = pygame.font.SysFont("Arial",30,False)
FUENTE_ARIAL_30_NEGRITA = pygame.font.SysFont("Arial",30,True)
FUENTE_ARIAL_40 = pygame.font.SysFont("Arial", 40, False)
FUENTE_ARIAL_50 = pygame.font.SysFont("Arial",50,True)
FUENTE_ARIAL_55 = pygame.font.SysFont("Arial", 55, True)
FUENTE_INICIO = pygame.font.SysFont("Franklin Gothic",24, False)

#SONIDOS
SONIDO_CLICK = pygame.mixer.Sound("Sonidos\Click.mp3")
SONIDO_ERROR = pygame.mixer.Sound("Sonidos\Error.mp3")
SONIDO_VIDA = pygame.mixer.Sound("Sonidos\+1 vida.mp3")