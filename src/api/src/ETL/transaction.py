from prefect import task,flow
import pandas as pd
import os

def transaction_fist_time(transactionsDFs):
    transaction_final = [file for file in files if file.endswith('.csv')]
    transaction_final = [pd.read_csv(os.path.join(transaction_list, file), encoding='latin-1') for file in transaction_final]

    # Lista para armazenar os DataFrames processados
    all_grouped_dfs = []

    # Percorrer cada DataFrame dentro de transaction_final
    for df in transaction_final:
        transaction_grouped = df.groupby(['cod_transacao']).agg({
            'quantidade': 'sum',
            'cod_prod': lambda x: ', '.join(x.astype(str)),
            'preco': 'sum',
            'cod_vendedor': 'first',
            'cod_loja': 'first'
        }).reset_index()  # Reseta o index para manter 'cod_transacao' como coluna

        # Adiciona o DataFrame processado à lista
        all_grouped_dfs.append(transaction_grouped)

    # Concatenar todos os DataFrames em um único DataFrame gigante
    final_dataset = pd.concat(all_grouped_dfs, ignore_index=True)

    return final_dataset

@task
def convert_data_to_datetime(df):
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y', errors='coerce')
    return df

@task
def ensure_numeric_types(df):
    df['quantidade'] = df['quantidade'].astype(int)
    df['cod_prod'] = df['cod_prod'].astype(int)
    df['preco'] = df['preco'].astype(float)
    df['cod_vendedor'] = df['cod_vendedor'].astype(int)
    return df

@flow(name="Transaction ETL")
def transaction_etl(transactionsDFs):
    transactions = transactionsDFs.copy()
    
    # Passo 1: Garante que a coluna 'data' está no formato de data
    transactions = convert_data_to_datetime(transactions)
    
    # Passo 2: Garante que as colunas 'quantidade', 'cod_prod', 'preco', e 'cod_vendedor' são numéricas
    transactions = ensure_numeric_types(transactions)
    
    # Passo 3: Remove duplicados com base no 'cod_transacao'
    transactions = transactions.drop_duplicates(subset=['cod_transacao'])
    
    # Passo 4: Remove linhas com valores nulos nas colunas essenciais
    transactions = transactions.dropna(subset=['cod_transacao', 'cod_prod', 'cod_vendedor', 'cod_loja'])
    
    # Passo 5: Valida se os valores de 'preco' são positivos
    transactions = transactions[transactions['preco'] > 0]
    
    # Retorna o DataFrame transformado
    return transactions

