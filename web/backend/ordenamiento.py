# ordenamiento.py

def merge_sort_descendente(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        izquierda = arr[:mid]
        derecha = arr[mid:]

        merge_sort_descendente(izquierda)
        merge_sort_descendente(derecha)

        i = j = k = 0
        while i < len(izquierda) and j < len(derecha):
            if izquierda[i] > derecha[j]:
                arr[k] = izquierda[i]
                i += 1
            else:
                arr[k] = derecha[j]
                j += 1
            k += 1

        while i < len(izquierda):
            arr[k] = izquierda[i]
            i += 1
            k += 1

        while j < len(derecha):
            arr[k] = derecha[j]
            j += 1
            k += 1

    return arr


def ordenamiento(words, contenido_texto):
    ocurrencias = []

    for word in words:
        count = contenido_texto.count(word)
        ocurrencias.append(count)

    new = ocurrencias.copy()
    new = merge_sort_descendente(new)

    # Reordena las palabras según las ocurrencias
    for i in range(len(new) // 2):
        idx = ocurrencias.index(new[i])
        words[i], words[idx] = words[idx], words[i]

    return words
