import sys
from etl.pipeline import processar_cnes_em_chunks
from config.path import data_raw, data_processed

def main():
    print("Iniciando Pipeline de Dados CNES-PB")

    # Configurações de execução
    # Mude dry_run=True para teste e leitura sem gravar no banco
    processar_cnes_em_chunks(
        input_csv=data_raw,
        output_csv=data_processed,
        chunk_size=50000,
        dry_run=False 
    )
    print("Pipeline finalizado")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nErro fatal no pipeline: {e}")
        sys.exit(1)