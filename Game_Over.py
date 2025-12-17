import pygame
import os
from Constantes import *
from Funciones import *
from Manejo_Archivos_Funciones import*

pygame.init()

pantalla_game_over = pygame.transform.scale(pygame.image.load("Texturas/Fondo_game_over.png"),PANTALLA)

boton_continuar = crear_boton_continuar("CONTINUAR", 300, 380, 200, 60,(80,255,80),(160,160,160),FUENTE_ARIAL_30,320,390,activo=False, )

def mostrar_game_over(pantalla:pygame.Surface, cola_eventos:list[pygame.event.Event], datos_juego:dict) -> str:
    datos_juego["bandera_texto"] = not datos_juego["bandera_texto"]

    ventana = "game_over"
    cuadro_nombre = crear_elemento_juego("Texturas/Figura_blanca.jpg", 300, 50, 250, 320)

    pantalla.blit(pantalla_game_over,(0,0))

    for evento in cola_eventos:
        manejar_texto_nombre(evento, datos_juego)

    mostrar_texto(pantalla, f"GAME OVER", (290, 200), FUENTE_ARIAL_40, COLOR_NEGRO)
    mostrar_texto(pantalla, f"PUNTUACIÓN FINAL: {datos_juego.get('puntuacion')}", (220, 260), FUENTE_ARIAL_40, COLOR_NEGRO)

    ingreso_nombre(datos_juego, pantalla, cuadro_nombre, boton_continuar)

    dibujar_boton_continuar(pantalla, boton_continuar)

    if boton_clickeado_continuar(cola_eventos, boton_continuar) and boton_continuar["activo"]:
        guardar_puntaje_json(ARCHIVO_RANKING, datos_juego["nombre"], datos_juego["puntuacion"])
        ventana = "menu"


    return ventana

