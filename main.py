from config.path import data_raw, data_processed
from etl.loader import setup_inicial_banco, verificar_tabela
from etl.pipeline import run_pipeline

def main():

    setup_inicial_banco() # Cria stg e tabelas finais
    run_pipeline(data_raw, data_processed)

    #if not verificar_tabela('hospitais_pb'):
        #print("eae")


if __name__ == "__main__":
    main()