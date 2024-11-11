import { Heart } from "lucide-react";
import { useProductStore } from "@/zustand/produts";
import { useState, useEffect } from "react";

export function PopularProducts() {
  const [loading, setLoading] = useState<boolean>(true); // Estado de carregamento
  const product = useProductStore(state => state.product);

  // Simulando o tempo de carregamento
  useEffect(() => {
    // Simular um tempo de carregamento (apenas como exemplo)
    const timer = setTimeout(() => {
      setLoading(false); // Finaliza o carregamento após um tempo
    }, 2000); // Defina o tempo desejado aqui

    return () => clearTimeout(timer); // Limpar o timer quando o componente desmontar
  }, []);

  return (
    <div className="popular-products mt-8">
      <h2 className="font-bold text-lg mb-4">Produtos populares</h2>

      {loading ? (
        // Esqueleto de carregamento
        <div>
          {[...Array(5)].map((_, index) => (
            <div key={index} className="border-b pb-4 mb-4 animate-pulse">
              <div className="flex items-center gap-4">
                <div className="w-16 h-16 bg-gray-300 rounded-full"></div> {/* Placeholder da imagem */}
                <div className="flex-1 space-y-2">
                  <div className="h-4 bg-gray-300 rounded w-3/4"></div> {/* Placeholder do nome */}
                  <div className="h-3 bg-gray-300 rounded w-1/2"></div> {/* Placeholder da categoria */}
                  <div className="h-4 bg-gray-300 rounded w-1/4"></div> {/* Placeholder do valor */}
                  <div className="h-3 bg-gray-300 rounded w-1/3"></div> {/* Placeholder da comissão */}
                </div>
                <div className="w-6 h-6 bg-gray-300 rounded-full"></div> {/* Placeholder do ícone de coração */}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div>
          {product && product.map((item) => (
            <div key={item.product_code} className="border-b pb-4 mb-4">
              <div className="flex items-center gap-4">
                <img
                  src={item.image}
                  alt={item.product_short_name}
                  className="w-16 h-16 object-contain"
                />
                <div>
                  <h3 className="font-semibold text-md">{item.product_short_name}</h3>
                  <p className="text-sm text-gray-500">{item.category}</p>
                  <p className="font-bold">R$ {item.content_value * 10}</p>
                  <p className="text-sm text-gray-500 bg-gray-200 rounded-full px-2 py-1 inline-block">
                    Comissão de R$ {((item.content_value * 10) * 0.1).toLocaleString("pt-BR")}
                  </p>
                </div>
                <Heart className="ml-auto text-red-500" />
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
