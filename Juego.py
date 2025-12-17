import pygame
from Constantes import *
from Funciones import *
from os import*
from Manejo_Archivos_Funciones import*

pygame.init()

cuadro_pregunta = crear_elemento_juego("Texturas/Cuadro_madera.jpg",ANCHO_PREGUNTA, ALTO_PREGUNTA, 125, 110)
cuadro_respuestas = crear_lista_respuestas("Texturas/Boton_Respuesta.jpg",270, 300, 4)
cuadro_puntuacion = crear_elemento_juego("Texturas/Boton_Respuesta.jpg",180, 100, 620, 1)
boton_volver = crear_boton_volver("VOLVER", "Texturas/Boton_Respuesta.jpg", 1, 1)
boton_bomba = crear_elemento_juego("Texturas/Bomba.png", 40, 40, 20, 260)
boton_x2 = crear_elemento_juego("Texturas/icono_x2.png", 40, 40, 20, 300)
boton_doble = crear_elemento_juego("Texturas/logo_dos_intentos.png", 40, 40, 20, 340)
boton_pasar = crear_elemento_juego("Texturas/Cambio_Pregunta.png", 40, 40, 20, 380)

pantalla_juego = pygame.transform.scale(pygame.image.load("Texturas/Fondo_Pantallas.png"),PANTALLA)

def mostrar_juego(pantalla: pygame.Surface, cola_eventos: list[pygame.event.Event], datos_juego: dict, preguntas) -> str:
    ventana = "jugar"

    if actualizar_tiempo_pregunta(datos_juego):
        pasar_pregunta(datos_juego, preguntas)

    pregunta_actual = obtener_pregunta_actual(datos_juego, preguntas)

    for evento in cola_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:

            if boton_volver["rectangulo"].collidepoint(evento.pos):
                    SONIDO_CLICK.play()
                    ventana = "menu"

            click_comodines(boton_bomba, boton_doble, boton_x2, boton_pasar, evento, datos_juego, pregunta_actual, preguntas)

            responder_pregunta_pygame(cuadro_respuestas, evento.pos ,SONIDO_CLICK, datos_juego, preguntas, pregunta_actual)

            pregunta_actual = obtener_pregunta_actual(datos_juego, preguntas)

    if datos_juego["cantidad_vidas"] <= 0:
        ventana = "game_over"

    pantalla.blit(pantalla_juego, (0, 0))

    mostrar_datos_juego_pygame(cuadro_puntuacion, pantalla, datos_juego)
    mostrar_pregunta_pygame(pregunta_actual,pantalla,cuadro_pregunta,cuadro_respuestas,datos_juego)
    dibujar_botones_disponibles(pantalla, datos_juego, boton_bomba, boton_x2, boton_doble, boton_pasar, boton_volver)

    return ventana

