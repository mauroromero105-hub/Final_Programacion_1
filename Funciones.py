import random
import os
from Constantes import *
import pygame

#GENERAL
def mostrar_texto(superficie, texto, posicion, fuente, color=pygame.Color('black')) -> None:
    lineas = [linea.split(' ') for linea in texto.splitlines()]

    ancho_espacio = fuente.size(' ')[0]

    ancho_maximo, alto_maximo = superficie.get_size()

    x_inicial, y = posicion
    x = x_inicial

    for linea in lineas:
        for palabra in linea:
            superficie_palabra = fuente.render(palabra, True, color)
            ancho_palabra, alto_palabra = superficie_palabra.get_size()

            if x + ancho_palabra >= ancho_maximo:
                x = x_inicial
                y += alto_palabra

            superficie.blit(superficie_palabra, (x, y))

            x += ancho_palabra + ancho_espacio

        x = x_inicial
        y += alto_palabra
    return None

def crear_datos_juego() -> dict:
    datos_juego = {
        #estadistica
        "nombre": "",
        "indice": 0,
        "puntuacion": 0,
        "cantidad_vidas": CANTIDAD_VIDAS,

        #tiempo
        "tiempo_total": 15,
        "tiempo_restante": 15,
        "tiempo_inicio_pregunta": pygame.time.get_ticks(),

        #dificultad
        "dificultad": "facil",
        "puntuacion_acierto": 30,
        "puntuacion_error": -10,

        #bomba
        "bomba_animando": False,
        "bomba_pendientes": [],

        #acciones
        "correctas_seguidas": 0,
        "respuestas_ocultas": [],
        "doble_chance_en_uso": False,
        "doble_chance_fallo": False,
        "x2_activado": False,

        #comodines
        "bomba_disponible": True,
        "x2_disponible": True,
        "pasar_disponible": True,
        "doble_chance_disponible": True,

        #Volumen
        "volumen_musica": 0.5,
        "bandera_texto": True,
        "ultimo_borrado": 0
    }
    return datos_juego

def verificar_indice(datos_juego:dict,lista_preguntas:list) -> None:
    if datos_juego["indice"] == len(lista_preguntas):
        datos_juego["indice"] = 0
        mezclar_lista(lista_preguntas)
    return None

def mezclar_lista(lista_preguntas:dict) -> bool:
    if type(lista_preguntas) == list and len(lista_preguntas):
        retorno = True
        random.shuffle(lista_preguntas)
    else:
        retorno = False
    return retorno

def crear_elemento_juego(textura:str, ancho_elemento:int, alto_elemento:int, x:int, y:int) -> dict | None:
    if os.path.exists(textura):

        superficie = pygame.image.load(textura)
        superficie = pygame.transform.scale(superficie, (ancho_elemento, alto_elemento))

        rectangulo = superficie.get_rect(topleft=(x, y))

        return {
            "superficie": superficie,
            "rectangulo": rectangulo
        }
    else:
        return None

def dibujar_botones(lista_botones, pantalla, superficie, superficie_boton, indice) -> None:
    pantalla.blit(lista_botones[indice][superficie], lista_botones[indice][superficie_boton])
    return None

def dibujar_lista_elementos(lista_elementos: list, pantalla: pygame.Surface) -> None:
    for elem in lista_elementos:
        pantalla.blit(elem["superficie"], elem["rectangulo"])
    return None

def dibujar_botones_disponibles(pantalla: pygame.Surface, datos_juego: dict, boton_bomba, boton_x2, boton_doble, boton_pasar, boton_volver) -> None:
    botones_visibles = []
    if datos_juego.get("bomba_disponible", False):
        botones_visibles.append(boton_bomba)
    if datos_juego.get("x2_disponible", False):
        botones_visibles.append(boton_x2)
    if datos_juego.get("doble_chance_disponible", False):
        botones_visibles.append(boton_doble)
    if datos_juego.get("pasar_disponible", False):
        botones_visibles.append(boton_pasar)

    botones_visibles.append(boton_volver)

    botones_filtrados = []
    for i in botones_visibles:
        if i:
            botones_filtrados.append(i)

    botones_visibles = botones_filtrados
    dibujar_lista_elementos(botones_visibles, pantalla)

    return None

def dibujar_respuestas(cuadro_respuestas: list, pantalla: pygame.Surface, pregunta_actual: dict, datos_juego: dict) -> None:
    opciones = ["opcion_A", "opcion_B", "opcion_C", "opcion_D"]

    for i, cuadro in enumerate(cuadro_respuestas):
        if i in datos_juego.get("respuestas_ocultas", []):
            continue

        cuadro["superficie"] = pygame.transform.scale(pygame.image.load("Texturas/Boton_Respuesta.jpg"), (ANCHO_RESPUESTA, ALTO_RESPUESTA))
        texto = pregunta_actual.get(opciones[i], "")
        mostrar_texto(cuadro["superficie"], texto, (15, 15), FUENTE_ARIAL_20, COLOR_BLANCO)
        pantalla.blit(cuadro["superficie"], cuadro["rectangulo"])
    return None

def mostrar_datos_juego_pygame(cuadro_puntuacion: dict, pantalla: pygame.Surface, datos_juego: dict) -> None:
    cuadro_puntuacion["superficie"] = pygame.transform.scale(pygame.image.load("Texturas/Boton_Respuesta.jpg"), (180, 100))
    mostrar_texto(cuadro_puntuacion["superficie"], f"Tiempo restante: {datos_juego.get('tiempo_restante')} s", (10, 10), FUENTE_INICIO, COLOR_BLANCO)
    mostrar_texto(cuadro_puntuacion["superficie"], f"Puntuación: {datos_juego.get('puntuacion')}", (10, 35), FUENTE_INICIO, COLOR_BLANCO)
    mostrar_texto(cuadro_puntuacion["superficie"], f"Vidas: {datos_juego.get('cantidad_vidas')}", (10, 60), FUENTE_INICIO, COLOR_BLANCO)
    pantalla.blit(cuadro_puntuacion["superficie"], cuadro_puntuacion["rectangulo"])
    return None

def resaltar_elemento(elemento: dict, pantalla: pygame.Surface, color=(255,215,0), grosor: int = 4, border_radius: int = 8) -> None:
    if not elemento:
        return None
    rect = elemento.get("rectangulo")
    if rect is None:
        return None
    pygame.draw.rect(pantalla, color, rect, grosor, border_radius=border_radius)
    return None

def dibujar_texto_en_cuadro(superficie, texto, rect, fuente, color=(0,0,0), margen=5) -> None:
    palabras = texto.split(" ")
    lineas = []
    linea_actual = ""

    for palabra in palabras:
        prueba_linea = linea_actual + " " + palabra if linea_actual != "" else palabra
        ancho, alto = fuente.size(prueba_linea)
        if ancho + 2*margen > rect.width:
            lineas.append(linea_actual)
            linea_actual = palabra
        else:
            linea_actual = prueba_linea

    if linea_actual:
        lineas.append(linea_actual)

    total_altura = len(lineas) * fuente.get_linesize()
    y_offset = rect.top + (rect.height - total_altura) // 2  

    for linea in lineas:
        ancho_linea, alto_linea = fuente.size(linea)
        x = rect.left + (rect.width - ancho_linea) // 2 
        render = fuente.render(linea, True, color)
        superficie.blit(render, (x, y_offset))
        y_offset += fuente.get_linesize()
    return None

def crear_boton_volver(texto, textura, x, y) -> dict:
    boton = crear_elemento_juego(textura,100, 40, x, y)
    dibujar_texto_en_cuadro(boton["superficie"], texto, boton["rectangulo"], FUENTE_INICIO, color= 'white')
    return boton

def colocar_musica(musica:str,datos_juego:dict) -> bool:
    if os.path.exists(musica):
        retorno = True
        pygame.mixer.music.load("Sonidos\Musica del juego.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(datos_juego.get("volumen_musica"))
    else:
        retorno = False
        
    return retorno

#JUEGO

def crear_lista_respuestas(textura:str,x:int,y:int,cantidad_respuestas:int) -> list:
    lista_respuestas = []

    for i in range(cantidad_respuestas):
        cuadro_respuesta = crear_elemento_juego(textura,ANCHO_RESPUESTA,ALTO_RESPUESTA,x,y)
        lista_respuestas.append(cuadro_respuesta)
        y += 70
    
    return lista_respuestas

def crear_lista_botones(textura:str,x:int,y:int,cantidad_botones:int) -> list:
    lista_botones = []

    for i in range(cantidad_botones):
        boton = crear_elemento_juego(textura,ANCHO_BOTON,ALTO_BOTON,x,y)
        lista_botones.append(boton)
        y += 85
    
    return lista_botones

def obtener_pregunta_actual(datos_juego:dict,lista_preguntas:list) -> dict | None:
    if type(datos_juego) == dict and type(lista_preguntas) == list and len(lista_preguntas) > 0 and datos_juego.get("indice") != None:
        indice = datos_juego.get("indice")
        pregunta = lista_preguntas[indice]
    else:
        pregunta = None

    return pregunta    

def pasar_pregunta(datos_juego:dict,lista_preguntas:list) -> bool:
    if type(datos_juego) == dict and datos_juego.get("indice") != None:
        retorno = True
        datos_juego["indice"] += 1
        verificar_indice(datos_juego,lista_preguntas)
    else:
        retorno = False 
        
    return retorno

def responder_pregunta_pygame(lista_respuestas, pos_click, sonido,datos_juego, lista_preguntas, pregunta_actual) -> bool:

    ocultas = datos_juego["respuestas_ocultas"]

    for i in range(len(lista_respuestas)):
        if i in ocultas:
            continue

        rect = lista_respuestas[i]["rectangulo"]

        if rect.collidepoint(pos_click):
            sonido.play()
            respuesta = i + 1

            es_correcta = verificar_respuesta(pregunta_actual,datos_juego,respuesta)

            if es_correcta:
                modificar_puntuacion(datos_juego, datos_juego.get("puntuacion_acierto", PUNTUACION_ACIERTO))
                if datos_juego.get("x2_activado"):
                    modificar_puntuacion(datos_juego, datos_juego.get("puntuacion_acierto", PUNTUACION_ACIERTO))
                    datos_juego["x2_activado"] = False

            else:
                SONIDO_ERROR.play()
                if datos_juego.get("doble_chance_en_uso"):
                    if not datos_juego.get("doble_chance_fallo"):
                        datos_juego["doble_chance_fallo"] = True
                        datos_juego["respuestas_ocultas"].append(i)
                        return True
                    else:
                        modificar_puntuacion(datos_juego, datos_juego.get("puntuacion_error", PUNTUACION_ERROR))
                        modificar_vida(datos_juego, VIDA_ERROR)
                        datos_juego["doble_chance_en_uso"] = False
                        datos_juego["doble_chance_fallo"] = False
                else:
                    modificar_puntuacion(datos_juego, datos_juego.get("puntuacion_error", PUNTUACION_ERROR))
                    modificar_vida(datos_juego, VIDA_ERROR)

            manejar_aciertos_consecutivos(datos_juego, es_correcta)

            datos_juego["respuestas_ocultas"] = []
            datos_juego["doble_chance_en_uso"] = False
            datos_juego["doble_chance_fallo"] = False

            pasar_pregunta(datos_juego, lista_preguntas)

            datos_juego["tiempo_inicio_pregunta"] = pygame.time.get_ticks()

            return True

    return False

def mostrar_pregunta_pygame(pregunta_actual:dict, pantalla:pygame.Surface,cuadro_pregunta:dict, cuadro_respuestas:list, datos_juego:dict) -> bool:
    if type(pregunta_actual) != dict:
        return False
    cuadro_pregunta["superficie"] = pygame.transform.scale(pygame.image.load("Texturas/Cuadro_madera.jpg"), (ANCHO_PREGUNTA, ALTO_PREGUNTA))
    mostrar_texto(cuadro_pregunta["superficie"], pregunta_actual.get("pregunta"), (10,10), FUENTE_ARIAL_30)
    pantalla.blit(cuadro_pregunta["superficie"], cuadro_pregunta["rectangulo"])

    dibujar_respuestas(cuadro_respuestas, pantalla, pregunta_actual, datos_juego)

    return True

def verificar_respuesta(pregunta_actual:dict, datos_juego:dict, respuesta:int) -> bool:
    if pregunta_actual is None:
        return False
    if respuesta < 1 or respuesta > 4:
        return False

    opciones = ["opcion_A", "opcion_B", "opcion_C", "opcion_D"]

    texto_elegido = pregunta_actual.get(opciones[respuesta - 1], "")
    texto_correcto = pregunta_actual.get("opcion_correcta", "")

    texto_elegido = str(texto_elegido).strip().casefold()
    texto_correcto = str(texto_correcto).strip().casefold()

    es_correcta = texto_elegido == texto_correcto and texto_correcto != ""

    return es_correcta

#COMODINES

def click_comodines(boton_bomba, boton_doble, boton_x2, boton_pasar, evento, datos_juego, pregunta_actual, preguntas) -> None:
    if datos_juego.get("bomba_disponible", False) and boton_bomba["rectangulo"].collidepoint(evento.pos):
        activar_bomba(datos_juego, pregunta_actual)

    if datos_juego.get("doble_chance_disponible", False) and boton_doble["rectangulo"].collidepoint(evento.pos):
        activar_doble_chance(datos_juego)

    if datos_juego.get("x2_disponible", False) and boton_x2["rectangulo"].collidepoint(evento.pos):
        activar_x2(datos_juego)

    if datos_juego.get("pasar_disponible", False) and boton_pasar["rectangulo"].collidepoint(evento.pos):
        activar_pasar(datos_juego, preguntas)
        pregunta_actual = obtener_pregunta_actual(datos_juego, preguntas)
    return None

def activar_x2(datos_juego:dict) -> bool:
    if not datos_juego.get("x2_disponible"):
        return False
    datos_juego["x2_activado"] = True
    datos_juego["x2_disponible"] = False
    return True

def usar_doble_chance(datos_juego) -> None:
    if datos_juego.get("doble_chance_disponible"):
        datos_juego["doble_chance_en_uso"] = True
        datos_juego["doble_chance_fallo"] = False
        datos_juego["doble_chance_disponible"] = False
    return None

def activar_doble_chance(datos_juego) -> None:
    if datos_juego["doble_chance_disponible"]:
        datos_juego["doble_chance_en_uso"] = True
        datos_juego["doble_chance_fallo"] = False
        datos_juego["doble_chance_disponible"] = False
    return None

def usar_pasar(datos_juego:dict, lista_preguntas:list) -> None:
    if not datos_juego.get("pasar_disponible"):
        return

    pasar_pregunta(datos_juego, lista_preguntas)
    datos_juego["respuestas_ocultas"] = []
    datos_juego["doble_chance_en_uso"] = False
    datos_juego["doble_chance_fallo"] = False
    datos_juego["tiempo_inicio_pregunta"] = pygame.time.get_ticks()
    datos_juego["pasar_disponible"] = False
    return None

def activar_pasar(datos_juego, lista_preguntas) -> None:
    if datos_juego["pasar_disponible"]:
        pasar_pregunta(datos_juego, lista_preguntas)
        datos_juego["pasar_disponible"] = False
        datos_juego["respuestas_ocultas"] = []
        datos_juego["bomba_animando"] = False
        datos_juego["bomba_pendientes"] = []
        datos_juego["tiempo_inicio_pregunta"] = pygame.time.get_ticks()
    return None

def activar_bomba(datos_juego, pregunta_actual) -> None:
    if not datos_juego["bomba_disponible"]:
        return

    opciones = ["opcion_A", "opcion_B", "opcion_C", "opcion_D"]
    correcta = pregunta_actual["opcion_correcta"]

    incorrectas = []

    for i in range(4):
        if pregunta_actual[opciones[i]] != correcta:
            incorrectas.append(i)

    while len(incorrectas) > 2:
        incorrectas.pop(random.randint(0, len(incorrectas)-1))

    datos_juego["respuestas_ocultas"] = incorrectas

    datos_juego["bomba_disponible"] = False
    return None


#ESTADISTICA

def reiniciar_estadisticas(datos_juego:dict) -> bool:
    if type(datos_juego) == dict:
        retorno = True
        datos_juego.update({
            "nombre": "",
            "tiempo_restante": datos_juego.get("tiempo_total", TIEMPO_TOTAL),
            "puntuacion":0,
            "cantidad_vidas":CANTIDAD_VIDAS,
            "tiempo_inicio_pregunta": pygame.time.get_ticks(),
            "correctas_seguidas": 0,
            "respuestas_ocultas": [],
            "doble_chance_en_uso": False,
            "doble_chance_fallo": False,
            "x2_activado": False,
            "bomba_disponible": True,
            "bomba_animando": False,
            "bomba_pendientes": [],
            "x2_disponible": True,
            "pasar_disponible": True,
            "doble_chance_disponible": True,
        })
    else:
        retorno = False
    
    return retorno

def actualizar_tiempo(tiempo_inicio:float,tiempo_actual:float,datos_juego:dict) -> bool:
    if type(datos_juego) == dict:
        retorno = True
        tiempo_transcurrido = int(tiempo_actual - tiempo_inicio)
        datos_juego["tiempo_restante"] = TIEMPO_TOTAL - tiempo_transcurrido
    else:
        retorno = False
        
    return retorno

def modificar_vida(datos_juego:dict,incremento:int) -> bool:
    if type(datos_juego) == dict and datos_juego.get("cantidad_vidas") != None:
        retorno = True
        datos_juego["cantidad_vidas"] += incremento
    else:
        retorno = False
        
    return retorno

def modificar_puntuacion(datos_juego:dict,incremento:int) -> bool:
    if type(datos_juego) == dict and datos_juego.get("puntuacion") != None:
        retorno = True
        datos_juego["puntuacion"] += incremento
    else:
        retorno = False
        
    return retorno

def actualizar_tiempo_pregunta(datos_juego) -> bool:
    tiempo_actual = pygame.time.get_ticks()
    transcurrido = (tiempo_actual - datos_juego["tiempo_inicio_pregunta"]) // 1000

    tiempo_total = datos_juego.get("tiempo_total", TIEMPO_TOTAL)

    restante = tiempo_total - transcurrido
    if restante < 0:
        restante = 0

    datos_juego["tiempo_restante"] = restante

    if restante == 0:
        modificar_vida(datos_juego, VIDA_ERROR)
        datos_juego["correctas_seguidas"] = 0
        datos_juego["respuestas_ocultas"] = []
        datos_juego["bomba_animando"] = False
        datos_juego["bomba_pendientes"] = []
        datos_juego["tiempo_inicio_pregunta"] = pygame.time.get_ticks()
        datos_juego["tiempo_restante"] = datos_juego.get("tiempo_total", TIEMPO_TOTAL)
        return True

    return False

def manejar_aciertos_consecutivos(datos_juego, es_correcta) -> None:
    if es_correcta:
        datos_juego["correctas_seguidas"] += 1

        if datos_juego["correctas_seguidas"] == 5:
            modificar_vida(datos_juego, 1)
            datos_juego["correctas_seguidas"] = 0

    else:
        datos_juego["correctas_seguidas"] = 0
    return None

#AJUSTES

def barra_volumen(screen, x, y, ancho=200, alto=20, volumen_actual=0.5) -> float:
    pygame.draw.rect(screen, (180,180,180), (x, y, ancho, alto))

    relleno = int(ancho * volumen_actual)
    pygame.draw.rect(screen, (50,200,50), (x, y, relleno, alto))

    porcentaje = int(volumen_actual * 100)
    texto = f"{porcentaje}%"
    superficie_texto = FUENTE_ARIAL_18.render(texto, True, COLOR_BLANCO)
    rect_texto = superficie_texto.get_rect(center=(x + ancho // 2, y + alto // 2))
    screen.blit(superficie_texto, rect_texto)

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if click[0]:
        if x <= mouse[0] <= x + ancho and y <= mouse[1] <= y + alto:
            volumen_actual = (mouse[0] - x) / ancho
            volumen_actual = max(0, min(1, volumen_actual))
            pygame.mixer.music.set_volume(volumen_actual)
            SONIDO_CLICK.set_volume(volumen_actual)
            SONIDO_ERROR.set_volume(volumen_actual)
            SONIDO_VIDA.set_volume(volumen_actual)

    return volumen_actual

def administrar_barra(datos_juego, pantalla) -> None:
    vol = datos_juego.get("volumen_musica", 0)
    vol = barra_volumen(pantalla, 150, 190, 500, 20, vol)
    datos_juego["volumen_musica"] = vol
    mostrar_texto(pantalla,"VOLUMEN", (290,120), FUENTE_ARIAL_50, color=COLOR_BLANCO)
    return None

def click_dificultad(boton_facil, boton_normal, boton_dificil, evento, datos_juego) -> dict:
    if boton_facil["rectangulo"].collidepoint(evento.pos):
        datos_juego["dificultad"] = "facil"
        datos_juego.update({
            "puntuacion_acierto": 30,
            "puntuacion_error": -10,
            "tiempo_total": 15,
            "tiempo_restante": 15,
            "tiempo_inicio_pregunta": pygame.time.get_ticks()
                })
        SONIDO_CLICK.play()

    if boton_normal["rectangulo"].collidepoint(evento.pos):
        datos_juego["dificultad"] = "normal"
        datos_juego.update({
            "puntuacion_acierto": 20,
            "puntuacion_error": -20,
            "tiempo_total": 12,
            "tiempo_restante": 12,
            "tiempo_inicio_pregunta": pygame.time.get_ticks()
                })
        SONIDO_CLICK.play()

    if boton_dificil["rectangulo"].collidepoint(evento.pos):
        datos_juego["dificultad"] = "dificil"
        datos_juego.update({
            "puntuacion_acierto": 10,
            "puntuacion_error": -30,
            "tiempo_total": 9,
            "tiempo_restante": 9,
            "tiempo_inicio_pregunta": pygame.time.get_ticks()
        })
        SONIDO_CLICK.play()
    return datos_juego

def resaltado_dificultad(boton_facil, boton_normal, boton_dificil, datos_juego, pantalla):
    seleccion = datos_juego.get("dificultad", "facil")
    if seleccion == "facil":
        resaltar_elemento(boton_facil, pantalla, COLOR_RESALTE, 4, 8)
    elif seleccion == "normal":
        resaltar_elemento(boton_normal, pantalla, COLOR_RESALTE, 4, 8)
    elif seleccion == "dificil":
        resaltar_elemento(boton_dificil, pantalla, COLOR_RESALTE, 4, 8)
    return None

#GAME_OVER

def manejar_texto_nombre(evento, datos_juego) -> None:
    nombre = datos_juego["nombre"]
    if evento.type == pygame.TEXTINPUT:
        if len(nombre) < 15:
            nombre += evento.text
    elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_BACKSPACE:
            nombre = nombre[:-1]
            datos_juego["ultimo_borrado"]
            
    datos_juego["nombre"] = nombre
    return None

def nombre_es_valido(nombre:str) -> bool:
    return 3 <= len(nombre) <= 15

def crear_boton_continuar(texto, x, y, ancho, alto, color_normal, color_inactivo, fuente, texto_x, texto_y, activo=True) -> dict:
    rect = pygame.Rect(x, y, ancho, alto)

    return {
        "rect": rect,
        "texto": texto,
        "color_normal": color_normal,
        "color_inactivo": color_inactivo,
        "activo": activo,
        "fuente": fuente,
        "texto_x": texto_x, 
        "texto_y": texto_y
    }

def dibujar_boton_continuar(pantalla, boton) -> None:
    color = boton["color_normal"] if boton["activo"] else boton["color_inactivo"]
    pygame.draw.rect(pantalla, color, boton["rect"], border_radius=10)

    superficie_texto = boton["fuente"].render(boton["texto"], True, (0,0,0))
    pantalla.blit(superficie_texto, (boton["texto_x"], boton["texto_y"]))
    return None

def boton_clickeado_continuar(eventos, boton) -> bool:
    if not boton["activo"]:
        return False

    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if boton["rect"].collidepoint(evento.pos):
                SONIDO_CLICK.play()
                return True
    return False

def ingreso_nombre(datos_juego, pantalla, cuadro_nombre, boton_continuar) -> None:
    nombre = datos_juego.get("nombre", "")
    if len(nombre) > 0:
        texto = f"{nombre}|" if datos_juego["bandera_texto"] else nombre
        mostrar_texto(cuadro_nombre["superficie"], texto, (10,10), FUENTE_ARIAL_30, COLOR_NEGRO)
    else:
        mostrar_texto(cuadro_nombre["superficie"], "Ingrese su nombre", (10,10), FUENTE_ARIAL_25, "#2E2D2D")

    pantalla.blit(cuadro_nombre["superficie"], cuadro_nombre["rectangulo"])

    if nombre_es_valido(nombre):
        boton_continuar["activo"] = True
    else:
        boton_continuar["activo"] = False
    return None

#RANKING

def mostrar_jugadores(pantalla, lista_ranking):
    y = 80
    for i, jugador in enumerate(lista_ranking):
        texto = f"{i+1}. {jugador['nombre']} - {jugador['puntuacion']} pts"
        mostrar_texto(pantalla, texto, (220, y + i * 50), FUENTE_ARIAL_40,COLOR_NEGRO)