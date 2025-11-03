# 🚀 Backend - API de Búsqueda KMP y Autocompletado

## 🛠️ Requisitos

- **Python 3.8 o superior**
- pip (gestor de paquetes de Python)

## 📦 Instalación

### 1. Crear entorno virtual

```bash
python3 -m venv env
```

### 2. Activar entorno virtual

**Linux/Mac:**
```bash
source env/bin/activate
```

**Windows (PowerShell):**
```powershell
.\env\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
.\env\Scripts\activate.bat
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 🚀 Ejecución

### Iniciar el servidor

```bash
uvicorn main:app --reload
```

**Opciones adicionales:**

```bash
# Con host y puerto específicos
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Sin auto-reload (para producción)
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Verificar que funciona

Abre tu navegador en:
- **API Root**: http://localhost:8000/
- **Documentación Swagger**: http://localhost:8000/docs ⭐ (Recomendado para probar)
- **Documentación ReDoc**: http://localhost:8000/redoc

## 📚 Endpoints Disponibles

### 📤 Subir Archivo
```http
POST /upload
```
Sube un archivo `.txt` y crea su vocabulario Trie.

**Body:** `multipart/form-data`
- `archivo`: archivo .txt

**Response:**
```json
{
  "file_name": "texto-1.txt",
  "mensaje": "Archivo procesado, ID: texto-1.txt"
}
```

---

### 🔍 Buscar Patrón (KMP)
```http
POST /kmp
```
Busca todas las ocurrencias de un patrón en el texto.

**Body:** `application/json`
```json
{
  "file_name": "texto-1.txt",
  "patron": "the"
}
```

**Response:**
```json
{
  "file_name": "texto-1.txt",
  "patron": "the",
  "ocurrencias": [0, 15, 32, 45],
  "total_ocurrencias": 4,
  "tiempo_busqueda": 0.000234
}
```

---

### ✨ Autocompletado
```http
POST /autocompletado
```
Sugiere palabras que comienzan con el prefijo dado.

**Body:** `application/json`
```json
{
  "file_name": "texto-1.txt",
  "palabra": "the"
}
```

**Response:**
```json
{
  "sugerencias": ["the", "their", "them", "then", "theory"],
  "tiempo_busqueda": 0.000156
}
```

---

### 📖 Obtener Vocabulario
```http
GET /vocabulario/{file_name}
```
Obtiene todas las palabras únicas del archivo.

**Response:**
```json
{
  "file_id": "texto-1.txt",
  "vocabulario": ["a", "about", "all", "an", "and", ...],
  "total_palabras_unicas": 1234
}
```

---

### 📁 Listar Archivos
```http
GET /archivos
```
Lista todos los archivos en memoria con sus estadísticas.

**Response:**
```json
{
  "total_archivos": 2,
  "limite_maximo": 5,
  "archivos": [
    {
      "file_id": "texto-1.txt",
      "total_palabras": 5678,
      "vocabulario_size": 1234
    }
  ]
}
```

---

### 🗑️ Eliminar Archivo
```http
DELETE /archivo/{file_name}
```
Elimina un archivo específico de la memoria.

---

### 🧹 Limpiar Memoria
```http
DELETE /archivos
```
Elimina todos los archivos de la memoria.

---