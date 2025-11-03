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

def z_algorithm(texto, patron):
    if not patron or not texto:
        return []
    
    s = patron + "$" + texto
    n = len(s)
    m = len(patron)
    
    z = z_function(s)
    
    ocurrencias = []
    for i in range(m + 1, n):
        if z[i] == m:
            ocurrencias.append(i - m - 1)
    
    return ocurrencias

def imprimir_contexto(texto, palabra, ocurrencias, caracteres=50):
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

def buscar_texto_z(texto, palabra):
    inicio = time.perf_counter()
    ocurrencias = z_algorithm(texto, palabra)
    fin = time.perf_counter()

    tiempo = fin - inicio

    num_ocurrencias = len(ocurrencias)

    return ocurrencias, num_ocurrencias, tiempo

if __name__ == "__main__":
    ruta_archivo = '/home/c4rnage/Desktop/c4rnage/repos/autocompletado-patrones/web/src/The call of Cthulhu.txt'

    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            texto = archivo.read()
    except FileNotFoundError:
        print("Error: No se encontró el archivo")
        exit(1)
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        exit(1)
    
    palabras_buscar = "Cthulhu"

    print("=" * 80)
    print(f"Buscando la palabra: '{palabras_buscar}'")
    print("=" * 80)

    # Probar con KMP
    print("\n>>> ALGORITMO KMP <<<")
    ocurrencias_kmp, num_ocurrencias_kmp, tiempo_kmp = buscar_texto(texto, palabras_buscar)
    print(f"Ocurrencias encontradas: {num_ocurrencias_kmp}")
    print(f"Tiempo de búsqueda: {tiempo_kmp*1000:.4f} ms")
    print(f"Posiciones: {ocurrencias_kmp}")

    # Probar con Z-algorithm
    print("\n>>> ALGORITMO Z <<<")
    ocurrencias_z, num_ocurrencias_z, tiempo_z = buscar_texto_z(texto, palabras_buscar)
    print(f"Ocurrencias encontradas: {num_ocurrencias_z}")
    print(f"Tiempo de búsqueda: {tiempo_z*1000:.4f} ms")
    print(f"Posiciones: {ocurrencias_z}")

    # Mostrar contexto de las ocurrencias
    imprimir_contexto(texto, palabras_buscar, ocurrencias_kmp, caracteres=50)
