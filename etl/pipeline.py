import pandas as pd
from etl.helpers import padronizar_colunas, limpar_strings, filtrar_hospitais_pb
from etl.loader import carregar_staging, executar_normalizacao, limpar_staging

def run_pipeline(input_csv, output_csv, chunk_size=50000):

    limpar_staging()

    chunks = pd.read_csv(
        input_csv, sep=';', dtype=str, chunksize=chunk_size, 
        encoding='latin1', quotechar='"'
    )
    
    primeiro = True

    for chunk in chunks:
        chunk = padronizar_colunas(chunk)
        chunk = filtrar_hospitais_pb(chunk)
        
        if chunk.empty: continue
        
        chunk = limpar_strings(chunk)

        # Salva Backup CSV
        chunk.to_csv(output_csv, mode='w' if primeiro else 'a', 
                     sep=';', index=False, header=primeiro)
        primeiro = False

        # Carrega no Banco
        carregar_staging(chunk)
    
    # Normalização
    executar_normalizacao()