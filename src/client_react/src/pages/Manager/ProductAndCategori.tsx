import { CategorySales } from "@/components/cagorySales";
import { ProductItem } from "@/components/productItem";
import { Shirt } from "lucide-react";
import { NavBar } from '@/components/navBar';
import PerfumeA from "../../assets/perfumeA.png"; // Mantenha apenas se for usar
import { useEffect, useState } from "react";
import { top_category, top_product } from "@/api/login";
import { useUserStore } from "@/zustand/user";

interface ProductSales {
    store_id: string;                 
    product_name: string;             
    year: number;                     
    month: number;                    
    total_sales: number;              
}

interface SalesData {
    store_id: string;           // ID da loja
    product_category: string;   // Categoria do produto
    year: number;               // Ano da venda
    month: number;              // Mês da venda
    total_sales: number;        // Total de vendas
}

// Função para calcular as porcentagens de vendas
const calculatePercentageChanges = (data: SalesData[]) => {
    // Objeto para armazenar os totais de vendas por categoria para cada mês
    const percentageChanges: { [key: string]: { current: number; previous: number } } = {};

    data.forEach(item => {
        const { product_category, month, total_sales } = item;

        // Armazena as vendas para o mês atual (outubro - mês 10)
        if (month === 10) {
            if (!percentageChanges[product_category]) {
                percentageChanges[product_category] = { current: 0, previous: 0 };
            }
            percentageChanges[product_category].current += total_sales; // Soma as vendas de outubro
        }

        // Armazena as vendas para o mês anterior (setembro - mês 9)
        if (month === 9) {
            if (!percentageChanges[product_category]) {
                percentageChanges[product_category] = { current: 0, previous: 0 };
            }
            percentageChanges[product_category].previous += total_sales; // Soma as vendas de setembro
        }
    });

    // Calcula a variação percentual
    return Object.entries(percentageChanges).map(([category, sales]) => {
        const { current, previous } = sales;
        const percentageChange = previous ? ((current - previous) / previous) * 100 : 0; // Previne divisão por zero
        return {
            product_category: category,
            current_sales: current,
            previous_sales: previous,
            percentage_change: percentageChange.toFixed(2) + "%", // Formata a porcentagem
        };
    });
};

// Exemplo do uso dessa função dentro do componente
export function ProductAndCategori() {
    const [product, setProduct] = useState<ProductSales[]>([]);
    const [categories, setCategories] = useState<SalesData[]>([]);
    const [loading, setLoading] = useState(true);
    const user = useUserStore((store) => store.user);

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            try {
                const [resultCategories, resultProduct] = await Promise.all([
                    top_category(user.access_toke),
                    top_product(user.access_toke)
                ]);
                setCategories(resultCategories);
                setProduct(resultProduct);
            } catch (error) {
                console.error("Error fetching data:", error);
            } finally {
                setLoading(false);
            }
        };
    
        fetchData();
    }, [user.access_toke]);

    const percentageData = calculatePercentageChanges(categories);

    return (
        <div className="p-5">
            <div className="max-w-lg mx-auto">
                <NavBar userRoute="/manager" salesManRoute="/manager/ProductAndCategori" isManagerPage={true} />
            </div>

            {/* Seção de categorias */}
            <div className="p-5 mt-5 border-2 rounded-md">
                <div>
                    <h1 className="text-xl">Top Categorias</h1>
                    <h2 className="text-[#777980]">Categorias mais vendidas comparado ao último mês</h2>
                </div>

                <div className="mt-5 max-h-64 overflow-y-auto">
                    {loading ? (
                        <div className="animate-pulse">
                            <div className="h-5 bg-gray-300 rounded w-3/4 mb-4"></div>
                            <div className="h-5 bg-gray-300 rounded w-2/4 mb-4"></div>
                            <div className="h-5 bg-gray-300 rounded w-1/4 mb-4"></div>
                        </div>
                    ) : (
                        percentageData.map(({ product_category, current_sales, previous_sales, percentage_change }) => (
                            <CategorySales
                                key={product_category}
                                icon={<Shirt />}
                                name={product_category}
                                sales={current_sales.toLocaleString("pt-BR", { maximumFractionDigits: 0 })}
                                amount={previous_sales.toLocaleString("pt-BR", { maximumFractionDigits: 0 })}
                                percentageChange={percentage_change}
                            />
                        ))
                    )}
                </div>
            </div>

            {/* Seção de produtos */}
            <div className="p-5 mt-5 border-2 rounded-md">
                <div>
                    <h1 className="text-xl">Top Produtos</h1>
                    <h2 className="text-[#777980]">Melhores produtos em um período de tempo</h2>
                </div>

                <div className="mt-5 max-h-64 overflow-y-auto">
                    {loading ? (
                        <div className="animate-pulse">
                            <div className="h-5 bg-gray-300 rounded w-3/4 mb-4"></div>
                            <div className="h-5 bg-gray-300 rounded w-2/4 mb-4"></div>
                            <div className="h-5 bg-gray-300 rounded w-1/4 mb-4"></div>
                        </div>
                    ) : (
                        product.map((item) => (
                            <ProductItem
                                key={`${item.store_id}-${item.product_name}-${item.month}-${item.year}`}
                                imageSrc={PerfumeA}
                                name={item.product_name}
                                category="Perfume"
                                price={`R$ ${item.total_sales.toLocaleString("pt-BR",{ maximumFractionDigits: 0 })}`}
                            />
                        ))
                    )}
                </div>
            </div>
        </div>
    );
}