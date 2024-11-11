from sqlalchemy import Column, String, DateTime
from clickhouse_sqlalchemy import get_declarative_base

Base = get_declarative_base()

class WorkingData(Base):
    __tablename__ = 'working_data'
    data_ingestao = Column(DateTime, primary_key=True)
    dado_linha = Column(String)
    tag = Column(String)
    createdBy = Column(String)
