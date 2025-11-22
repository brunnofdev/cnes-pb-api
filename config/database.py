import os
from dotenv import load_dotenv

# Carrega o .env
load_dotenv()

# Configuração Padrão
PG_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)), 
    "database": os.getenv("DB_NAME", "cnes_pb"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASS", "senha")
}

# String de Conexão (Para SQLAlchemy / Pandas / FastAPI)
def get_db_url():
    return f"postgresql+psycopg2://{PG_CONFIG['user']}:{PG_CONFIG['password']}@{PG_CONFIG['host']}:{PG_CONFIG['port']}/{PG_CONFIG['database']}"