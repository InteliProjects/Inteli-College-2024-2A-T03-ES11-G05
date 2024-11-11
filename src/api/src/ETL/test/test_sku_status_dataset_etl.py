import pandas as pd
from ETL.sku_status_dataset import sku_status_dataset_etl  # Ajuste conforme o caminho correto para o fluxo

def test_sku_status_dataset_etl():
    # Simulando um DataFrame de SKU Status Dataset
    data = {
        'cod_prod': [101, 102, 103, 104, 101],
        'data_inicio': ['01/01/2021', '05/02/2021', None, '15/03/2021', '01/01/2021'],
        'data_fim': [None, '30/04/2021', '01/05/2021', None, None]
    }
    
    skuStatusDatasetDF = pd.DataFrame(data)

    # Executa o fluxo ETL
    cleaned_df = sku_status_dataset_etl(skuStatusDatasetDF)

    # Verifica se os tipos de dados foram convertidos corretamente
    assert pd.api.types.is_datetime64_any_dtype(cleaned_df['data_inicio']), "A coluna 'data_inicio' não foi convertida para datetime."
    
    # Verifica se todos os valores nulos em 'data_inicio' foram removidos
    assert cleaned_df['data_inicio'].notna().all(), "Ainda existem valores nulos na coluna 'data_inicio'."

    # Verifica se somente produtos ativos (com 'data_fim' nulo) foram mantidos
    assert cleaned_df.shape[0] == 2, "O número de produtos ativos filtrados está incorreto."
    assert cleaned_df['data_fim'].isna().all(), "Alguns produtos inativos ainda estão no DataFrame."

    # Verifica se a coluna 'data_fim' foi removida
    assert 'data_fim' not in cleaned_df.columns, "A coluna 'data_fim' não foi removida."

    # Verifica se as duplicatas foram removidas
    assert cleaned_df.duplicated().sum() == 0, "Ainda existem duplicatas no DataFrame."

    # Verifica se o índice foi resetado corretamente
    assert list(cleaned_df.index) == list(range(len(cleaned_df))), "O índice não foi resetado corretamente."

    # Verifica o número final de registros
    print(f"Número final de registros: {cleaned_df.shape[0]}")

