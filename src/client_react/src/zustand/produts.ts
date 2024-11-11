import {create} from 'zustand';

// Interface para o tipo Product
export interface Product {
    store_name: string;
    product_code: number;
    stock: number;
    product_short_name: string;
    product_name: string;
    description: string;
    category: string;
    sub_category: string;
    brand: string;
    content_value: number;
    content_unit: string;
    inventory_date: string;
    image: string;
}

// Definindo o tipo ProductStore para o Zustand
type ProductStore = {
    product: Product[];
    setProduct: (products: Product[]) => void; // Função para definir a lista de produtos
    clearProduct: () => void; // Função para limpar a lista de produtos
};

// Criando o Zustand store para os produtos
export const useProductStore = create<ProductStore>((set) => ({
    // Estado inicial para o array de produtos
    product: [{
        store_name: "",
        product_code: 0,
        stock: 0,
        product_short_name: "",
        product_name: "",
        description: "",
        category: "",
        sub_category: "",
        brand: "",
        content_value: 0,
        content_unit: "",
        inventory_date: "",
        image: ""
    }],
    
    // Função para definir produtos no estado
    setProduct: (products: Product[]) => set({ product: products }),

    // Função para limpar o array de produtos
    clearProduct: () => set({ product: [] }),
}));
