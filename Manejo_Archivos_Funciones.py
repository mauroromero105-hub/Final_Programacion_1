import json
import os

def cargar_preguntas(nombre_archivo: str):
    preguntas = []

    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()

            if lineas:
                lineas = lineas[1:]

            for linea in lineas:
                fila = linea.strip().split(',')
                if len(fila) < 6:
                    print("Fila inválida (ignorada):", fila)
                    continue

                preguntas.append({
                    "pregunta": fila[0],
                    "opcion_A": fila[1],
                    "opcion_B": fila[2],
                    "opcion_C": fila[3],
                    "opcion_D": fila[4],
                    "opcion_correcta": fila[5]
                })

    return preguntas


def guardar_puntaje_json(nombre_archivo: str, nombre: str, puntuacion: int):
    ranking = []


    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, "r", encoding="utf-8") as archivo:
            try:
                ranking = json.load(archivo)
            except json.JSONDecodeError:
                ranking = []

    
    nombre_encontrado = False
    for jugador in ranking:
        if jugador["nombre"].lower() == nombre.lower():
            nombre_encontrado = True
            # Actualizar solo si el puntaje es mayor
            if puntuacion > jugador["puntuacion"]:
                jugador["puntuacion"] = puntuacion
            break

   
    if not nombre_encontrado:
        ranking.append({
            "nombre": nombre,
            "puntuacion": puntuacion
        })

    
    ranking.sort(key=lambda x: x["puntuacion"], reverse=True)

    
    ranking = ranking[:10]

    
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        json.dump(ranking, archivo, indent=4, ensure_ascii=False)

def leer_json(nombre_archivo: str) -> list:
    if not os.path.exists(nombre_archivo):
        return []

    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        try:
            ranking = json.load(archivo)
        except json.JSONDecodeError:
            ranking = []

    return ranking

