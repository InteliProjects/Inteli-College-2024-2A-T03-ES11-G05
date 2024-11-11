from datetime import datetime
from repository.ingest.working_data_repository import insert_working_data, search_duplicates
from configs.db import SessionLocal
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from utils.supabase_client import SupabaseClient
from io import StringIO
from sqlalchemy.orm import Session
from models.working_data import WorkingData
import json
from typing import List, Dict
import os
from configs.logging import Logger
from ETL.main import init_ETL
from utils.pydantic_models import StoreFinal, TargetStoreFinal, SkuStatusDataset, TargetsSalespersonFinal, SkuPrice, SkuDataset, SkuCost, EmployeeFinal

sb = SupabaseClient()

logger = Logger(
    log_group="cosmeticoders-api",
    log_stream="ingest-route",
)

def process_and_save_data(file, tag, user):
    logger.log("debug", f"Processing and saving data for tag {tag}")
    sb.create_bucket_if_not_exists("raw-data")

    if(tag == "employee_final"):
        decoded_file = file.file.read().decode("latin1")
    else:
        # Inicialmente, tente decodificar como UTF-8
        try:
            decoded_file = file.file.read().decode("utf-8")
        except UnicodeDecodeError as e:
            print(f"Erro ao decodificar como UTF-8: {e}")   
    
     # Carrega o conteúdo decodificado em um DataFrame
    if(tag == "sku_status_dataset" or tag == "sku_dataset"):
        df = pd.read_csv(StringIO(decoded_file),sep=';')
    else:
        df = pd.read_csv(StringIO(decoded_file), dtype={'date_column': str})

    df = init_ETL(tag, df)

    data_silver = df

    db = SessionLocal()

    filename = process_data(df)
    # Upload the Parquet file to Supabase
    if filename:
        logger.log("debug", f"Uploading file {filename} to Supabase")
        print(f"Uploading file {filename} to Supabase...")
        sb.upload_file("raw-data", filename)

        # Define the local path for the downloaded file
        logger.log("debug", f"Downloading file {filename} from Supabase")
        downloaded_filename = f"downloaded_{filename}"

        # Download the Parquet file from Supabase
        print(f"Downloading file {filename} from Supabase as {downloaded_filename}...")
        sb.download_file("raw-data", filename, downloaded_filename)

        # Check if the file was downloaded successfully
        if os.path.exists(downloaded_filename):
            print(f"File {downloaded_filename} downloaded successfully.")

            # Read the Parquet file
            df_parquet = pd.read_parquet(downloaded_filename)

            # Prepare the DataFrame for insertion
            df_prepared = prepare_dataframe_for_insert(df_parquet)

            data_ingestao = datetime.utcnow()
            db = SessionLocal()
            try:
                logger.log("debug", f"Ingesting data for tag {tag}")
                result = insert_working_data(
                    db, data_ingestao, df_prepared, tag, user.user.email)
            finally:
                db.close()

            logger.log("info", f"Data ingested successfully for tag {tag}")
            # Clean up downloaded file
            os.remove(downloaded_filename)

            return {"message": "Dados ingeridos com sucesso", "data": result, "df":data_silver}
        else:
            logger.log("error", f"File {downloaded_filename} not found after download")
            print(f"Erro: Arquivo {downloaded_filename} não encontrado após o download.")
            return {"message": "Erro ao ingerir dados", "error": f"Arquivo {downloaded_filename} não encontrado após download."}
    else:
        logger.log("error", "Error processing Parquet file")
        return {"message": "Erro ao processar arquivo Parquet"}

# def merge_process(list):
#     merge_tables_two(list)

def process_data(data):
    try:
        filename = f"raw_data_{datetime.now().strftime('%Y%m%d%H%M%S')}.parquet"
        table = pa.Table.from_pandas(data)
        pq.write_table(table, filename)
        return filename
    except Exception as e:
        print(f"Erro ao processar dados: {e}")
        return None


def prepare_dataframe_for_insert(df):
    try:
        df['dado_linha'] = df.apply(lambda row: row.to_json().replace('\\/', '/'), axis=1)
        df['data_ingestao'] = datetime.now()
        df['tag'] = 'tag'
        return df[['data_ingestao', 'dado_linha', 'tag']]
    except Exception as e:
        print(f"Erro ao preparar DataFrame: {e}")
        return None


def get_data_by_tag(tag: str) -> List[Dict]:
    # Create a new database session
    db: Session = SessionLocal()
    try:
        # Query the ClickHouse database for records with the given tag
        result = db.query(WorkingData).filter(WorkingData.tag == tag).all()
        structured_data = []
        for r in result:
            record = r.__dict__.copy()
            if 'dado_linha' in record:
                try:
                    record['dado_linha'] = json.loads(record['dado_linha'])
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON for record {record['id']}: {e}")
            structured_data.append(record)
        return structured_data
    except Exception as e:
        print(f"Error retrieving data by tag: {e}")
        return []
    finally:
        db.close()


def process_and_save_data_transaction(file, tag, user):
    decoded_file = file.file.read().decode("utf-8")  
    
    df = pd.read_csv(StringIO(decoded_file), dtype={'date_column': str})

    df_prepared = prepare_dataframe_for_insert(df)
    
    data_ingestao = datetime.utcnow()
    db = SessionLocal()
    try:
        logger.log("debug", f"Ingesting data for tag {tag}")
        result = insert_working_data(
            db, data_ingestao, df_prepared, tag, user.user.email)
    finally:
        db.close()

    return {"message": "Dados ingeridos com sucesso", "data": result}

def validate_csv_data(filename: str, data: list[dict]):
    model_mapping = {
        "targets_salesperson": TargetsSalespersonFinal,
        "target_store": TargetStoreFinal,
        "store_final": StoreFinal,
        "sku_status_dataset": SkuStatusDataset,
        "sku_price": SkuPrice,
        "sku_dataset": SkuDataset,
        "sku_cost": SkuCost,
        "employee_final": EmployeeFinal,
    }

    # Verificando se o nome do arquivo está no mapeamento
    if filename in model_mapping:
        model = model_mapping[filename]
        return [model(**row) for row in data]
    else:
        raise ValueError(f"Unknown file type: {filename}")