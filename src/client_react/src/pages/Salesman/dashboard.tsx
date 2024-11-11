import { useEffect, useState } from "react";
import { MoreVertical, X } from "lucide-react";
import green_kart from "../../assets/green-kart.png";
import money_icon from "../../assets/fi-sr-money.svg";
import { NavBar } from '@/components/navBar';
import { salesMan_target, sellers_performance } from "@/api/login";
import { useUserStore } from "@/zustand/user";

interface Target {
  id_employee: number;
  name: string;
  surname: string;
  store_id: string;
  year: number;
  month: number;
  sales_target: number;
}

interface Sellers {
  employee_id: number;
  employee_name: string;
  store_id: string;
  sales_target: number;
  total_sales: number;
}

export function Dashboard() {
  const [showDetails, setShowDetails] = useState(false);
  const [loading, setLoading] = useState<boolean>(false);
  const [data, setData] = useState<Target[]>([]);
  const [vendasAtuais, setVendasAtuais] = useState(0);
  const user = useUserStore(state => state.user);

  const toggleDetails = () => {
    setShowDetails(!showDetails);
  };

  const diasRestantes = 21;

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true); // Início do carregamento

        // Faz a requisição apenas se o token existir
        if (user.access_toke) {
          const salesTarget: Target[] = await salesMan_target(user.access_toke);
          const sellersPerformance: Sellers[] = await sellers_performance(user.access_toke);
          setData(salesTarget);
          
          const filter = sellersPerformance.filter((item) => item.employee_id === salesTarget[0].id_employee);
          setVendasAtuais(filter[0].total_sales);
        }
      } catch (error) {
        console.error("Erro ao buscar dados:", error);
      } finally {
        setLoading(false); // Finaliza o carregamento
      }
    };

    fetchData();
  }, [user.access_toke]); // Dependência adicionada


  const metaMensal = data[0]?.sales_target || 0;
  const progressoMeta = (vendasAtuais / metaMensal) * 100;
  const metaRestanteDiaria = (metaMensal - Math.round(vendasAtuais)) / diasRestantes;

  return (
    
    <div className="max-w-lg mx-auto p-6 space-y-6">
      <div className="max-w-lg mx-auto">
        <NavBar userRoute="/dash" salesManRoute="/salesMan" isManagerPage={false} />
      </div>

      {loading ? ( <div className="max-w-lg mx-auto p-6 space-y-6">
        <div className="animate-pulse space-y-4">
          <div className="h-12 bg-gray-300 rounded-lg"></div>
          <div className="h-24 bg-gray-300 rounded-lg"></div>
          <div className="h-12 bg-gray-300 rounded-lg"></div>
          <div className="h-24 bg-gray-300 rounded-lg"></div>
          <div className="h-12 bg-gray-300 rounded-lg"></div>
        </div>
      </div>) : ( <div className="space-y-4">
        
        {/* Barra de Progresso da Meta */}
        <div className="border rounded-lg p-4">
          <h2 className="text-xl text-gray-700 font-semibold mb-2">Progresso da Meta</h2>
          <div className="w-full bg-gray-200 rounded-full h-2.5">
            <div
              className="bg-green-500 h-2.5 rounded-full"
              style={{ width: `${progressoMeta}%` }}
            ></div>
          </div>
          <p className="mt-2">Você atingiu {progressoMeta.toFixed(2)}% da meta mensal.</p>
        </div>

        {/* Total de Ganhos */}
        <div className="border rounded-lg p-4">
          <div className="flex justify-between">
            <div className="flex justify-between space-x-2">
              <img src={money_icon} alt="blue_money_icon" />
              <p className="text-[#777980]"> Total de Ganhos</p>
            </div>
            <button onClick={toggleDetails}>
              <MoreVertical className="text-gray-500" />
            </button>
          </div>
          <h2 className="text-3xl font-semibold ml-1">R$ {(vendasAtuais * 0.05).toLocaleString("pt-BR")}</h2>
        </div>

        {/* Card Comissão */}
        {showDetails && (
          <div className="border inset-1 flex items-center justify-center z-10">
            <div className="bg-white p-6 rounded-lg shadow-xl w-11/20 max-w-md">
              <div className="flex justify-between items-center mb-4">
                <p className="text-sm text-gray-600">Cálculo da sua comissão</p>
                <button onClick={toggleDetails}>
                  <X className="text-gray-500" />
                </button>
              </div>
              <p className="text-xs text-gray-500 mb-4">
                5% de comissão das vendas mensais + 50% da comissão se a meta for atingida + R$ 100 para 10 produtos vendidos com a maior margem*
              </p>
              <p className="text-sm text-green-600">
                10% <span className="text-gray-500">⬆</span> + 15 vendas
              </p>
            </div>
          </div>
        )}

        {/* Meta diária */}
        <div className="border rounded-lg p-4">
          <h2 className="text-xl font-semibold mb-2">Meta Diária</h2>
          <p>
            Você precisa vender <strong>R${metaRestanteDiaria.toFixed(2)}</strong> por dia para atingir sua meta mensal.
          </p>
        </div>

        {/* Estatísticas de Vendas */}
        <div className="border rounded-lg p-4">
          <p className="text-sm text-gray-500">Vendas atuais</p>
          <h2 className="text-2xl font-bold">
            R${vendasAtuais.toLocaleString('pt-BR', { maximumFractionDigits: 0 })}
          </h2>
          <p className="text-xs text-green-600">Progresso até agora</p>
        </div>

        {/* Meta mensal */}
        <div className="border rounded-lg p-4">
          <div className="border-[#E0E2E7] rounded-lg">
            <div className="flex justify-between">
              <div className="flex justify-between space-x-2">
                <img src={green_kart} alt="green_kart_icon" />
                <p className="text-[#777980]"> Meta do Mês</p>
              </div>
            </div>
            <h2 className="text-2xl font-bold">
              R${data[0]?.sales_target?.toLocaleString('pt-BR')}
            </h2>
          </div>
        </div>
      </div>)}
     
    </div>
  );
}
