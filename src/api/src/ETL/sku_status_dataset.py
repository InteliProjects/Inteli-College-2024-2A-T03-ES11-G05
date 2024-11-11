import pandas as pd
from prefect import task,flow

@task
def convert_data_types(df):
    try:
        df['cod_prod'] = df['cod_prod'].astype(str)  # Converte código do produto para string
        df['data_inicio'] = pd.to_datetime(df['data_inicio'], errors='coerce')  # Converte data_inicio para datetime
        df['data_fim'] = pd.to_datetime(df['data_fim'], errors='coerce')  # Converte data_fim para datetime
    except Exception as e:
        print(f"Erro na conversão de tipos de dados: {e}")
    return df

@task
def remove_null_values(df):
    df.dropna(subset=['data_inicio'], inplace=True)
    return df

@task
def filter_active_products(df):
    return df[df['data_fim'].isna()]

@task
def remove_unnecessary_column(df):
    return df.drop('data_fim', axis=1)

@task
def remove_duplicates(df):
    df.drop_duplicates(inplace=True)
    return df

@task
def reset_index(df):
    df.reset_index(drop=True, inplace=True)
    return df

@flow(name="SKU Status Dataset ETL")
def sku_status_dataset_etl(skuStatusDatasetDF):
    # Cria uma cópia do DataFrame para evitar alterações no original
    sku_status_dataset = skuStatusDatasetDF.copy()

    # Passo 1: Converte os tipos de dados
    sku_status_dataset = convert_data_types(sku_status_dataset)

    # Passo 2: Remove valores nulos
    sku_status_dataset = remove_null_values(sku_status_dataset)

    # Passo 3: Seleciona produtos ativos
    sku_status_ativos = filter_active_products(sku_status_dataset)

    # Passo 4: Remove a coluna 'data_fim'
    sku_ativos = remove_unnecessary_column(sku_status_ativos)

    # Passo 5: Remove duplicatas
    sku_ativos = remove_duplicates(sku_ativos)

    # Passo 6: Reseta o índice
    sku_ativos = reset_index(sku_ativos)

    # Log de informações sobre o DataFrame resultante
    print(f"Dados processados: {sku_ativos.shape[0]} registros de produtos ativos.")
    print(sku_ativos.head())  # Exibe as primeiras linhas para verificação

    return sku_ativos
