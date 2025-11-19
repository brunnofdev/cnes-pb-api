import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

# --- MUDANÇA 1: A URL de Conexão --
# O formato padrão é: postgresql://USUARIO:SENHA@HOST/NOME_DO_BANCO
# Exemplo abaixo assumindo que seu usuário é 'postgres', senha 'admin' e banco 'cnes_db'
SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URL')

# --- MUDANÇA 2: Limpeza no create_engine ---
# Removemos o 'connect_args={"check_same_thread": False}' pois ele é exclusivo do SQLite.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()