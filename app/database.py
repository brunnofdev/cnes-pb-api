import psycopg2
import os
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

def testar_conexao():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS")
        )
        print("Conexão OK! Python -> PostgreSQL funcionando.")
        conn.close()
    except Exception as e:
        print("Erro de conexão:", e)

if __name__ == "__main__":
    testar_conexao()
