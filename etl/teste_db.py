import psycopg2

def testar_conexao():
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5433,  # Use a porta do seu docker-compose
            database="cnes",
            user="postgres",
            password="postgres"
        )
        print("Conexão OK! Python -> PostgreSQL funcionando.")
        conn.close()
    except Exception as e:
        print("Erro de conexão:", e)

if __name__ == "__main__":
    testar_conexao()
