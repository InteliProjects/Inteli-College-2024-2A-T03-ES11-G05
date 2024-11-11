import { SetStateAction, useState } from 'react';

export function Categories() {
    // categoria ativa
    const [activeCategory, setActiveCategory] = useState('All');

    // alterar a categoria ativa
    const handleCategoryClick = (category: SetStateAction<string>) => {
        setActiveCategory(category);
    };

    return (
        <div className="flex justify-around mb-4">
            <button
                className={`${
                    activeCategory === 'All' ? 'text-red-500 border-b-2 border-red-500' : 'text-gray-500'
                }`}
                onClick={() => handleCategoryClick('All')}
            >
                All
            </button>
            <button
                className={`${
                    activeCategory === 'Perfume' ? 'text-red-500 border-b-2 border-red-500' : 'text-gray-500'
                }`}
                onClick={() => handleCategoryClick('Perfume')}
            >
                Perfume
            </button>
            <button
                className={`${
                    activeCategory === 'Makeup' ? 'text-red-500 border-b-2 border-red-500' : 'text-gray-500'
                }`}
                onClick={() => handleCategoryClick('Makeup')}
            >
                Makeup
            </button>
            <button
                className={`${
                    activeCategory === 'Cabelos' ? 'text-red-500 border-b-2 border-red-500' : 'text-gray-500'
                }`}
                onClick={() => handleCategoryClick('Cabelos')}
            >
                Cabelos
            </button>
            <button
                className={`${
                    activeCategory === 'Unhas' ? 'text-red-500 border-b-2 border-red-500' : 'text-gray-500'
                }`}
                onClick={() => handleCategoryClick('Unhas')}
            >
                Unhas
            </button>
        </div>
    );
}