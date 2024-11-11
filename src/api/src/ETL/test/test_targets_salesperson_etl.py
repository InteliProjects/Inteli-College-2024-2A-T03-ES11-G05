import pandas as pd
from ETL.target_salesperson import targets_salesperson_etl  # Ajuste conforme o caminho correto

def test_targets_salesperson_etl():
    # Simulando um DataFrame de metas de vendas
    data = {
        'id_employee': [1, 2, 3, 4, 5],
        'month': ['01/2023', '02/2023', '03/2023', '04/2023', '05/2023'],
        'sales_target': ['1000', '1500', '2000', '2500', '3000']
    }
    
    target_salespersonDF = pd.DataFrame(data)
    
    # Executa o fluxo ETL
    processed_df = targets_salesperson_etl(target_salespersonDF)
    
    # Verifica se a coluna 'month' foi convertida corretamente para o formato datetime
    assert pd.api.types.is_datetime64_any_dtype(processed_df['month']), "A coluna 'month' não foi convertida para datetime."
    
    # Verifica se as colunas 'id_employee' e 'sales_target' foram convertidas corretamente para o tipo int
    assert pd.api.types.is_integer_dtype(processed_df['id_employee']), "A coluna 'id_employee' não foi convertida para int."
    assert pd.api.types.is_integer_dtype(processed_df['sales_target']), "A coluna 'sales_target' não foi convertida para int."
    
    # Verifica se o DataFrame resultante tem o mesmo número de linhas do original
    assert processed_df.shape[0] == target_salespersonDF.shape[0], "O número de registros no DataFrame processado está incorreto."
    
    # Verifica o número final de registros e exibe uma mensagem de sucesso
    print(f"Número final de registros: {processed_df.shape[0]}")

