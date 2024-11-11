import pandas as pd

def sales_employee_merge(employee,target_salesperson):
    sales_employee = pd.merge(employee, target_salesperson, on='id_employee', how='inner')
    return sales_employee