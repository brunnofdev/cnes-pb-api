import os
from dotenv import load_dotenv
import pandas as pd
import psycopg2
from etl.helpers import separar_endereco, filtrar_hospitais_pb, limpar_strings, padronizar_colunas

from path import data_raw, data_processed

# Carregar variáveis do .env
load_dotenv()

PG_HOST = os.getenv("DB_HOST")
PG_PORT = int(os.getenv("DB_PORT", 5432))
PG_DB = os.getenv("DB_NAME")
PG_USER = os.getenv("DB_USER")
PG_PASSWORD = os.getenv("DB_PASS")

# Funções de banco de dados
def save_to_postgres(df, table_name):
    """Insere um DataFrame diretamente no PostgreSQL."""
    conn = psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        database=PG_DB,
        user=PG_USER,
        password=PG_PASSWORD
    )
    cur = conn.cursor()
    for _, row in df.iterrows():
        cur.execute(f"""
            INSERT INTO {table_name} (codigo_estabelecimento, nome, municipio, logradouro, numero, bairro, cep)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            row.get("codigo_estabelecimento"),
            row.get("nome"),
            row.get("municipio"),
            row.get("logradouro"),
            row.get("numero"),
            row.get("bairro"),
            row.get("cep"),
        ))
    conn.commit()
    cur.close()
    conn.close()


# Função principal do pipeline
def processar_cnes_em_chunks(input_csv, output_csv, chunk_size=50000, dry_run=False):
    """
    Processa o CSV do CNES em chunks.
    dry_run=True: apenas imprime os resultados (para testes)
    dry_run=False: insere os dados no PostgreSQL e salva CSV
    """
    primeiro = True

    for chunk in pd.read_csv(input_csv, sep=';', dtype=str, chunksize=chunk_size, encoding='latin1'):
        # 1. Padroniza nomes de colunas
        chunk = padronizar_colunas(chunk)
        # 2. Limpeza básica
        chunk = limpar_strings(chunk)
        # 3. Filtro do seu caso (PB + hospitais)
        chunk = filtrar_hospitais_pb(chunk)
        # 4. Normalização / padronização de endereço
        chunk = separar_endereco(chunk)

        # Dry-run: apenas visualizar
        if dry_run:
            print("\n=== Pré-visualização do chunk transformado ===")
            print(chunk.head())
            print(f"Linhas restantes no chunk: {len(chunk)}")
            continue

        # Salva CSV incremental
        if not chunk.empty:
            chunk.to_csv(
                output_csv,
                mode="w" if primeiro else "a",
                sep=';',
                index=False,
                header=primeiro
            )
            primeiro = False

        # Inserção no PostgreSQL
        if not chunk.empty:
            save_to_postgres(chunk, "hospitais_pb")


# Execução
def main():
    processar_cnes_em_chunks(
        input_csv= data_raw,
        output_csv=data_processed,
        chunk_size=50000,
        dry_run=False
    )

