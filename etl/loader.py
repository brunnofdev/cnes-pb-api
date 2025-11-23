import psycopg2
import psycopg2.extras
import pandas as pd
from config.path import sql_rawTable, sql_normalize, sql_tables
from config.database import PG_CONFIG

def get_conn():
    return psycopg2.connect(**PG_CONFIG)

def executar_script_sql(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        sql = f.read()
    
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def setup_inicial_banco():
    # Configuração inicial do banco: cria tabelas de staging e finais
    executar_script_sql(sql_rawTable) # Cria stg_hospitais_raw
    executar_script_sql(sql_tables) # Cria tabelas normalizadas

def carregar_staging(df: pd.DataFrame):
    # Carrega DataFrame na tabela de staging (stg_hospitais_raw)
    if df.empty: return

    # Mapeamento: Coluna do DF -> Coluna do Banco Raw
    # Certifique-se que os nomes aqui batem com o helpers.padronizar_colunas
    colunas_banco = [
        'co_cnes', 'no_fantasia', 'nu_cnpj_mantenedora', 'no_razao_social',
        'co_ibge', 'no_logradouro', 'nu_endereco', 'no_bairro', 'co_cep',
        'nu_telefone', 'tp_unidade', 'ds_esfera_administrativa', 
        'ds_turno_atendimento', 'nu_latitude', 'nu_longitude', 'no_email'
    ]
    
    # Filtra e ordena o DF
    df_insert = df.reindex(columns=colunas_banco).where(pd.notnull(df), None)
    
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            query = f"INSERT INTO stg_hospitais_raw ({','.join(colunas_banco)}) VALUES %s"
            valores = [tuple(x) for x in df_insert.to_numpy()]
            psycopg2.extras.execute_values(cur, query, valores)
            conn.commit()
    except Exception as e:
        conn.rollback()
    finally:
        conn.close()

def executar_normalizacao():
    # script de normalização (distribuição para tabelas finais)
    executar_script_sql(sql_normalize)

# Função para limpar a tabela de staging antes de carregar novos dados
def limpar_staging():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE stg_hospitais_raw")
            conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()

def verificar_tabela(nome_tabela):

    conn = get_conn()  # Usa sua função de conexão existente
    try:
        with conn.cursor() as cur:
            # Query super rápida: Tenta pegar só o primeiro registro
            cur.execute(f"SELECT 1 FROM {nome_tabela} LIMIT 1")
            resultado = cur.fetchone()

            if (resultado is not None):
                print("Tabela já existe")
                return True

    except Exception as e:
        print(f"Tabela inexistente ou inacessível")
        return False

    finally:
        conn.close()