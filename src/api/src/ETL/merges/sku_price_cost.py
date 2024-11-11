import pandas as pd

def merge_sku_data(sku_cost, sku_price, sku_ativos):
    sku_merged = pd.merge(sku_cost, sku_price, how='left', on='cod_prod')
    
    sku_active = pd.merge(sku_merged, sku_ativos, how='inner', on='cod_prod')
    
    return sku_active