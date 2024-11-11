import pandas as pd

def transaction_sellers_merge(transactions, employee):
    transaction_with_sellers = pd.merge(transactions, employee, left_on='cod_vendedor', right_on='id_employee', how='left')
    return transaction_with_sellers
