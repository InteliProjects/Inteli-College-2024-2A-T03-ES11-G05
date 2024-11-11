import pandas as pd
from ETL.transaction import transaction_etl

def test_transaction_etl():
    # Simulando um DataFrame com dados de transações
    data = {
        'cod_vendedor': [101, 102, 103, 104],
        'transaction_date': ['10/05/2023', '15/06/2023', '25/07/2023', None],
        'amount': [1200.50, 800.75, None, 950.00]
    }
    
    df = pd.DataFrame(data)
    
    # Executa o fluxo de ETL
    processed_transactions = transaction_etl(df)
    
    # Verifique se o número de registros sem transações nulas foi tratado corretamente (deve ser 3)
    assert processed_transactions.shape[0] == 3
    
    # Verifique se a coluna 'data' foi convertida corretamente para datetime
    assert pd.api.types.is_datetime64_any_dtype(processed_transactions['data'])
    
    # Verifique se o valor 'preco' não possui mais valores nulos
    assert processed_transactions['preco'].isnull().sum() == 0
    
    # Verifique se a primeira data de transação foi convertida corretamente
    assert processed_transactions['data'].iloc[0] == pd.to_datetime('10/05/2023', format='%d/%m/%Y')