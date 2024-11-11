import pandas as pd
from prefect import task,flow

@task
def convert_month_to_datetime(df):
    df['month'] = pd.to_datetime(df['month'], format='%m/%Y')
    return df

@task
def ensure_numeric_types(df):
    df['id_employee'] = df['id_employee'].astype(int)
    df['sales_target'] = df['sales_target'].astype(int)
    return df

@flow(name="Target Salesperson ETL")
def targets_salesperson_etl(target_salespersonDF):
    # Cria uma cópia do DataFrame para evitar modificar o original
    target_salesperson = target_salespersonDF.copy()
    
    # Passo 1: Converte a coluna 'month' para o formato datetime
    target_salesperson = convert_month_to_datetime(target_salesperson)
    
    # Passo 2: Garante que 'id_employee' e 'sales_target' sejam numéricos
    target_salesperson = ensure_numeric_types(target_salesperson)
    
    # Log de informações sobre o DataFrame resultante
    print(f"Dados processados: {target_salesperson.shape[0]} registros de metas de vendas.")
    print(target_salesperson.head())  # Exibe as primeiras linhas para verificação
    
    # Retorna o DataFrame transformado
    return target_salesperson