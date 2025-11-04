const API_URL = 'http://localhost:8000';

export const subirArchivo = async (file) => {
    const formData = new FormData();
    formData.append('archivo', file)

    try {
        const response = await fetch(`${API_URL}/upload`, {
            method: 'POST',
            body: formData
        });
        return await response.json();
    } catch (error) {
        console.error('Error en subirArchivo', error);
        throw error;
    }
}

export const obtenerSugerencias = async (fileName, palabra) => {
    try {
        const response = await fetch(`${API_URL}/autocompletado`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                file_name: fileName,
                palabra: palabra
            })
        });
        return await response.json();
    } catch (error) {
        console.error('Error en obtenerSugerencias', error);
        throw error;
    }
}

export const obtenerIndicesPatrones = async (fileName, patron) => {
    try {
        const response = await fetch(`${API_URL}/kmp`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                file_name: fileName,
                patron: patron
            })
        });
        return await response.json();
    } catch (error) {
        console.error('Error en obtenerSugerencias', error);
        throw error;
    }
}

export const obtenerIndicesPatronesZ = async (fileName, patron) => {
    try {
        const response = await fetch(`${API_URL}/z`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                file_name: fileName,
                patron: patron
            })
        });
        return await response.json();
    } catch (error) {
        console.error('Error en obtenerSugerencias', error);
        throw error;
    }
}