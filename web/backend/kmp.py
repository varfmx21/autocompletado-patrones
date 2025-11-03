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
        return []
    
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

def imprimir_contexto(texto, palabra, ocurrencias, caracteres=50):
    """
    Imprime cada ocurrencia de la palabra con contexto alrededor
    
    Args:
        texto: El texto completo donde se buscó
        palabra: La palabra buscada
        ocurrencias: Lista de posiciones donde se encontró la palabra
        caracteres: Cantidad de caracteres a mostrar antes y después (default: 50)
    """
    if not ocurrencias:
        print("No se encontraron ocurrencias")
        return
    
    print(f"\nSe encontraron {len(ocurrencias)} ocurrencias de '{palabra}':\n")
    print("=" * 80)
    
    for idx, pos in enumerate(ocurrencias, 1):
        # Calcular inicio y fin del contexto
        inicio = max(0, pos - caracteres)
        fin = min(len(texto), pos + len(palabra) + caracteres)
        
        # Extraer el contexto
        palabra_encontrada = texto[pos:pos + len(palabra)]
        contexto_despues = texto[pos + len(palabra):fin]
        
        # Imprimir
        print(f"\nOcurrencia #{idx} (posición {pos}):")
        print(f"[{palabra_encontrada}]{contexto_despues}...")
        print("-" * 80)

def buscar_texto(texto, palabra):

    inicio = time.perf_counter()
    ocurrencias = kmp(texto, palabra)
    fin = time.perf_counter()

    tiempo = fin - inicio

    num_ocurrencias = len(ocurrencias)

    return ocurrencias, num_ocurrencias, tiempo

if __name__ == "__main__":
    ruta_archivo = '../src/texto-1.txt'

    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            texto = archivo.read()
    except FileNotFoundError:
        print("Error: No se encontró el archivo")
        exit(1)
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        exit(1)
    
    palabras_buscar = "a"

    ocurrencias, num_ocurrencias, tiempo = buscar_texto(texto, palabras_buscar)

    imprimir_contexto(texto, palabras_buscar, ocurrencias, caracteres=50)

    print(ocurrencias)