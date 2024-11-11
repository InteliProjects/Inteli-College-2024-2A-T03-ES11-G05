import { SalespersonCard } from "@/components/topSallers";
import { NavBar } from "../../components/navBar";
import { useEffect, useState } from "react";
import { sellers_performance } from "@/api/login";
import { useUserStore } from "@/zustand/user";

interface EmployeeSales {
    store_id: string;          // ID da loja
    employee_id: number;      // ID do empregado
    employee_name: string;     // Nome do empregado
    sales_target: number;      // Meta de vendas
    total_sales: number;       // Total de vendas realizadas
}

export function TopSalesMans() {
    const [topSalers, setTopSalers] = useState<EmployeeSales[]>([]);
    const [loading, setLoading] = useState(true); // Estado de carregamento
    const user = useUserStore((state) => state.user);
    
    useEffect(() => {
        const fetchData = async () => {
            setLoading(true); // Inicia o carregamento
            try {
                const sallers = await sellers_performance(user.access_toke);
                setTopSalers(sallers);
            } catch (error) {
                console.error("Error fetching sellers:", error);
            } finally {
                setLoading(false); // Finaliza o carregamento
            }
        };

        fetchData();
    }, [user.access_toke]);

    return (
        <div className="p-5">
            <div className="">
                <NavBar userRoute="/manager" salesManRoute="/manager/ProductAndCategori" isManagerPage={true} />
            </div>

            <div className="p-5 mt-5 border-2 rounded-md">
                <div className="mb-5">
                    <h1 className="text-xl">Top Sellers</h1>
                    <h2 className="text-[#777980]">Top seller no mês</h2>
                </div>

                {loading ? (
                    // Efeito pulse enquanto está carregando
                    <div className="animate-pulse">
                        <div className="h-5 bg-gray-300 rounded w-3/4 mb-4"></div>
                        <div className="h-5 bg-gray-300 rounded w-2/4 mb-4"></div>
                        <div className="h-5 bg-gray-300 rounded w-1/4 mb-4"></div>
                    </div>
                ) : (
                    topSalers.map(item => {
                        // Defina um limite para o total de vendas que será considerado
                        const salesLimit = item.sales_target; // Alterado para 3 vezes a meta
                        const limitedSales = Math.min(item.total_sales, salesLimit);

                        // Calcule o progresso com o total de vendas limitado
                        const progress = item.sales_target > 0 
                            ? Math.min((limitedSales / item.sales_target) * 100)
                            : 0; // Evita divisão por zero

                        return (
                            <SalespersonCard 
                                key={item.employee_id} 
                                name={item.employee_name} 
                                date="08/10/2007" // Atualize conforme necessário
                                progress={progress} 
                                totalSales={item.total_sales} // Total de vendas realizadas
                                salesTarget={item.sales_target} // Meta de vendas
                            />
                        );
                    })
                )}
            </div>
        </div>
    );
}
