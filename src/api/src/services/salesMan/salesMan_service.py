from repository.salesMan.salesMan_repository import get_sales_target_by_user, get_store_inventory, get_recomendation_product
from configs.db import SessionLocal

def sales_target_by_user(user_id):
    db = SessionLocal()
    try:
        result = get_sales_target_by_user(
            db, user_id)
    finally:
        db.close()

    return result

def store_inventory(store_id):
    db = SessionLocal()
    try:
        result = get_store_inventory(
            db, store_id)
    finally:
        db.close()

    return result

def recomendation_product(product_id):
    db = SessionLocal()
    try:
        result = get_recomendation_product(
            db, product_id)
    finally:
        db.close()

    return result