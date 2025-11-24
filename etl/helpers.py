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

# Padronização de sinônimos e abreviações
def tratar_sinonimos(df: pd.DataFrame) -> pd.DataFrame:

    # Abreviação de termos comuns em endereços
    if 'no_logradouro' in df.columns:
        # Dicionário de Regex: \b garante palavra exata
        regras = {
            r'\bAVENIDA\b': 'AV',
            r'\bRUA\b': 'R',
            r'\bDOUTOR\b': 'DR',
            r'\bPRESIDENTE\b': 'PRES',
            r'\bCORONEL\b': 'CEL',
            r'\bPRACA\b': 'PC',
            r'\bPROFESSOR\b': 'PROF',
            r'\bENGENHEIRO\b': 'ENG'
        }
        
        for padrao, substituto in regras.items():
            df['no_logradouro'] = df['no_logradouro'].str.replace(padrao, substituto, regex=True)

    # Padronização dos turnos de atendimento
    if 'ds_turno_atendimento' in df.columns:
        mapa_turnos = {
            'ATENDIMENTOS NOS TURNOS DA MANHA E A TARDE': 'DIURNO',
            'ATENDIMENTO NOS TURNOS DA MANHA, TARDE E NOITE': 'INTEGRAL',
            'ATENDIMENTO CONTINUO DE 24 HORAS/DIA (PLANTAO:INCLUI SABADOS, DOMINGOS E FERIADOS)': 'PLANTAO 24H',
            'ATENDIMENTO SOMENTE PELA MANHA': 'MANHA',
            'ATENDIMENTO SOMENTE A TARDE': 'TARDE',
            'ATENDIMENTO SOMENTE A NOITE': 'NOITE'
        }
        df['ds_turno_atendimento'] = df['ds_turno_atendimento'].replace(mapa_turnos)

    return df