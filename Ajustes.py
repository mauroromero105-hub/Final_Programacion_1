import pygame
from Constantes import *  
from Funciones import *   

pygame.init()

boton_volver = crear_boton_volver("VOLVER", "Texturas\Boton_Respuesta.jpg", 1, 1)
boton_facil = crear_elemento_juego("Texturas/Boton_Respuesta.jpg", 200, 60, 80, 370)
boton_normal = crear_elemento_juego("Texturas/Boton_Respuesta.jpg", 200, 60, 300, 370)
boton_dificil = crear_elemento_juego("Texturas/Boton_Respuesta.jpg", 200, 60, 520, 370)

pantalla_ajustes = pygame.transform.scale(pygame.image.load("Texturas/Fondo_Pantallas.png"),PANTALLA)


def mostrar_ajustes(pantalla, eventos, datos_juego):
    ventana = "ajustes"
    pantalla.blit(pantalla_ajustes, (0,0))

    administrar_barra(datos_juego, pantalla)

    mostrar_texto(pantalla,"DIFICULTAD", (280,300), FUENTE_ARIAL_50, color=COLOR_BLANCO)
    mostrar_texto(boton_facil["superficie"], "FACIL", (60,15), FUENTE_ARIAL_30, COLOR_BLANCO)
    mostrar_texto(boton_normal["superficie"], "NORMAL", (45,15), FUENTE_ARIAL_30, COLOR_BLANCO)
    mostrar_texto(boton_dificil["superficie"], "DIFICIL", (45,15), FUENTE_ARIAL_30, COLOR_BLANCO)

    dibujar_lista_elementos([boton_facil, boton_normal, boton_dificil], pantalla)

    resaltado_dificultad(boton_facil, boton_normal, boton_dificil, datos_juego, pantalla)

    dibujar_botones([boton_volver], pantalla, "superficie", "rectangulo", 0)

    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            click_dificultad(boton_facil, boton_normal, boton_dificil, evento, datos_juego)

            if boton_volver["rectangulo"].collidepoint(evento.pos):
                SONIDO_CLICK.play()
                ventana = "menu"

    return ventana

