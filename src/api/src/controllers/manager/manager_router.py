from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from services.manager.manager_service import performance_store_six, sales_month, top_categories, top_products, sellers_performance
from configs.db import get_db, SessionLocal
import os

router = APIRouter(
    prefix="/manager",
    tags=["manager"],
    responses={404: {"description": "View route not found"}}
)


# def load_sql_query(filename):
#     file_path = os.path.join('..', '..', 'sql', filename)
#     with open(file_path, 'r') as file:
#         return file.read()


# @router.get("/sales_targets_last_two_months")
# def get_sales_targets_last_two_months():
#     db: Session = SessionLocal()
#     create_view_query = load_sql_query('sales_targets_last_two_months.sql')
#     try:
#         # Criar a view se não existir
#         db.execute(text(create_view_query))
#         db.commit()

#         # Consultar a view
#         select_query = "SELECT * FROM sales_targets_last_two_months"
#         result_proxy = db.execute(text(select_query))

#         # Obter os nomes das colunas
#         columns = result_proxy.keys()

#         # Obter todos os resultados
#         result = result_proxy.fetchall()

#         # Converter o resultado em uma lista de dicionários
#         data = [dict(zip(columns, row)) for row in result]

#     except Exception as e:
#         db.rollback()
#         return {"message": f"Erro ao criar ou consultar a view: {e}"}
#     finally:
#         db.close()
#     return data


# @router.get("/store_sales_last_six_months")
# def get_store_sales_last_six_months():
#     db: Session = SessionLocal()
#     create_view_query = load_sql_query('store_sales_last_six_months.sql')
#     try:
#         db.execute(text(create_view_query))
#         db.commit()
#         select_query = "SELECT * FROM store_sales_last_six_months"
#         result_proxy = db.execute(text(select_query))
#         columns = result_proxy.keys()
#         result = result_proxy.fetchall()
#         data = [dict(zip(columns, row)) for row in result]
#     except Exception as e:
#         db.rollback()
#         return {"message": f"Erro ao criar ou consultar a view: {e}"}
#     finally:
#         db.close()
#     return data


# @router.get("/sales_by_category_last_two_months")
# def get_sales_by_category_last_two_months():
#     db: Session = SessionLocal()
#     create_view_query = load_sql_query('sales_by_category_last_two_months.sql')
#     try:
#         db.execute(text(create_view_query))
#         db.commit()
#         select_query = "SELECT * FROM sales_by_category_last_two_months"
#         result_proxy = db.execute(text(select_query))
#         columns = result_proxy.keys()
#         result = result_proxy.fetchall()
#         data = [dict(zip(columns, row)) for row in result]
#     except Exception as e:
#         db.rollback()
#         return {"message": f"Erro ao criar ou consultar a view: {e}"}
#     finally:
#         db.close()
#     return data


# @router.get("/top_products")
# def get_top_products():
#     db: Session = SessionLocal()
#     create_view_query = load_sql_query('top_products.sql')
#     try:
#         db.execute(text(create_view_query))
#         db.commit()
#         select_query = "SELECT * FROM top_products"
#         result_proxy = db.execute(text(select_query))
#         columns = result_proxy.keys()
#         result = result_proxy.fetchall()
#         data = [dict(zip(columns, row)) for row in result]
#     except Exception as e:
#         db.rollback()
#         return {"message": f"Erro ao criar ou consultar a view: {e}"}
#     finally:
#         db.close()
#     return data

class SalesMonthRequest(BaseModel):
    store_id: str

@router.post("/sales-month")
def get_sales_month(request: SalesMonthRequest):
    result = sales_month(request.store_id)

    return result


@router.post("/performance-by-store-six")
def get_sales_month(request: SalesMonthRequest):
    result = performance_store_six(request.store_id)

    return result

@router.post("/top-categories")
def get_sales_month(request: SalesMonthRequest):
    result = top_categories(request.store_id)

    return result

@router.post("/top-products")
def get_sales_month(request: SalesMonthRequest):
    result = top_products(request.store_id)

    return result

@router.post("/sellers-performance")
def get_sales_month(request: SalesMonthRequest):
    result = sellers_performance(request.store_id)

    return result