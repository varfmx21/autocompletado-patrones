import { useState } from 'react';
import { obtenerSugerencias, subirArchivo } from './services/api';

const suggestions = [
  "React", "Vue", "Angular", "Svelte", "TailwindCSS", "JavaScript", "TypeScript", "Node.js", "HTML", "CSS", "Redux", "GraphQL"
];

function App() {
  const [inputText, setInputText] = useState("");
  const [filteredSuggestions, setFilteredSuggestions] = useState([]);
  const [fileContent, setFileContent] = useState("");
  const [fileName, setFileName] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

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
    } catch (err) {
      console.error('Error al obtener sugerencias', err);
      setFilteredSuggestions([]);
    } finally {
      setLoading(false);
    }
  };

  // Manejar clic en sugerencia
  const handleSuggestionClick = (suggestion) => {
    setInputText(suggestion);
    setFilteredSuggestions([]);
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
        <div className="w-full h-[60%] flex flex-col mb-4">
          <div className="mb-2">
            <input
              type="file"
              accept=".txt"
              onChange={handleFileUpload}
              className="px-4 py-2 bg-blue-500 text-white rounded-md cursor-pointer hover:bg-blue-700"
            />
          </div>
          
          <div className="flex-1 bg-white border-2 border-gray-300 rounded-md p-4 overflow-auto">
            <pre className="whitespace-pre-wrap text-sm">
              {fileContent || "No hay archivo cargado. Selecciona un archivo .txt"}
            </pre>
          </div>
        </div>

        {/* Sección inferior: Input y sugerencias */}
        <div className="w-full h-[35%] flex gap-4">
          {/* Input de búsqueda */}
          <div className="w-[70%] h-full">
            <input
              type="text"
              value={inputText}
              onChange={handleInputChange}
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