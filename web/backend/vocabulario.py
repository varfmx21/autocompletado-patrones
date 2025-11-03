#!/usr/bin/env python3

import re
import time

class NodoTrie:
    """Nodo del árbol Trie"""
    def __init__(self):
        self.hijos = {}
        self.es_fin_palabra = False

class Trie:
    """Estructura de datos Trie para autocompletado eficiente"""
    def __init__(self):
        self.raiz = NodoTrie()
    
    def insertar(self, palabra):
        """Inserta una palabra en el Trie"""
        nodo = self.raiz
        for caracter in palabra:
            if caracter not in nodo.hijos:
                nodo.hijos[caracter] = NodoTrie()
            nodo = nodo.hijos[caracter]
        nodo.es_fin_palabra = True
    
    def buscar_prefijo(self, prefijo):
        """Busca si existe un prefijo en el Trie y retorna el nodo"""
        nodo = self.raiz
        for caracter in prefijo:
            if caracter not in nodo.hijos:
                return None
            nodo = nodo.hijos[caracter]
        return nodo
    
    def _obtener_palabras_desde_nodo(self, nodo, prefijo, palabras):
        """Método auxiliar recursivo para obtener todas las palabras desde un nodo"""
        if nodo.es_fin_palabra:
            palabras.append(prefijo)
        
        for caracter, hijo in sorted(nodo.hijos.items()):
            self._obtener_palabras_desde_nodo(hijo, prefijo + caracter, palabras)
    
    def autocompletar(self, prefijo):
        """Retorna todas las palabras que comienzan con el prefijo dado"""
        nodo = self.buscar_prefijo(prefijo)
        if nodo is None:
            return []
        
        palabras = []
        self._obtener_palabras_desde_nodo(nodo, prefijo, palabras)
        return palabras
    
    def _contar_palabras(self, nodo):
        """Cuenta recursivamente el número de palabras en el Trie"""
        count = 1 if nodo.es_fin_palabra else 0
        for hijo in nodo.hijos.values():
            count += self._contar_palabras(hijo)
        return count

    def __len__(self):
        """Retorna el número total de palabras en el Trie"""
        return self._contar_palabras(self.raiz)

def crear_vocabulario(texto):
    texto_minusculas = texto.lower()
    
    texto_limpio = re.sub(r'[^a-záéíóúñü\s]', ' ', texto_minusculas)
    
    palabras = texto_limpio.split()
    
    vocabulario = set(palabras)
    
    vocabulario.discard('')

    vocabulario = sorted(vocabulario)

    return vocabulario

def crear_trie(texto):
    vocabulario = crear_vocabulario(texto)
    
    trie = Trie()
    
    # Insertar todas las palabras en el Trie
    for palabra in vocabulario:
        trie.insertar(palabra)
    
    return trie

def sugerir_palabras(trie, prefijo):    
    # Convertir prefijo a minúsculas para búsqueda consistente
    prefijo = prefijo.lower()
    
    # Medir tiempo de búsqueda
    inicio = time.perf_counter()
    
    # Obtener todas las palabras que coinciden con el prefijo
    sugerencias = trie.autocompletar(prefijo)
    
    fin = time.perf_counter()
    tiempo = fin - inicio
    
    return sugerencias, tiempo

if __name__ == "__main__":
    # Ejemplo de uso
    ruta_archivo = '../src/At the mountains of madness.txt'
    
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            texto = archivo.read()
        
        print("Creando vocabulario y Trie...")
        
        # Crear vocabulario
        vocabulario = crear_vocabulario(texto)
        print(f"✓ Tamaño del vocabulario: {len(vocabulario)} palabras únicas")
        
        # Crear Trie desde el texto
        trie = crear_trie(texto)
        print(f"✓ Trie creado con {len(vocabulario)} palabras\n")
        
        # Ejemplos de autocompletado
        print("=" * 60)
        print("EJEMPLOS DE AUTOCOMPLETADO")
        print("=" * 60)
        
        prefijos_prueba = ["the", "moun", "exp", "ant", "ice"]
        
        for prefijo in prefijos_prueba:
            sugerencias, tiempo = sugerir_palabras(trie, prefijo)
            print(type(sugerencias))
            print(f"\nPrefijo: '{prefijo}' (tiempo: {tiempo*1000:.4f} ms)")
            if sugerencias:
                print(f"Sugerencias ({len(sugerencias)}):")
                for palabra in sugerencias:
                    print(f"  → {palabra}")
            else:
                print("  (No hay sugerencias)")
        
    except FileNotFoundError:
        print("Error: No se encontró el archivo")
    except Exception as e:
        print(f"Error: {e}")