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
        df['preco'] = pd.to_numeric(df['preco'], errors='coerce')  # Converte preço para numérico, marcando erros como NaN
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

@flow(name="SKU Price ETL")
def sku_price_etl(skuPriceDF):
    # Copia o DataFrame original para evitar modificações não intencionais
    sku_price = skuPriceDF.copy()

    # Passo 1: Verifica e remove valores nulos
    sku_price = check_and_remove_nulls(sku_price)

    # Passo 2: Converte tipos de dados
    sku_price = convert_data_types(sku_price)

    # Passo 3: Remove novamente valores nulos que podem ter sido gerados pelas conversões
    sku_price = check_and_remove_nulls(sku_price)

    # Passo 4: Filtra registros com datas inválidas
    sku_price = filter_invalid_date_ranges(sku_price)

    # Passo 5: Remove duplicatas
    sku_price = remove_duplicates(sku_price)

    # Passo 6: Reseta o índice
    sku_price = reset_index(sku_price)

    # Log de informações sobre o DataFrame resultante
    print(f"Dados processados: {sku_price.shape[0]} registros após limpeza.")
    print(sku_price.head())  # Exibe as primeiras linhas para verificação

    return sku_price