import pandas as pd
# 1. Padroniza nomes de colunas
def padronizar_colunas(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(' ', '_')
        .str.replace(r'[^\w]', '', regex=True)
    )
    return df

# 2. Limpeza básica de strings

def limpar_strings(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.select_dtypes(include='object').columns:

        df[col] = df[col].astype(str).str.strip().replace({'': None})

    return df

# 3. Filtro específico: hospitais da Paraíba

def filtrar_hospitais_pb(df: pd.DataFrame) -> pd.DataFrame:

    # Ajuste conforme sua coluna que indica UF

    if 'uf' in df.columns:

        df = df[df['uf'].str.upper() == 'PB']

    # Ajuste conforme sua coluna que indica tipo de estabelecimento

    if 'tipo_estabelecimento' in df.columns:

        df = df[df['tipo_estabelecimento'].str.lower().str.contains('hospital')]

    return df

# 4. Separação e padronização de endereço
def separar_endereco(df: pd.DataFrame) -> pd.DataFrame:
    """
    Garante que o endereço esteja separado em colunas:
    logradouro, numero, bairro, cep.
    """
    if 'endereco' in df.columns:
        endereco_split = df['endereco'].str.split(',', expand=True)

        if endereco_split.shape[1] >= 4:
            df['logradouro'] = endereco_split[0].str.strip()
            df['numero'] = endereco_split[1].str.strip()
            df['bairro'] = endereco_split[2].str.strip()
            df['cep'] = endereco_split[3].str.strip()
        df.drop(columns=['endereco'], inplace=True)
    else:
        # Caso já existam colunas separadas, apenas garantir limpeza
        for col in ['logradouro', 'numero', 'bairro', 'cep']:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
    return df