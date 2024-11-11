from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
from services.salesMan.salesMan_service import sales_target_by_user, store_inventory, recomendation_product
from configs.db import get_db, SessionLocal
import os

router = APIRouter(
    prefix="/sales-man",
    tags=["sales-man"],
    responses={404: {"description": "View route not found"}}
)

class SalesMonthRequest(BaseModel):
    store_id: str

class SalesUserRequest(BaseModel):
    user_id: str

class SalesProductRequest(BaseModel):
    product_id: str

@router.post("/sales-target")
def get_sales_target_user(request: SalesUserRequest):
    result = sales_target_by_user(request.user_id)

    return result

@router.post("/inventory")
def get_store_inventory(request: SalesMonthRequest):
    result = store_inventory(request.store_id)

    return result

@router.post("/recomendation")
def get_recomendation_product(request: SalesProductRequest):
    result = recomendation_product(request.product_id)

    return result