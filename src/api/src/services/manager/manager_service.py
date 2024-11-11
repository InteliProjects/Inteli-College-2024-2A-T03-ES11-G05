from repository.manager.manager_repository import get_performance_store_six, get_sales_month, get_top_categories, get_top_products, get_sellers_performance
from configs.db import SessionLocal

def sales_month(store_id):
    db = SessionLocal()
    try:
        result = get_sales_month(
            db, store_id)
    finally:
        db.close()

    return result

def performance_store_six(store_id):
    db = SessionLocal()
    try:
        result = get_performance_store_six(
            db, store_id)
    finally:
        db.close()

    return result

def top_categories(store_id):
    db = SessionLocal()
    try:
        result = get_top_categories(
            db, store_id)
    finally:
        db.close()

    return result

def top_products(store_id):
    db = SessionLocal()
    try:
        result = get_top_products(
            db, store_id)
    finally:
        db.close()

    return result

def sellers_performance(store_id):
    db = SessionLocal()
    try:
        result = get_sellers_performance(
            db, store_id)
    finally:
        db.close()

    return result
