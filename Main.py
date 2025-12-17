import pygame
from Funciones import*
from Constantes import*
from Manejo_Archivos_Funciones import*
from Menu import*
from Juego import*
from Rankings import*
from Ajustes import*
from Game_Over import*


pygame.init()

pygame.display.set_caption("Preguntados")
pantalla = pygame.display.set_mode(PANTALLA)
pygame.display.set_icon(pygame.image.load("Texturas\Icono.png"))
reloj = pygame.time.Clock()
datos_juego = crear_datos_juego()
csv_preguntas = cargar_preguntas("Preguntas.csv") 
ventana_actual = "menu"
bandera_juego = False
os.system("cls")

while(True):
    reloj.tick(FPS)
    cola_eventos = pygame.event.get()

    for evento in cola_eventos:
        if evento.type == pygame.QUIT:
            ventana_actual = "salir"
    if ventana_actual == "menu":
        pygame.mixer.music.stop()
        bandera_juego = False
        ventana_actual = mostrar_menu(pantalla, cola_eventos)
    elif ventana_actual == "jugar":
        if bandera_juego == False:
            colocar_musica("Sonidos\Musica del juego.mp3", datos_juego)
            mezclar_lista(csv_preguntas)
            reiniciar_estadisticas(datos_juego)
            bandera_juego = True
        ventana_actual = mostrar_juego(pantalla, cola_eventos, datos_juego, csv_preguntas)
    elif ventana_actual == "ajustes":
        ventana_actual = mostrar_ajustes(pantalla, cola_eventos, datos_juego)
    elif ventana_actual == "rankings":
        ventana_actual = mostrar_rankings(pantalla, cola_eventos)
    elif ventana_actual == "game_over":
        if bandera_juego == True:
            pygame.mixer.music.stop()
            bandera_juego = False
        ventana_actual = mostrar_game_over(pantalla, cola_eventos, datos_juego)
    elif ventana_actual == "salir":
        break
    
    pygame.display.flip()

pygame.quit()