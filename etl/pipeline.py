import os
from dotenv import load_dotenv
import pandas as pd
import psycopg2
import psycopg2.extras
from etl.helpers import filtrar_hospitais_pb, limpar_strings, padronizar_colunas
from config.path import data_raw, data_processed

# Carregar variáveis do .env
load_dotenv()

# variável de ambiente para conexão com o PostgreSQL
PG_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS")
}

# Funções de banco de dados
def save_to_postgres_bulk(df, table_name):
    if df.empty:
        return
    
    # Insere um DataFrame diretamente no PostgreSQL
    conn = psycopg2.connect(**PG_CONFIG)
    cur = conn.cursor()

    # colunas selecionadas para inserção
    # a ordem das colunas deve corresponder à ordem na tabela do banco
    colunas_desejadas = [
        'co_cnes', 'no_fantasia', 'co_ibge', 
        'no_logradouro', 'nu_endereco', 'no_bairro', 'co_cep', 'nu_telefone'
    ]
    # filtro para garantir que só as colunas desejadas sejam inseridas
    df_final = df.reindex(columns=colunas_desejadas)

    cols_str = ', '.join(colunas_desejadas)
    vals_str = ', '.join(['%s'] * len(colunas_desejadas))
    
    # Tratamento de nulos para SQL
    df_to_insert = df_final.where(pd.notnull(df_final), None)
    valores = [tuple(x) for x in df_to_insert.to_numpy()]

    query = f"INSERT INTO {table_name} ({cols_str}) VALUES %s"

    try:
        psycopg2.extras.execute_values(cur, query, valores, template=f"({vals_str})")
        conn.commit()
        print(f"Inseridas {len(df)} linhas no banco.")
    except Exception as e:
        conn.rollback()
        print(f"Erro ao inserir: {e}")
    finally:
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

    chunks = pd.read_csv(
        input_csv, 
        sep=';', 
        dtype=str, 
        chunksize=chunk_size, 
        encoding='latin1', # Teste 'utf-8' se os acentos ficarem estranhos
        quotechar='"' # para lidar com aspas corretamente
    )

    for i, chunk in enumerate(chunks):
        chunk = padronizar_colunas(chunk)
        chunk = filtrar_hospitais_pb(chunk)
        
        if chunk.empty:
            continue

        print(f"Chunk {i}: Processando {len(chunk)} registros da PB...")
        chunk = limpar_strings(chunk)

        if dry_run:
            print(chunk[['co_cnes', 'no_fantasia', 'no_bairro']].head())
            continue

        chunk.to_csv(output_csv, mode="w" if primeiro else "a", sep=';', index=False, header=primeiro)
        primeiro = False

        save_to_postgres_bulk(chunk, "hospitais_pb")