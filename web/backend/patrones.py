#!/usr/bin/env python3

import time

def z_function(s):

    n = len(s)
    if n == 0:
        return []
    
    z = [0] * n
    
    l = 0
    r = 0
    
    for i in range(1, n):
        if i < r:
            z[i] = min(r - i, z[i - l])
        
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        
        if i + z[i] > r:
            l = i
            r = i + z[i]
    
    return z

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

def buscar_patron(texto, patron):

    if not patron or not texto:
        return []
    
    cadena_combinada = patron + "$" + texto
    z_array = z_function(cadena_combinada)
    
    longitud_patron = len(patron)
    ocurrencias = []
    
    for i in range(longitud_patron + 1, len(cadena_combinada)):
        if z_array[i] == longitud_patron:
            posicion_en_texto = i - longitud_patron - 1
            ocurrencias.append(posicion_en_texto)
    
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

    ruta_archivo = './The call of Cthulhu by H. P. Lovecraft.txt'

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
        "god"
    ]
    
    print("="*70)
    print(f"\tBÚSQUEDA DE OCURRENCIAS USANDO EL ALGORITMO Z")
    print("="*70)

    total_ocurrencias = 0
    tiempo_total = 0
    
    for i, palabra in enumerate(palabras_buscar, 1):
        tiempo_inicio = time.time()
        ocurrencias = buscar_patron(texto, palabra)
        tiempo_fin = time.time()
        tiempo_busqueda = tiempo_fin - tiempo_inicio
        
        total_ocurrencias += len(ocurrencias)
        tiempo_total += tiempo_busqueda
        
        mostrar_resultados(texto, palabra, ocurrencias)
    
    print(f"\n\t--- TIEMPO TOTAL: {format_time(tiempo_total)} segundos ---")

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