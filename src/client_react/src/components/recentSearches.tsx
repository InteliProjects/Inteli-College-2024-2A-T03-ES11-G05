import LaVieEstBellePerfume from '../assets/produtos/LaVieEstBellePerfum.png';
import Cerave from '../assets/produtos/CeraveImage.png';
import { ProductCard } from "../components/productCard";
import { useUserStore } from '@/zustand/user';
import { useEffect, useState } from 'react';
import { salesMan_inventory } from '@/api/login';
import { useProductStore } from '@/zustand/produts';

interface Product {
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
  inventory_date: string; // Ou Date, se preferir trabalhar com objetos de data
  image: string
}

export function RecentSearches() {
  const [loading, setLoading] = useState<boolean>(false);
  const user = useUserStore((state) => state.user);
  const product = useProductStore((state) => state.product);
  const setProduct = useProductStore((state) => state.setProduct);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true); // Início do carregamento

        // Faz a requisição apenas se o token existir
        if (user.access_toke) {
          const result = await salesMan_inventory(user.access_toke);

          // Array de imagens para randomização
          const images = [LaVieEstBellePerfume, Cerave];

          const enrichedResults = result.map((item: Product) => {
            // Escolher uma imagem aleatória
            const randomImage = images[Math.floor(Math.random() * images.length)];
            return {
              ...item,
              image: randomImage, // Atribuir a imagem aleatória ao item
            };
          });

          setProduct(enrichedResults);
        }
      } catch (error) {
        console.error("Erro ao buscar dados:", error);
      } finally {
        setLoading(false); // Finaliza o carregamento
      }
    };

    fetchData();
  }, [user.access_toke]);

  return (
    <div className="recent-searches relative">
      <h2 className="font-bold text-lg mb-4">Pesquisas Recentes</h2>

      {loading ? (
        // Exibe esqueleto enquanto está carregando
        <div className="overflow-x-auto whitespace-nowrap">
          <div className="flex gap-5">
            {[...Array(5)].map((_, index) => (
              <div
                key={index}
                className="w-60 h-72 bg-gray-200 animate-pulse rounded-lg flex flex-col space-y-4 flex-shrink-0"
              >
                <div className="h-48 bg-gray-300 rounded-t-lg"></div> {/* Imagem maior */}
                <div className="h-6 bg-gray-300 rounded w-3/4 mx-auto"></div> {/* Nome do produto */}
                <div className="h-4 bg-gray-300 rounded w-1/2 mx-auto"></div> {/* Categoria ou preço */}
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div className="overflow-x-auto whitespace-nowrap">
          <div className="flex gap-6">
            {product &&
              product.slice(0, 5).map((product) => (
                <ProductCard
                  key={product.product_code}
                  name={product.product_short_name}
                  category={product.category}
                  price={String(product.content_value * 10)}
                  image={product.image}
                  installments={String(product.stock)}
                />
              ))}
          </div>
        </div>
      )}
    </div>
  );
}

