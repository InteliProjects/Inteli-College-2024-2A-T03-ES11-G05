import pandas as pd
from datetime import datetime
from ETL.employee import employee_etl
from ETL.sku_cost import sku_cost_etl
from ETL.sku_price import sku_price_etl
from ETL.sku_status_dataset import sku_status_dataset_etl
from ETL.target_salesperson import targets_salesperson_etl
from ETL.transaction import transaction_etl
from ETL.merges.sales_employee import sales_employee_merge
from ETL.merges.sku_price_cost import merge_sku_data
from ETL.merges.transaction_sellers import transaction_sellers_merge

from configs.db import SessionLocal
import os

def init_ETL(tag, df):
    print("EXECUTING ETL...")
    match tag:
        case "sku_cost":
            data_frame_pos = sku_cost_etl(df)
            return data_frame_pos
        case "sku_price":
            data_frame_pos = sku_price_etl(df)
            return data_frame_pos
        case "sku_status_dataset":
            data_frame_pos = sku_status_dataset_etl(df)
            return data_frame_pos
        case "targets_salesperson":
            data_frame_pos = targets_salesperson_etl(df)
            return data_frame_pos
        case "store_final":
            return df
        case "employee_final":
            data_frame_pos = employee_etl(df)
            return data_frame_pos
        case "transactions":
            data_frame_pos = transaction_etl(df)
            return data_frame_pos
        case _:
            return df
            
    
def merge_tables(tables: list, user):
    from services.ingest.working_data_service import process_data,prepare_dataframe_for_insert, insert_working_data
        # Dicionário para mapear as tabelas
    table_dict = {table['tag']: table['df'] for table in tables}

    # Verifica se 'employee' e 'target_sales_person' estão presentes
    if 'employee_final' in table_dict and 'targets_salesperson' in table_dict:
        tag = "employee_targets"
        employe_df = table_dict['employee_final']
        targets_salesperson_df = table_dict['targets_salesperson']
        print("Realizando o merge entre employe e target_sales_person")

        df_sales_employee = sales_employee_merge(
            employe_df, 
            targets_salesperson_df
        )

        filename = process_data(df_sales_employee)
        df_parquet = pd.read_parquet(filename)
        df_prepared = prepare_dataframe_for_insert(df_parquet)

        data_ingestao = datetime.utcnow()

        db = SessionLocal()
        try:
            insert_working_data(
                db, data_ingestao, df_prepared, tag, user.user.email)
        finally:
            db.close()

    
    # Verifica se 'sku_cost', 'sku_price' e 'sku_status' estão presentes
    if 'sku_cost' in table_dict and 'sku_price' in table_dict and 'sku_status_dataset' in table_dict:
        sku_cost_df = table_dict['sku_cost']
        sku_price_df = table_dict['sku_price']
        sku_status_df = table_dict['sku_status_dataset']
        print("Realizando o merge entre sku_cost, sku_price e sku_status")
        # Aqui você colocaria o código para realizar o merge entre as três tabelas
        # merged_df = sku_cost_df.merge(sku_price_df, on="coluna_comum").merge(sku_status_df, on="outra_coluna_comum")
    
    return True