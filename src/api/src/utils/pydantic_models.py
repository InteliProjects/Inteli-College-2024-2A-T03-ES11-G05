from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class StoreFinal(BaseModel):
    nome_loja: str
    regiao: str
    diretoria: str
    data_inauguracao: str  # Consider changing to date if you need strict validation

class TargetStoreFinal(BaseModel):
    month: str
    store_id: str
    sales_target: float

class SkuStatusDataset(BaseModel):
    cod_prod: int
    data_inicio: str  # You can convert this to date for stricter validation
    data_fim: Optional[str] = None  # Optional in case the status has no end date

class TargetsSalespersonFinal(BaseModel):
    id_employee: int
    sales_target: float
    month: str

class SkuPrice(BaseModel):
    cod_prod: int
    data_inicio: str  # You can convert this to date for stricter validation
    data_fim: Optional[str] = None  # Optional in case the price has no end date
    preco: float

class SkuDataset(BaseModel):
    cod_prod: int
    nome_abrev: str
    nome_completo: str
    descricao: Optional[str] = None
    categoria: str
    sub_categoria: Optional[str] = None
    marca: Optional[str] = None
    conteudo_valor: Optional[str] = None
    conteudo_medida: Optional[str] = None

class SkuCost(BaseModel):
    cod_prod: int
    data_inicio: str  # You can convert this to date for stricter validation
    data_fim: Optional[str] = None
    custo: float

class EmployeeFinal(BaseModel):
    id_employee: int
    name: str
    surname: str
    cpf: str
    status: str  # You may add an enum for 'ativo' and 'inativo'
    role: str
    initial_date: str  # You can convert this to date for stricter validation
    end_date: Optional[str] = None
    store_id: str
