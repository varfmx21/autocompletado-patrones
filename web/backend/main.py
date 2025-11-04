from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware  # ← AGREGAR ESTA LÍNEA
from pydantic import BaseModel
from typing import List
import kmp
import ordenamiento
import vocabulario

app = FastAPI()
# ==================== CORS ====================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En desarrollo permite todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, DELETE, etc.)
    allow_headers=["*"],  # Permite todos los headers
)

# ==================== MODELOS ====================

class FileProcessResponse(BaseModel):
    file_name: str
    mensaje: str

class TextSearchRequest(BaseModel):
    file_name: str
    patron: str

class TextSearchResponse(BaseModel):
    file_name: str
    patron: str
    ocurrencias: List[int]
    total_ocurrencias: int
    tiempo_busqueda: float

class AutoCompleteResponse(BaseModel):
    sugerencias: List[str]
    tiempo_busqueda: float

class AutoCompleteRequest(BaseModel):
    file_name: str
    palabra: str

# ==================== MEMORIA TEMPORAL ====================

archivos = {}
MAX_ARCHIVOS = 5

# ==================== ENDPOINTS ====================
@app.get("/")
async def root():
    return {
        "message": "API para búsquedas por KMP y autocompletado de texto",
        "version": "1.0.0",
        "total_endpoints": 7,
        "endpoints": [
            {
                "path": "/",
                "method": "GET",
                "descripcion": "Información general de la API y lista de endpoints disponibles",
                "entrada": "Ninguna",
                "salida": "Objeto JSON con información de la API y endpoints"
            },
            {
                "path": "/upload",
                "method": "POST",
                "descripcion": "Sube un archivo .txt y crea su vocabulario Trie para búsquedas",
                "entrada": "archivo: UploadFile (.txt)",
                "salida": {
                    "file_name": "string - nombre del archivo",
                    "mensaje": "string - confirmación de procesamiento"
                },
                "nota": f"Límite máximo: {MAX_ARCHIVOS} archivos"
            },
            {
                "path": "/kmp",
                "method": "POST",
                "descripcion": "Busca todas las ocurrencias de un patrón en el texto usando algoritmo KMP",
                "entrada": {
                    "file_name": "string - nombre del archivo previamente subido",
                    "patron": "string - palabra o frase a buscar"
                },
                "salida": {
                    "file_name": "string",
                    "patron": "string",
                    "ocurrencias": "array[int] - posiciones donde se encontró el patrón",
                    "total_ocurrencias": "int - cantidad de ocurrencias",
                    "tiempo_busqueda": "float - tiempo en segundos"
                }
            },
            {
                "path": "/autocompletado",
                "method": "POST",
                "descripcion": "Sugiere palabras que comienzan con el prefijo dado usando estructura Trie",
                "entrada": {
                    "file_name": "string - nombre del archivo previamente subido",
                    "palabra": "string - prefijo para autocompletar"
                },
                "salida": {
                    "sugerencias": "array[string] - lista de palabras sugeridas",
                    "tiempo_busqueda": "float - tiempo en segundos"
                }
            },
            {
                "path": "/vocabulario/{file_name}",
                "method": "GET",
                "descripcion": "Obtiene el vocabulario completo (palabras únicas) de un archivo",
                "entrada": "file_name: string (parámetro de ruta)",
                "salida": {
                    "file_id": "string",
                    "vocabulario": "array[string] - lista de palabras únicas",
                    "total_palabras_unicas": "int"
                }
            },
            {
                "path": "/archivos",
                "method": "GET",
                "descripcion": "Lista todos los archivos almacenados en memoria con sus estadísticas",
                "entrada": "Ninguna",
                "salida": {
                    "total_archivos": "int",
                    "limite_maximo": "int",
                    "archivos": "array - información de cada archivo"
                }
            },
            {
                "path": "/archivo/{file_name}",
                "method": "DELETE",
                "descripcion": "Elimina un archivo específico de la memoria",
                "entrada": "file_name: string (parámetro de ruta)",
                "salida": {
                    "mensaje": "string - confirmación de eliminación",
                    "archivos_restantes": "int"
                }
            },
            {
                "path": "/archivos",
                "method": "DELETE",
                "descripcion": "Limpia todos los archivos de la memoria",
                "entrada": "Ninguna",
                "salida": {
                    "mensaje": "string - confirmación con cantidad eliminada"
                }
            }
        ],
        "uso_tipico": [
            "1. POST /upload - Subir archivo de texto",
            "2. POST /kmp - Buscar patrones en el texto",
            "3. POST /autocompletado - Obtener sugerencias de palabras",
            "4. GET /vocabulario/{file_name} - Ver vocabulario completo",
            "5. GET /archivos - Listar archivos en memoria",
            "6. DELETE /archivo/{file_name} - Eliminar archivo específico"
        ]
    }

@app.post("/upload", response_model=FileProcessResponse)
async def subir_archivo(archivo: UploadFile = File()):
    if not archivo.filename or not archivo.filename.endswith('.txt'):
        raise HTTPException(
            status_code=400,
            detail="Solo se aceptan archivos .txt"
        )
    
    try:
        contenido_bytes = await archivo.read()
        texto = contenido_bytes.decode('utf-8')
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error al leer el archivo {str(e)}"
        )
    
    if not texto.strip():
        raise HTTPException(
            status_code=400,
            detail="El archivo está vacio"
        )
    
    # Creación del vocabulario
    trie_vocabulario = vocabulario.crear_trie(texto)

    if len(archivos) >= MAX_ARCHIVOS and archivo.filename not in archivos:
        raise HTTPException(
            status_code=507,
            detail="Limite de archivos alcanzado. Elimina archivos"
        )
    
    filename = archivo.filename or "unnamed.txt"
    
    archivos[filename] = {
        "texto": texto,
        "vocabulario": trie_vocabulario
    }

    return FileProcessResponse(
        file_name=filename,
        mensaje=f"Archivo procesado, ID: {filename}"
    )


@app.post("/kmp", response_model=TextSearchResponse)
async def buscar_patrones(request: TextSearchRequest):
    if request.file_name not in archivos:
        raise HTTPException(
            status_code=404,
            detail="Primero debes subir un archivo. Utiliza /upload"
        )
    
    if not request.patron:
        raise HTTPException(
            status_code=400,
            detail="El patrón no debe estar vacio."
        )
    
    texto = archivos[request.file_name]["texto"]

    ocurrencias, num_ocurrencias, tiempo = kmp.buscar_texto(texto, request.patron)

    return TextSearchResponse(
        file_name=request.file_name,
        patron=request.patron,
        ocurrencias=ocurrencias,
        total_ocurrencias=num_ocurrencias,
        tiempo_busqueda=tiempo
    )

@app.post("/z", response_model=TextSearchResponse)
async def buscar_patrones_z(request: TextSearchRequest):
    if request.file_name not in archivos:
        raise HTTPException(
            status_code=404,
            detail="Primero debes subir un archivo. Utiliza /upload"
        )
    
    if not request.patron:
        raise HTTPException(
            status_code=400,
            detail="El patrón no debe estar vacio."
        )
    
    texto = archivos[request.file_name]["texto"]

    ocurrencias, num_ocurrencias, tiempo = kmp.buscar_texto_z(texto, request.patron)

    return TextSearchResponse(
        file_name=request.file_name,
        patron=request.patron,
        ocurrencias=ocurrencias,
        total_ocurrencias=num_ocurrencias,
        tiempo_busqueda=tiempo
    )



@app.post("/autocompletado", response_model=AutoCompleteResponse)
async def autocompletado(request: AutoCompleteRequest):
    if request.file_name not in archivos:
        raise HTTPException(
            status_code=404,
            detail="Primero debes subir un archivo. Utiliza /upload"
        )
    
    if not request.palabra:
        raise HTTPException(
            status_code=400,
            detail="Debes ingresar algún prefijo para sugerir."
        )
    
    data_archivo = archivos[request.file_name]
    trie = data_archivo["vocabulario"]
    texto = data_archivo["texto"]

    sugerencias, tiempo = vocabulario.sugerir_palabras(trie, request.palabra)

    if sugerencias:
        try:
            sugerencias = ordenamiento.ordenamiento(sugerencias, texto)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al ordenar las sugerencias: {str(e)}"
            )

    return AutoCompleteResponse(
        sugerencias=sugerencias,
        tiempo_busqueda=tiempo
    )

@app.get("/vocabulario/{file_name}")
async def obtener_vocabulario(file_name: str):
    if file_name not in archivos:
        raise HTTPException(
            status_code=404,
            detail=f"Archivo '{file_name}' no encontrado"
        )
    
    trie = archivos[file_name]["vocabulario"]

    vocabulario = trie.autocompletar("")
    
    return {
        "file_id": file_name,
        "vocabulario": vocabulario,
        "total_palabras_unicas": len(trie)
    }

@app.get("/archivos")
async def listar_archivos():
    archivos_info = []
    
    for file_id, data in archivos.items():
        archivos_info.append({
            "file_id": file_id,
            "total_palabras": len(data["texto"]),
            "vocabulario_size": len(data["vocabulario"]),
        })
    
    return {
        "total_archivos": len(archivos),
        "limite_maximo": MAX_ARCHIVOS,
        "archivos": archivos_info
    }

@app.delete("/archivo/{file_name}")
async def eliminar_archivo(file_name: str):
    """
    Elimina un archivo de la memoria
    """
    if file_name not in archivos:
        raise HTTPException(
            status_code=404,
            detail=f"Archivo '{file_name}' no encontrado"
        )
    
    del archivos[file_name]
    
    return {
        "mensaje": f"Archivo '{file_name}' eliminado exitosamente",
        "archivos_restantes": len(archivos)
    }

@app.delete("/archivos")
async def limpiar_memoria():
    """
    Limpia todos los archivos de la memoria
    """
    cantidad = len(archivos)
    archivos.clear()
    
    return {
        "mensaje": f"Memoria limpiada. {cantidad} archivo(s) eliminado(s)"
    }
