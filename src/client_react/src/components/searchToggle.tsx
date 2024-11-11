import { useState } from 'react';
import { Search } from 'lucide-react';

export function SearchToggle() {
    const [isVisible, setIsVisible] = useState(false);

    // Função visibilidade barra de pesquisa
    const toggleSearch = () => {
        setIsVisible(!isVisible);
    };

    return (  
        <div className="p-2 flex items-center justify-between">   
          {isVisible && (  
            <input  
              type="search"  
              placeholder="Buscar"  
              className="flex-grow border rounded p-1"  
              autoFocus  
            />  
          )} 
          <button onClick={toggleSearch} className="p-2">  
            <Search size={24} />  
          </button>  
        </div>  
      );
}
