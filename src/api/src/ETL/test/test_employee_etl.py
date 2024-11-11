import pandas as pd
from ETL.employee import employee_etl

def test_employee_etl():
    # Simulando um DataFrame com dados de funcionários
    data = {
        'status': ['ativo', 'inativo', 'ativo', 'ativo', 'inativo'],
        'end_date': [None, '10/09/2022', None, None, '15/01/2023'],
        'role': ['vendedor', 'gerente', 'vendedor', 'vendedor', 'analista'],
        'initial_date': ['10/05/2021', '15/03/2019', '25/08/2020', '05/06/2018', '18/07/2021']
    }
    
    df = pd.DataFrame(data)
    
    # Executa o fluxo de ETL
    processed_employees = employee_etl(df)
    
    # Verifique se o número de registros de funcionários ativos está correto (deve ser 3)
    assert processed_employees.shape[0] == 3
    
    # Verifique se a coluna 'end_date' foi removida
    assert 'end_date' not in processed_employees.columns
    
    # Verifique se a coluna 'initial_date' foi convertida corretamente para datetime
    assert pd.api.types.is_datetime64_any_dtype(processed_employees['initial_date'])
    
    # Verifique os valores finais (exemplo: o primeiro registro de 'initial_date')
    assert processed_employees['initial_date'].iloc[0] == pd.to_datetime('10/05/2021', format='%d/%m/%Y')

