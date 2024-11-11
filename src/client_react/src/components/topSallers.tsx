interface SalespersonCardProps {
  name: string;
  date: string;
  progress: number; // De 0 a 100
  avatar?: string; // Caminho para a imagem do avatar (opcional)
  totalSales: number; // Total de vendas realizadas
  salesTarget: number; // Meta de vendas
}

export function SalespersonCard({ name, date, progress, avatar, totalSales, salesTarget }: SalespersonCardProps) {
  return (
    <div className="flex items-center p-4 bg-white rounded-lg shadow-md mb-5">
      {/* Avatar do vendedor */}
      <div className="w-12 h-12 rounded-full bg-purple-100 flex items-center justify-center">
        {avatar ? (
          <img src={avatar} alt={name} className="w-full h-full rounded-full" />
        ) : (
          <span className="text-xl text-purple-500">👤</span> // Ícone de fallback se não houver avatar
        )}
      </div>

      {/* Detalhes do vendedor */}
      <div className="ml-4 flex-1">
        <h3 className="text-lg font-semibold">{name}</h3>
        <p className="text-sm text-gray-500">Vendedor(a) desde {date}</p>

        {/* Informações de vendas */}
        <p className="text-sm font-bold  text-gray-700 mt-5">
          Total vendido: 
        </p>

        <p className="text-sm">R${totalSales.toLocaleString("pt-BR",{maximumFractionDigits:0})}</p>

        <p className="text-sm font-bold  text-gray-700 mt-5">
          Meta: 
        </p>

        <p className="text-sm">R${salesTarget.toLocaleString("pt-BR")}</p>

        {/* Barra de progresso */}
        <div className="mt-2 h-4 w-full bg-gray-200 rounded-full overflow-hidden border border-gray-300 shadow-sm">
          <div
            className="h-full rounded-full bg-gradient-to-r from-green-400 to-teal-500"
            style={{ width: `${progress}%` }}
          ></div>
        </div>
      </div>
    </div>
  );
}