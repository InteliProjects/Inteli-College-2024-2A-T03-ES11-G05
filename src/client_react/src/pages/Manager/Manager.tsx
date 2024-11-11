import green_kart from "../../assets/green-kart.png";
import arrow_green from "../../assets/fi-rr-caret-up.png";
import arrow_red from "../../assets/fi-rr-caret-down.png"
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Bar, CartesianGrid, Line, LineChart, XAxis, BarChart, LabelList } from "recharts";
import { NavBar } from '@/components/navBar';
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart";
import { useEffect, useState } from "react";
import { performance_by_store_six, sales_month } from "@/api/login";
import { useUserStore } from "@/zustand/user";

// Função para mapear o número do mês para o nome do mês
const getMonthName = (month: number) => {
  const months = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
  return months[month];
}

const chartConfig = {
  desktop: {
    label: "Vendas Totais",
    color: "#2563eb",
  },
} satisfies ChartConfig;

interface IsalesMonth {
  sales_target: number;
  period: "previous_month" | "current_month";
}

interface IPerformanceStore {
  month: number;
  total_sales: number;
}

export function Manager() {
  const [salesMonth, setSalesMonth] = useState<IsalesMonth[]>([]);
  const [performance, setPerformance] = useState<IPerformanceStore[]>([]);
  const [loading, setLoading] = useState(true); // Estado de carregamento
  const user = useUserStore((state) => state.user);

  const salesDifference =
    salesMonth.length > 1
      ? salesMonth[1].sales_target - salesMonth[0].sales_target
      : 0;
  const percentageDifference =
    salesMonth.length > 1
      ? (salesDifference / salesMonth[0].sales_target) * 100
      : 0;

  const totalSales = performance.reduce((acc, item) => acc + item.total_sales, 0);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Começa o carregamento
        setLoading(true);

        // Faz as requisições
        const salesMonthResult = await sales_month(user.access_toke);
        const performanceResult = await performance_by_store_six(user.access_toke);

        setSalesMonth(salesMonthResult);
        setPerformance(performanceResult);
      } catch (error) {
        console.error("Erro ao buscar dados:", error);
      } finally {
        // Finaliza o carregamento
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const chartData = performance
    .sort((a, b) => a.month - b.month) // Ordena os meses de forma crescente
    .map((item) => ({
      month: getMonthName(item.month), // Mapeia corretamente o número do mês
      total_sales: (item.total_sales / 1000).toFixed(1), // Formata o valor para milhares
    }));

  return (
    <div className="p-5">
      <div className="max-w-lg mx-auto">
        <NavBar
          userRoute="/manager"
          salesManRoute="/manager/ProductAndCategori"
          isManagerPage={true}
        />
      </div>

      {/* Card */}
      <div className="border-2 border-[#E0E2E7] rounded-lg mt-10 p-5">
        {loading ? (
          <div className="flex justify-center items-center">
            {/* Placeholder de carregamento */}
            <div className="animate-pulse w-full">
              <div className="h-4 bg-gray-300 rounded w-1/4 mb-4"></div>
              <div className="h-8 bg-gray-300 rounded w-1/2 mb-4"></div>
              <div className="flex items-center">
                <div className="h-3 bg-gray-300 rounded w-1/6"></div>
                <div className="ml-4 h-3 bg-gray-300 rounded w-1/12"></div>
                <div className="ml-4 h-3 bg-gray-300 rounded w-1/3"></div>
              </div>
            </div>
          </div>
        ) : (
          <>
            <div className="flex">
              <div>
                <img src={green_kart} alt="green_kart_icon" />
              </div>
              <p className="text-[#777980] mb-2">Meta de Vendas</p>
            </div>
            <h2 className="text-3xl font-semibold ml-1">
              {salesMonth.length > 0 ? salesMonth[0].sales_target.toLocaleString("pt-BR",{ style: 'currency', currency: 'BRL', minimumFractionDigits: 0 }) : 0}
            </h2>

            <div className="flex text-center items-center text-sm mt-4 ml-1">
              <p
                className={`font-bold ${
                  percentageDifference > 0 ? "text-[#1A9882]" : "text-red-500"
                }`}
              >
                {percentageDifference.toLocaleString("pt-BR")}%
              </p>
              <div>
                {percentageDifference > 0 ? <img src={arrow_green} alt="green_kart_icon" /> : <img src={arrow_red} alt="green_kart_icon" />}
              </div>
              <p className="text-[#858D9D]">
                {salesDifference > 0
                  ? `+ ${salesDifference.toLocaleString("pt-BR",{ style: 'currency', currency: 'BRL', minimumFractionDigits: 0 })} vendas do que mês passado`
                  : `- ${Math.abs(salesDifference).toLocaleString("pt-BR",{ style: 'currency', currency: 'BRL', minimumFractionDigits: 0 })} vendas do que mês passado`}
              </p>
            </div>
          </>
        )}
      </div>

      <div className="flex justify-center">
        <Tabs className="mt-10 mb-10" defaultValue="12_Months">
          <TabsList>
            <TabsTrigger value="12_Months">12 Meses</TabsTrigger>
            <TabsTrigger value="30_Days">30 Dias</TabsTrigger>
            <TabsTrigger value="7_Days">7 Dias</TabsTrigger>
            <TabsTrigger value="24_Hours">24 Horas</TabsTrigger>
          </TabsList>
        </Tabs>
      </div>

      <div>
        <Card>
          <CardHeader>
            <CardTitle>Desempenho da Filial - MG_21</CardTitle>
            <CardDescription>Abril - Julho 2024</CardDescription>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="flex justify-center items-center animate-pulse">
                {/* Placeholder para o gráfico */}
                <div className="h-48 bg-gray-300 rounded w-full"></div>
              </div>
            ) : (
              <ChartContainer config={chartConfig}>
                <LineChart
                  accessibilityLayer
                  data={chartData}
                  margin={{
                    left: 12,
                    right: 12,
                  }}
                >
                  <CartesianGrid vertical={false} />
                  <XAxis
                    dataKey="month"
                    tickLine={false}
                    axisLine={false}
                    tickMargin={8}
                    tickFormatter={(value) => value.slice(0, 3)}
                  />
                  <ChartTooltip cursor={false} content={<ChartTooltipContent />} />
                  <Line
                    dataKey="total_sales"
                    type="monotone"
                    stroke="var(--color-desktop)"
                    strokeWidth={2}
                    dot={false}
                  />
                </LineChart>
              </ChartContainer>
            )}
          </CardContent>
          {!loading && (
            <CardFooter className="w-full mt-5">
              <div className="flex flex-col w-full">
                <div className="flex">
                  <h2 className="text-xl">Total de Vendas:</h2>
                  <h2 className="ml-auto text-xl text-[#94C3F6]">{(totalSales).toLocaleString("pt-BR",{ style: 'currency', currency: 'BRL', maximumFractionDigits: 0 })}</h2>
                </div>
              </div>
            </CardFooter>
          )}
        </Card>
      </div>

      <div className="mt-10">
        <Card>
          <CardHeader>
            <CardTitle>Desempenho Mensal</CardTitle>
            <CardDescription>Janeiro - Junho 2024</CardDescription>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="flex justify-center items-center animate-pulse">
                {/* Placeholder para o gráfico */}
                <div className="h-48 bg-gray-300 rounded w-full"></div>
              </div>
            ) : (
              <ChartContainer config={chartConfig}>
                <BarChart accessibilityLayer data={chartData}>
                  <defs>
                    <linearGradient id="colorGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#50C474" />
                      <stop offset="100%" stopColor="#128E38" />
                    </linearGradient>
                  </defs>
                  <CartesianGrid vertical={false} />
                  <XAxis
                    dataKey="month"
                    tickLine={false}
                    axisLine={false}
                    tickMargin={8}
                    tickFormatter={(value) => (value.slice(0, 3))}
                  />
                  <ChartTooltip
                    cursor={false}
                    content={<ChartTooltipContent hideLabel />}
                  />
                  <Bar dataKey="total_sales" fill="url(#colorGradient)" radius={8}>
                    <LabelList
                      dataKey="total_sales"
                      position="top"
                      offset={12}
                      className="fill-foreground"
                      fontSize={12}
                    />
                  </Bar>
                </BarChart>
              </ChartContainer>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
