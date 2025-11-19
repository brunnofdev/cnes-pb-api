import pandas as pd
import psycopg2
from .helpers import padronizar_colunas, limpar_strings, filtrar_hospitais_pb, separar_endereco

# Funções de banco de dados
def save_to_postgres(df, table_name):
    """Insere um DataFrame diretamente no PostgreSQL."""
    conn = psycopg2.connect(
        host="localhost",
        port=5433,  # ajuste conforme seu Docker
        database="cnes",
        user="postgres",
        password="postgres"
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
def processar_cnes_em_chunks(input_csv, chunk_size=50000, dry_run=True):
    """
    Processa o CSV do CNES em chunks.
    dry_run=True: apenas imprime os resultados (para testes)
    dry_run=False: insere os dados no PostgreSQL
    """
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
            continue  # não salva no banco se dry_run=True
        # Inserção no PostgreSQL
        if not chunk.empty:
            save_to_postgres(chunk, "hospitais_pb")

# Execução
def main():
    processar_cnes_em_chunks(
        input_csv="data/raw/teste.csv",  # altere se quiser usar teste.csv
        chunk_size=50000,
        dry_run=True  # True para teste, False para salvar no banco
    )

if __name__ == "__main__":
    main()
