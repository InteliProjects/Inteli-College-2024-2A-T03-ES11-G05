from unittest.mock import MagicMock
import os
import pytest
from io import StringIO
from dotenv import load_dotenv
# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Agora as variáveis estarão disponíveis no ambiente
minio_root_user = os.getenv("MINIO_ROOT_USER")
minio_root_password = os.getenv("MINIO_ROOT_PASSWORD")
clickhouse_host = os.getenv("CLICKHOUSE_HOST")
clickhouse_port = os.getenv("CLICKHOUSE_PORT")
clickhouse_password = os.getenv("CLICKHOUSE_PASSWORD")
database_url = os.getenv("DATABASE_URL")
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
access_key_aws = os.getenv("ACCESS_KEY_AWS")
secret_key_aws = os.getenv("SECRET_KEY_AWS")
session_token_aws = os.getenv("SESSION_TOKEN_AWS")



@pytest.fixture(scope="module")
def db_session():
    from configs.db import engine
    from sqlalchemy.orm import sessionmaker

    # Setup: Create a new session
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    # Teardown: Close the session
    session.close()

    import pytest


@pytest.fixture
def mock_minio_client():
    mock_client = MagicMock()
    # Configure the mock client as needed
    mock_client.fget_object.return_value = None  # Example configuration
    return mock_client


@pytest.fixture
def sample_csv_file():
    # Create a sample CSV file content
    csv_content = """col1,col2
1,A
2,B
3,C"""
    return StringIO(csv_content)
