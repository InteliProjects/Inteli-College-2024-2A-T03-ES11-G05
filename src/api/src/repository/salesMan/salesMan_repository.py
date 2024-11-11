from models.working_data import WorkingData
from sqlalchemy.sql import text
import pandas as pd
from sqlalchemy import text
from datetime import datetime


def get_sales_target_by_user(db, user_id):
    # Consultar a view com o parâmetro seguro
    select_query = "SELECT * FROM target_sales_by_employee ts WHERE ts.id_employee = :user_id"
    
    result_proxy = db.execute(text(select_query), {'user_id': user_id})
    
    # Obter os resultados e as colunas
    result_set = result_proxy.fetchall()
    columns = result_proxy.keys()
    
    # Criar o DataFrame com os dados e as colunas corretas
    df = pd.DataFrame(result_set, columns=columns)
    
    # Certificar que o DataFrame não está vazio
    if not df.empty:
        # Converter o DataFrame para uma lista de dicionários (formato records)
        return df.to_dict(orient='records')
    else:
        return []  # Retornar uma lista vazia se não houver dados
    
def get_store_inventory(db, store_id):
    # Consultar a view com o parâmetro seguro
    select_query = "SELECT * FROM inventory_by_store_current_day ts WHERE ts.store_name = :store_id"
    
    result_proxy = db.execute(text(select_query), {'store_id': store_id})
    
    # Obter os resultados e as colunas
    result_set = result_proxy.fetchall()
    columns = result_proxy.keys()
    
    # Criar o DataFrame com os dados e as colunas corretas
    df = pd.DataFrame(result_set, columns=columns)
    
    # Certificar que o DataFrame não está vazio
    if not df.empty:
        # Converter o DataFrame para uma lista de dicionários (formato records)
        return df.to_dict(orient='records')
    else:
        return []  # Retornar uma lista vazia se não houver dados
    
def get_recomendation_product(db, product_id):
    # Consultar a view com o parâmetro seguro
    select_query = "SELECT * FROM recommended_products rp WHERE rp.product_id = :product_id"
    
    result_proxy = db.execute(text(select_query), {'product_id': product_id})
    
    # Obter os resultados e as colunas
    result_set = result_proxy.fetchall()
    columns = result_proxy.keys()
    
    # Criar o DataFrame com os dados e as colunas corretas
    df = pd.DataFrame(result_set, columns=columns)
    
    # Certificar que o DataFrame não está vazio
    if not df.empty:
        # Converter o DataFrame para uma lista de dicionários (formato records)
        return df.to_dict(orient='records')
    else:
        return []  # Retornar uma lista vazia se não houver dados