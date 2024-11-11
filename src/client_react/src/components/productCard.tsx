import { Heart } from "lucide-react";

interface ProductCardProps {
  name: string;
  category: string;
  price: string;
  image: string;
  installments: string;
}

export function ProductCard({
  name,
  category,
  price,
  image,
  installments,
}: ProductCardProps) {
    
    return (
        <div className="border rounded-lg p-4 relative flex flex-col justify-between h-60 w-42 -z-0">
          <img src={image} alt={name} className="w-full h-20 object-contain mb-2" />
          <div className="absolute top-2 right-2">
            <Heart className="text-red-500" />
          </div>
          <div className="flex flex-col justify-between flex-grow z-0">
            <h3 className="font-semibold text-md mb-1 truncate">{name}</h3>
            <p className="text-sm text-gray-500 mb-1 z-0">{category}</p>
            <p className="font-bold mb-1">R$ {Number(price).toLocaleString("pt-BR")}</p>
            {installments && (
              <p className="font-regular text-sm">Estoque: {installments} produtos</p>
            )}
          </div>
        </div>
      );
}
