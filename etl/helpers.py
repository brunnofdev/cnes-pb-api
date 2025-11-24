import pandas as pd
import unicodedata

# Padronização dos nomes de colunas
def padronizar_colunas(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(' ', '_')
        .str.replace(r'[^\w]', '', regex=True)
    )
    return df


# Limpeza das strings
def limpar_strings(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.select_dtypes(include='object').columns:
        # Remover aspas duplas
        df[col] = df[col].astype(str).str.replace('"', '').str.strip()
        # Converter vazios e 'nan' para None
        df[col] = df[col].replace({'': None, 'nan': None, 'NaN': None})
    return df

# Filtro dos hospitais da Paraíba
def filtrar_hospitais_pb(df: pd.DataFrame) -> pd.DataFrame:
    # O código IBGE da Paraíba é 25
    if 'co_uf' in df.columns:
        # Filtra tanto '25' quanto 'PB' para garantir
        df = df[df['co_uf'].astype(str).str.upper().isin(['25', 'PB'])]
    return df

def remover_acentos(texto: str) -> str:
    if not isinstance(texto, str):
        return str(texto)
    return ''.join(c for c in unicodedata.normalize('NFD', texto)
                  if unicodedata.category(c) != 'Mn').upper().strip()
