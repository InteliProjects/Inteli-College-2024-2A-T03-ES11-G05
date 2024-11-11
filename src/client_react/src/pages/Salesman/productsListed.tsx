import { useState } from "react";
import { ProductCard } from "../../components/productCard";
import LaVieEstBellePerfume from '../../assets/produtos/LaVieEstBellePerfum.png';
import {
  Drawer,
  DrawerClose,
  DrawerContent,
  DrawerDescription,
  DrawerFooter,
  DrawerHeader,
  DrawerTitle,
} from "@/components/ui/drawer";
import { Button } from "@/components/ui/button";
import { Product, useProductStore } from "@/zustand/produts";
import { salesMan_recomendation } from "@/api/login";
import { useUserStore } from "@/zustand/user";

interface RecommendedProduct {
  product_id: number;
  name: string;
  category: string;
  price: number;
  stock: number;
}

export function ProductsListed() {
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [recommendations, setRecommendations] = useState<RecommendedProduct[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const user = useUserStore(state => state.user);
  const product = useProductStore(state => state.product);

  const handleCardClick = async (product: Product) => {
    setSelectedProduct(product);
    await handleRecomendationProject(String(product.product_code));
  };

  const handleCloseRelatedProducts = () => {
    setSelectedProduct(null);
    setRecommendations([]); // Limpa as recomendações ao fechar
    setIsLoading(false); // Reseta o estado de loading
  };

  const handleRecomendationProject = async (product_id: string) => {
    setIsLoading(true); // Inicia o estado de loading
    try {
      const recomendations = await salesMan_recomendation(user.access_toke, product_id);

      if (recomendations && recomendations.length > 0) {
        const separatedRecommendations = recomendations.map((rec: any) => {
          const recommendedProduct1: RecommendedProduct = {
            product_id: rec.recommended_product_1_id,
            name: rec.recommended_product_1_name,
            category: rec.recommended_product_1_category,
            price: rec.recommended_product_1_price,
            stock: rec.recommended_product_1_stock,
          };

          const recommendedProduct2: RecommendedProduct = {
            product_id: rec.recommended_product_2_id,
            name: rec.recommended_product_2_name,
            category: rec.recommended_product_2_category,
            price: rec.recommended_product_2_price,
            stock: rec.recommended_product_2_stock,
          };

          return [recommendedProduct1, recommendedProduct2];
        });

        const flattenedRecommendations = separatedRecommendations.flat();
        setRecommendations(flattenedRecommendations);
      }
    } catch (error) {
      console.error("Erro ao buscar recomendações:", error);
    } finally {
      setIsLoading(false); // Finaliza o estado de loading
    }
  };

  return (
    <div className="max-w-full mx-auto p-4 relative">
      {/* Lista de produtos principais */}
      <div className={`grid grid-cols-2 gap-6`}>
        {product.map((item) => (
          <div key={item.product_code} className="relative">
            <div
              className={`relative ${selectedProduct && selectedProduct.product_code !== item.product_code ? "blur-lg" : ""}`}
              onClick={() => handleCardClick(item)}
            >
              <ProductCard
                name={item.product_short_name}
                category={item.category}
                price={String(item.content_value * 10)}
                image={item.image}
                installments={((item.content_value * 10) * 0.1).toLocaleString("pt-BR")}
              />
            </div>
          </div>
        ))}
      </div>

      {/* Drawer para produtos recomendados */}
      {selectedProduct && (
        <Drawer open={Boolean(selectedProduct)} onOpenChange={handleCloseRelatedProducts}>
          <DrawerContent>
            <DrawerHeader>
              <DrawerTitle>Produtos Recomendados</DrawerTitle>
              <DrawerDescription>Veja os produtos recomendados para {selectedProduct.product_short_name}</DrawerDescription>
            </DrawerHeader>
            <div className="grid grid-cols-2 gap-4 p-4">
              {isLoading ? (
                // Componente de loading com animação pulse
                <>
                  <div className="animate-pulse bg-gray-300 h-40 w-full rounded-lg"></div>
                  <div className="animate-pulse bg-gray-300 h-40 w-full rounded-lg"></div>
                </>
              ) : (
                // Mostrar as recomendações após o carregamento
                recommendations.map((recommendedProduct) => (
                  <ProductCard
                    key={recommendedProduct.product_id}
                    name={recommendedProduct.name}
                    category={recommendedProduct.category}
                    price={String(recommendedProduct.price)}
                    image={LaVieEstBellePerfume} // Use a imagem correta aqui
                    installments={`${recommendedProduct.stock}`}
                  />
                ))
              )}
            </div>
            <DrawerFooter>
              <DrawerClose>
                <Button variant="outline" onClick={handleCloseRelatedProducts}>Fechar</Button>
              </DrawerClose>
            </DrawerFooter>
          </DrawerContent>
        </Drawer>
      )}
    </div>
  );
}
