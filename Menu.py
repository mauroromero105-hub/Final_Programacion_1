import pygame
from Constantes import*
from Funciones import*


pygame.init()

fondo_menu = pygame.transform.scale(pygame.image.load("Texturas\Fondo_inicio.png"),PANTALLA)
lista_botones = crear_lista_botones("Texturas\Boton_inicio.jpg", 240,150,4)
lista_texto_botones = ["JUGAR","AJUSTES","RANKINGS","SALIR"]
posicion_botones = [(100,15),(90,15),(85,15),(105,15)]

def mostrar_menu(pantalla:pygame.Surface, cola_eventos:list[pygame.event.Event]) -> str:
    ventana = "menu"
    
    for evento in cola_eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for i in range(len(lista_botones)):
                if lista_botones[i]["rectangulo"].collidepoint(evento.pos):
                    SONIDO_CLICK.play()
                    ventana = lista_texto_botones[i].lower()
                    
    pantalla.blit(fondo_menu,(0,0))
    for i in range(len(lista_botones)):
        mostrar_texto(lista_botones[i]["superficie"], lista_texto_botones[i], posicion_botones[i],FUENTE_ARIAL_30_NEGRITA,COLOR_BLANCO)
        dibujar_botones(lista_botones, pantalla, "superficie", "rectangulo", i)

    return ventana