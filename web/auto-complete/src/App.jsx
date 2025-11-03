import { useState } from 'react';
import { obtenerIndicesPatrones, obtenerSugerencias, subirArchivo } from './services/api';

const suggestions = [
  "React", "Vue", "Angular", "Svelte", "TailwindCSS", "JavaScript", "TypeScript", "Node.js", "HTML", "CSS", "Redux", "GraphQL"
];

function App() {
  const [inputText, setInputText] = useState("");
  const [filteredSuggestions, setFilteredSuggestions] = useState([]);
  const [indexesPatrones, setindexesPatrones] = useState([]);
  const [fileContent, setFileContent] = useState("");
  const [fileName, setFileName] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [estadisticas, setEstadisticas] = useState({
    totalOcurrencias: 0,
    tiempoBusqueda: 0,
    tiempoAutocompletado: 0
  })

  // Manejar la carga del archivo
  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (event) => {
      setFileContent(event.target.result);
    };
    reader.readAsText(file);

    try {
      setLoading(true);
      setError(null);
      const response = await subirArchivo(file);
      setFileName(response.file_name);
      console.log('Archivo subido:', response);
    } catch (err) {
      setError('Error al subir el archivo');
      console.error(err);
    } finally {
      setLoading(false);
    }

  };

  // Filtrar las sugerencias según el texto ingresado
  const handleInputChange = async (e) => {
    const query = e.target.value;
    setInputText(query);

    if (query === "" || !fileName) {
      setFilteredSuggestions([]);
      return;
    }

    try {
      setLoading(true);
      const response = await obtenerSugerencias(fileName, query);
      setFilteredSuggestions(response.sugerencias || []);
      setEstadisticas(prev => ({
        ...prev,
        tiempoAutocompletado: response.tiempo_busqueda || 0
      }));
      console.log(response.tiempo_busqueda)
    } catch (err) {
      console.error('Error al obtener sugerencias', err);
      setFilteredSuggestions([]);
    } finally {
      setLoading(false);
    }
  };

  // Manejar clic en sugerencia
  const handleSuggestionClick = async (suggestion) => {
    setInputText(suggestion);
    setFilteredSuggestions([]);

    try {
      setLoading(true);
      const response = await obtenerIndicesPatrones(fileName, suggestion);
      setindexesPatrones(response.ocurrencias || []);
      setEstadisticas(prev => ({
        ...prev,
        totalOcurrencias: response.total_ocurrencias || 0,
        tiempoBusqueda: response.tiempo_busqueda || 0,
      }));
      console.log('Índices encontrados:', response.ocurrencias, 'palabra:', suggestion);
    } catch (err) {
      console.error('Error al obtener indices', err);
      setindexesPatrones([]);
      setEstadisticas({
        totalOcurrencias: 0,
        tiempoBusqueda: 0,
        tiempoAutocompletado: 0
      });
    } finally {
      setLoading(false);
    }
  };

  const resaltarTexto = (texto, indices, patron) => {
    if (!indices || indices.length === 0) {
      return texto;
    }

    const fragmentos = [];
    let ultimoIndice = 0;

    indices.forEach((inicio) => {
      const fin = inicio + patron.length;
      
      // Texto antes del patrón
      fragmentos.push(texto.substring(ultimoIndice, inicio));
      
      // Patrón resaltado
      fragmentos.push(
        <mark key={inicio} className="bg-yellow-300">
          {texto.substring(inicio, fin)}
        </mark>
      );
      
      ultimoIndice = fin;
    });

    // Texto restante después del último patrón
    fragmentos.push(texto.substring(ultimoIndice));

    return fragmentos;
  };

  return (
    <div className="relative w-[100vw] h-[100vh] flex flex-wrap justify-center items-center">
      <video
        autoPlay
        muted
        loop
        className="absolute top-0 left-0 w-full h-full object-cover z-[-1]"
      >
        <source src="/assets/background.mp4" type="video/mp4" />
        Your browser does not support the video tag.
      </video>

      <div className="w-[80%] h-[80%] bg-gray-50 flex flex-col z-10 p-4">
        {/* Sección superior: Botón de subir archivo y vista del texto */}
        <div className="w-full h-[70%] flex flex-col mb-4">
          <div className="mb-2 flex items-center justify-between">
            <input
              type="file"
              accept=".txt"
              onChange={handleFileUpload}
              className="px-4 py-2 bg-blue-500 text-white rounded-md cursor-pointer hover:bg-blue-700"
            />
            
            {/* Estadísticas */}
            {estadisticas.totalOcurrencias > 0 && (
              <div className="flex gap-6 text-sm">
                <div>
                  <span className="text-gray-600">Coincidencias: </span>
                  <span className="font-bold text-blue-600">{estadisticas.totalOcurrencias}</span>
                </div>
                <div>
                  <span className="text-gray-600">Busqueda: </span>
                  <span className="font-bold text-green-600">{(estadisticas.tiempoBusqueda * 1000).toFixed(3)} ms</span>
                </div>
                <div>
                  <span className="text-gray-600">Autocompletado: </span>
                  <span className="font-bold text-purple-600">{(estadisticas.tiempoAutocompletado * 1000).toFixed(3)} ms</span>
                </div>
              </div>
            )}
          </div>
          
          <div className="flex-1 bg-white border-2 border-gray-300 rounded-md p-4 overflow-auto">
            <pre className="whitespace-pre-wrap text-sm">
              {fileContent ? resaltarTexto(fileContent, indexesPatrones, inputText) : "No hay archivo cargado. Selecciona un archivo .txt"}
            </pre>
          </div>
        </div>

        {/* Sección inferior: Input y sugerencias */}
        <div className="w-full h-[25%] flex gap-4">
          {/* Input de búsqueda */}
          <div className="w-[70%] h-full">
            <input
              type="text"
              value={inputText}
              onChange={handleInputChange}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && inputText && fileName) {
                  handleSuggestionClick(inputText)
                }
              }}
              className="w-full h-full p-4 border-2 border-gray-300 rounded-md text-lg"
              placeholder="Escribe para buscar..."
            />
          </div>

          {/* Panel de sugerencias */}
          <div className="w-[30%] h-full bg-gray-100 border-2 border-gray-300 rounded-md flex flex-col items-center justify-start overflow-auto p-2">
            <h3 className="text-sm font-bold mb-2">Sugerencias:</h3>
            {loading ? (
              <p className="text-gray-500 text-sm">Buscando...</p>
            ) : filteredSuggestions && filteredSuggestions.length > 0 ? (
              filteredSuggestions.map((suggestion, index) => (
                <button
                  className="w-full h-[40px] bg-blue-500 text-white rounded-md mb-2 hover:bg-blue-700 transition-colors"
                  key={index}
                  onClick={() => handleSuggestionClick(suggestion)}
                >
                  {suggestion}
                </button>
              ))
            ) : (
              <p className="text-gray-500 text-sm">No hay sugerencias</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;