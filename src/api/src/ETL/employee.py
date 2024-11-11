import pandas as pd
from prefect import task,flow

@task
def filter_active_employees(df):
    filtered_df = df[(df['status'] == 'ativo') & 
                     (df['end_date'].isna()) & 
                     (df['role'] == 'vendedor')]
    return filtered_df

@task
def remove_end_date_column(df):
    df_without_end_date = df.drop('end_date', axis=1)
    return df_without_end_date

@task
def convert_initial_date_to_datetime(df):
    df['initial_date'] = pd.to_datetime(df['initial_date'], format='%d/%m/%Y', errors='coerce')
    return df

@flow(name="Employee ETL")
def employee_etl(employeeDF):
    active_employees = filter_active_employees(employeeDF)
    
    # Remove a coluna 'end_date'
    active_employees_no_end_date = remove_end_date_column(active_employees)
    
    # Converte 'initial_date' para datetime
    processed_employees = convert_initial_date_to_datetime(active_employees_no_end_date)
    
    print(f"Dados processados: {processed_employees.shape[0]} registros de vendedores ativos.")
    print(processed_employees.head())  # Exibe as primeiras linhas para verificação
    
    return processed_employees

