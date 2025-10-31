#!/usr/bin/env python3

import time

def lps(patron):

    m = len(patron)
    if m == 0:
        return []
    
    v = [0] * m
    j = 0
    i = 1
    
    while i < m:
        if patron[i] == patron[j]:
            v[i] = j + 1
            i += 1
            j += 1
        else:
            if j == 0:
                v[i] = 0
                i += 1
            else:
                j = v[j - 1]
    
    return v

def kmp(texto, patron):

    if not patron or not texto:
        return -1
    
    m = len(patron)
    n = len(texto)
    
    v = lps(patron)
    i = 0  
    j = 0  
    ocurrencias = []
    
    while i < n:
        if texto[i] == patron[j]:
            i += 1
            j += 1
        
        if j == m:
            ocurrencias.append(i - j)
            j = v[j - 1]  
        elif i < n and texto[i] != patron[j]:
            if j == 0:
                i += 1
            else:
                j = v[j - 1]
    
    return ocurrencias

def format_time(tiempo_segundos):
    
    if tiempo_segundos >= 1.0:
        return f"{tiempo_segundos:.3f} segundos"
    elif tiempo_segundos >= 0.001:
        return f"{tiempo_segundos * 1000:.3f} milisegundos"
    else:
        return f"{tiempo_segundos * 1000000:.3f} microsegundos"

def mostrar_resultados(texto, patron, ocurrencias):
    
    if ocurrencias:        

        for i, pos in enumerate(ocurrencias, 1):
            contexto = texto[pos:pos + 50]
            
            if len(contexto) == 50:
                contexto += "..."
            
            print(f"  {i}. [{pos}]: \"{contexto}\"")
    else:
        print("No se encontraron ocurrencias")

if __name__ == "__main__":

    ruta_archivo = 'src/vocabulary.txt'

    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            texto = archivo.read()
    except FileNotFoundError:
        print("Error: No se encontró el archivo")
        exit(1)
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        exit(1)
    
    palabras_buscar = [
        "quick"
    ]

    total_ocurrencias = 0
    tiempo_total = 0

    print("="*70)
    print(f"\tBÚSQUEDA DE OCURRENCIAS USANDO EL ALGORITMO KMP")
    print("="*70)

    total_ocurrencias = 0
    tiempo_total = 0
    
    for palabra in palabras_buscar:
        tiempo_inicio = time.time()
        ocurrencias = kmp(texto, palabra)
        tiempo_fin = time.time()
        tiempo_busqueda = tiempo_fin - tiempo_inicio
        
        total_ocurrencias += len(ocurrencias)
        tiempo_total += tiempo_busqueda
        
        mostrar_resultados(texto, palabra, ocurrencias)
    
    print(f"\n\t--- TIEMPO TOTAL: {format_time(tiempo_total)} segundos ---")