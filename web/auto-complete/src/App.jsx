import { useState } from 'react';

const suggestions = [
  "React", "Vue", "Angular", "Svelte", "TailwindCSS", "JavaScript", "TypeScript", "Node.js", "HTML", "CSS", "Redux", "GraphQL"
];

function App() {
  const [inputText, setInputText] = useState("");
  const [filteredSuggestions, setFilteredSuggestions] = useState([]);

  // Filtrar las sugerencias según el texto ingresado
  const handleInputChange = (e) => {
    const query = e.target.value;
    setInputText(query);

    if (query === "") {
      setFilteredSuggestions([]);
    } else {
      setFilteredSuggestions(suggestions.filter((word) => word.toLowerCase().includes(query.toLowerCase())));
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

          <div className="w-[70%] h-[70%] bg-gray-50 flex z-10">
            <div className="w-[70%] h-[100%] bg-blue-50 border-2">
              <textarea
                type="text"
                value={inputText}
                onChange={handleInputChange}
                className="w-[100%] h-[100%] justify-start items-start text-start p-[5%] resize-none"
                placeholder="Escribe algo..."
              />
            </div>

            <div className="w-[29%] h-[100%] bg-gray-100 flex flex-col items-center justify-start">
              {filteredSuggestions.map((suggestion, index) => (
                <button
                  className="w-[90%] h-[40px] bg-blue-500 text-white rounded-md m-[1%] hover:bg-blue-700 transition-colors"
                  key={index}
                  onClick={() => handleSuggestionClick(suggestion)}
                >
                  {suggestion}
                </button>
              ))}
            </div>
        </div>
    </div>
  );
}

export default App;
