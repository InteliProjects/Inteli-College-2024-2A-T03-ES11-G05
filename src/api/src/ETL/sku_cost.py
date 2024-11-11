import pandas as pd
from prefect import task,flow

@task
def check_and_remove_nulls(df):
    if df.isnull().values.any():
        print("Aviso: Encontrado valores nulos. Removendo linhas com valores nulos...")
        df.dropna(inplace=True)
    return df

@task
def convert_data_types(df):
    try:
        df['cod_prod'] = df['cod_prod'].astype(str)  # Converte o código do produto para string
        df['custo'] = pd.to_numeric(df['custo'], errors='coerce')  # Converte custo para numérico, marcando erros como NaN
        df['data_inicio'] = pd.to_datetime(df['data_inicio'], errors='coerce')  # Converte as datas
        df['data_fim'] = pd.to_datetime(df['data_fim'], errors='coerce')
    except Exception as e:
        print(f"Erro na conversão de tipos de dados: {e}")
    return df

@task
def filter_invalid_date_ranges(df):
    df = df[df['data_inicio'] < df['data_fim']]
    return df

@task
def remove_duplicates(df):
    df.drop_duplicates(inplace=True)
    return df

@task
def reset_index(df):
    df.reset_index(drop=True, inplace=True)
    return df

@flow(name="SKU Cost ETL")
def sku_cost_etl(skuCostDF):
    # Copia o DataFrame original para evitar modificações não intencionais
    sku_cost = skuCostDF.copy()

    # Passo 1: Verifica e remove valores nulos
    sku_cost = check_and_remove_nulls(sku_cost)

    # Passo 2: Converte tipos de dados
    sku_cost = convert_data_types(sku_cost)

    # Passo 3: Remove novamente valores nulos que podem ter sido gerados pelas conversões
    sku_cost = check_and_remove_nulls(sku_cost)

    # Passo 4: Filtra registros com datas inválidas
    sku_cost = filter_invalid_date_ranges(sku_cost)

    # Passo 5: Remove duplicatas
    sku_cost = remove_duplicates(sku_cost)

    # Passo 6: Reseta o índice
    sku_cost = reset_index(sku_cost)

    # Log de informações sobre o DataFrame resultante
    print(f"Dados processados: {sku_cost.shape[0]} registros após limpeza.")
    print(sku_cost.head())  # Exibe as primeiras linhas para verificação

    return sku_cost
