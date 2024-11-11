export function CategorySales({ icon, name, sales, amount, percentageChange }) {
  // Converter percentageChange para número se necessário
  const percentageValue = parseFloat(percentageChange);
  
  const isPositive = percentageValue > 0;
  const isNegative = percentageValue < 0;

  return (
    <div className="flex items-center justify-between py-3 border-b last:border-b-0">
      {/* Ícone e informações de vendas */}
      <div className="flex items-center w-1/2">
        <div className="w-12 h-12 flex items-center justify-center bg-gray-100 rounded-full">
          {icon}
        </div>
        <div className="flex flex-col">
          <h2 className="text-sm font-medium truncate w-20">{name}</h2> {/* Ajuste de largura para evitar corte */}
          <p className="text-xs text-gray-500">{sales} Vendas</p>
        </div>
      </div>

      {/* Informações de valor e mudança percentual */}
      <div className="flex items-center w-1/2 justify-end">
        <span className="text-sm font-semibold ">R$ {amount}</span>
        <span
          className={`text-xs font-semibold rounded-full py-2 px-1  ml-2 ${
            isPositive
              ? 'bg-green-100 text-green-600'
              : isNegative
              ? 'bg-red-100 text-red-600'
              : 'bg-gray-100 text-gray-600' // Para o caso de ser 0
          }`}
        >
          {isPositive ? `+${percentageValue.toFixed(2)}%` : 
           isNegative ? `${percentageValue.toFixed(2)}%` : '0.00%'}
        </span>
      </div>
    </div>
  );
}
