from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from pydantic import BaseModel
from services.ingest.working_data_service import process_and_save_data, get_data_by_tag, process_and_save_data_transaction
from middlewares.auth_middleware import get_current_user
from typing import List
from ETL.main import merge_tables
import time
import re

router = APIRouter(
    prefix="/ingest",
    tags=["ingest"],
    responses={404: {"description": "Ingest route not found"}}
)


class Request(BaseModel):
    tag: str

class Trigger(BaseModel):
    bucket: str
    object: str


@router.post("/")
async def postIngest(files: List[UploadFile] = File(...), current_user: dict = Depends(get_current_user)):
    results = []
    errors = []
    dataframes = []
    for file in files:
        try:
            # Generate tag from filename
            filename = file.filename
            filename = filename.lower().replace(" ", "_")

            filename = filename.split(".")[0]

            arquivos = [
                "targets_salesperson",
                "target_store",
                "store_final",
                "sku_status_dataset",
                "sku_price",
                "sku_dataset",
                "sku_cost",
                "inventory_dataset",
                "employee_final",
                "transaction_fact",
                "transaction_fact_2",
                "inventory",
                "recomendacao"
            ]

            if filename not in arquivos:
                #Verificar se é um transaction_fact_2023
                if re.match(r'^transaction_fact_20[2-3][0-9]$', filename):
                    filename = "transaction_fact"
                else:
                    raise Exception("Nome do arquivo inválido")

            if (filename == "transaction_fact" or filename == "transaction_fact_2"):
                saved_data = process_and_save_data_transaction(file, filename, current_user)
            else:
                saved_data = process_and_save_data(file, filename, current_user)
                results.append(
                {"file": file.filename, "status": "success", "data": saved_data})
            dataframes.append({"df":saved_data.df, "tag":filename})
            
        except Exception as e:
            results.append(
                {"file": file.filename, "status": "error", "error": str(e)})

    return {"message": "Processamento concluído", "results": results}


@router.get("/visualize/{tag}")
async def get_visualize(tag: str):
    try:
        # Fetch data by tag
        data = get_data_by_tag(tag)
        if not data:
            raise HTTPException(status_code=404, detail="Data not found")
        return {"message": "Data retrieved successfully", "data": data}
    except Exception as e:
        return {"message": "Error retrieving data", "error": str(e)}


@router.post("/process")
async def process_data(request: Trigger):
    print(request)
    return {"message": "Data processing triggered successfully", "data": request}