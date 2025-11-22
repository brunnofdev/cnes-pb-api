from config.path import data_raw, data_processed
from etl.loader import setup_inicial_banco
from etl.pipeline import run_pipeline

def main():
    setup_inicial_banco() # Cria stg e tabelas finais
    # Roda o processo
    run_pipeline(data_raw, data_processed)

if __name__ == "__main__":
    main()