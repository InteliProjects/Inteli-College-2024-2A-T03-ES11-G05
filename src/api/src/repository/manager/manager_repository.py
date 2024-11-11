from models.working_data import WorkingData
from sqlalchemy.sql import text
import pandas as pd
from sqlalchemy import text
from datetime import datetime


def get_sales_month(db, store_id):
    # Consultar a view com o parâmetro seguro
    select_query = "SELECT * FROM sales_targets_last_two_months st WHERE st.store_id = :store_id"
    
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
    

def get_performance_store_six(db, store_id):
    # Consultar a view com o parâmetro seguro
    select_query = "SELECT * FROM store_sales_last_six_months ssl WHERE ssl.store_id = :store_id"
    
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
    
def get_top_categories(db, store_id):
    # Consultar a view com o parâmetro seguro
    select_query = "SELECT * FROM sales_by_category_last_two_months sbc WHERE sbc.store_id = :store_id ORDER BY sbc.total_sales DESC"

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

def get_top_products(db, store_id, top_n=2):
    # Obter o mês atual e o mês anterior
    current_month = datetime.now().month
    previous_month = current_month - 1 if current_month > 1 else 12
    
    # Query 1: Buscar os top N produtos do mês atual
    top_products_query = """
    SELECT TOP :top_n * FROM sales_by_product_last_two_months sbp 
    WHERE sbp.store_id = :store_id 
    AND sbp.month = :current_month 
    ORDER BY sbp.total_sales DESC
    """
    
    # Executa a query para buscar os top N produtos
    result_proxy = db.execute(text(top_products_query), {'top_n': top_n, 'store_id': store_id, 'current_month': current_month})
    top_products = pd.DataFrame(result_proxy.fetchall(), columns=result_proxy.keys())
    
    # Se não houver produtos retornados, encerrar
    if top_products.empty:
        return []

    # Extrair os nomes dos produtos top N
    top_product_names = top_products['product_name'].tolist()

    # Query 2: Buscar informações dos mesmos produtos no mês anterior
    products_last_month_query = """
    SELECT * FROM sales_by_product_last_two_months sbp 
    WHERE sbp.store_id = :store_id 
    AND sbp.month = :previous_month
    AND sbp.product_name IN :product_names
    """
    
    # Executa a query para os mesmos produtos no mês anterior
    result_proxy = db.execute(
        text(products_last_month_query), 
        {'store_id': store_id, 'previous_month': previous_month, 'product_names': tuple(top_product_names)}
    )
    
    previous_month_sales = pd.DataFrame(result_proxy.fetchall(), columns=result_proxy.keys())

    # Adicionar o valor de vendas do mês anterior ao DataFrame do mês atual
    if not previous_month_sales.empty:
        top_products = top_products.merge(previous_month_sales[['product_name', 'total_sales']], 
                                          on='product_name', 
                                          how='left', 
                                          suffixes=('', '_previous_month'))

    # Retornar os resultados como JSON, incluindo as vendas do mês anterior
    return top_products.to_dict(orient='records')

def get_sellers_performance(db, store_id):
    # Consultar a view com o parâmetro seguro
    select_query = "SELECT * FROM seller_performance_current_month spcm WHERE spcm.store_id = :store_id"

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
