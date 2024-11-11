from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from clickhouse_sqlalchemy import make_session

from .settings import settings

DATABASE_URI = settings.DATABASE_URL

# Configurações do ClickHouse
CLICKHOUSE_URL = DATABASE_URI

# Criando o engine e a sessão
engine = create_engine(CLICKHOUSE_URL)
SessionLocal = sessionmaker(bind=engine)


def get_db():
    db = make_session(engine)()
    try:
        yield db
    finally:
        db.close()
