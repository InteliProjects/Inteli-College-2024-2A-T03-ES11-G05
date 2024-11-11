import pandas as pd
from ETL.sku_cost import sku_cost_etl  # Ajuste conforme o caminho correto para o fluxo

def test_sku_cost_etl():
    # Simulando um DataFrame de SKU Costs
    data = {
        'cod_prod': [123, 456, 789, None, 123],
        'custo': ['10.5', 'abc', '30.0', '20.0', '10.5'],
        'data_inicio': ['01/01/2021', '01/03/2021', '01/05/2021', '01/01/2020', '01/01/2021'],
        'data_fim': ['01/02/2021', '01/04/2021', '01/06/2021', None, '01/02/2021']
    }
    
    skuCostDF = pd.DataFrame(data)

    # Executa o fluxo ETL
    cleaned_df = sku_cost_etl(skuCostDF)

    # Verifica se valores nulos foram removidos
    assert not cleaned_df.isnull().values.any(), "Ainda existem valores nulos após o processamento."

    # Verifica se tipos de dados foram convertidos corretamente
    assert cleaned_df['cod_prod'].dtype == object, "A coluna 'cod_prod' não foi convertida corretamente para string."
    assert pd.api.types.is_numeric_dtype(cleaned_df['custo']), "A coluna 'custo' não foi convertida corretamente para numérico."
    assert pd.api.types.is_datetime64_any_dtype(cleaned_df['data_inicio']), "A coluna 'data_inicio' não foi convertida para datetime."
    assert pd.api.types.is_datetime64_any_dtype(cleaned_df['data_fim']), "A coluna 'data_fim' não foi convertida para datetime."

    # Verifica se o filtro de datas inválidas está correto (data_inicio < data_fim)
    assert all(cleaned_df['data_inicio'] < cleaned_df['data_fim']), "Existem registros com 'data_inicio' maior ou igual a 'data_fim'."

    # Verifica se as duplicatas foram removidas
    assert cleaned_df.duplicated().sum() == 0, "Existem duplicatas que não foram removidas."

    # Verifica se o índice foi resetado
    assert list(cleaned_df.index) == list(range(len(cleaned_df))), "O índice não foi resetado corretamente."

    # Verifica o número final de registros
    print(f"Número final de registros: {cleaned_df.shape[0]}")
