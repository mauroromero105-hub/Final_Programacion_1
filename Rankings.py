import pygame
import os
from Constantes import *
from Funciones import *
from Manejo_Archivos_Funciones import*
from Game_Over import*

pygame.init()

pantalla_rankings = pygame.transform.scale(pygame.image.load("Texturas/Fondo_Pantallas.png"),PANTALLA)
boton_volver = crear_boton_volver("VOLVER", "Texturas\Boton_Respuesta.jpg", 1, 1)
cuadro_top = crear_elemento_juego("Texturas\Pared_Blanca.png", 400,600,195, 1)

def mostrar_rankings(pantalla, cola_eventos) -> str:
    ventana = "rankings"

    lista_ranking = leer_json(ARCHIVO_RANKING)

    pantalla.blit(pantalla_rankings, (0, 0))    
    pantalla.blit(cuadro_top["superficie"], cuadro_top["rectangulo"])
    pantalla.blit(boton_volver["superficie"], boton_volver["rectangulo"])
    mostrar_texto(pantalla, "TOP 10", (310, 0), FUENTE_ARIAL_55, COLOR_NEGRO)
    mostrar_jugadores(pantalla, lista_ranking)


    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            ventana = "salir"
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if boton_volver["rectangulo"].collidepoint(evento.pos):
                SONIDO_CLICK.play()
                ventana = "menu"

    return ventana


