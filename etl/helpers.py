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





































#Dicionário

MAPA_TIPOS = {
    # --- ATENÇÃO BÁSICA ---
    "POSTO DE SAUDE": "01",
    "CENTRO DE SAUDE": "02",
    "UBS": "02",
    "UNIDADE BASICA DE SAUDE": "02",
    "PSF": "02",
    "USF": "02",

    # --- ATENDIMENTO ESPECIALIZADO ---
    "POLICLINICA": "04",
    "CLINICA": "36",
    "CLINICA ESPECIALIZADA": "36",
    "AMBULATORIO": "36",
    "CENTRO DE ESPECIALIDADES": "36",
    "CONSULTORIO": "22",
    "CONSULTORIO ISOLADO": "22",

    # --- HOSPITAIS E URGÊNCIA ---
    "HOSPITAL": "05",
    "HOSPITAL GERAL": "05",
    "HOSPITAL ESPECIALIZADO": "07",
    "MATERNIDADE": "07",
    "UNIDADE MISTA": "15",
    "PRONTO SOCORRO": "20",
    "PA": "73",
    "PRONTO ATENDIMENTO": "73",
    "UPA": "73",
    "UNIDADE DE PRONTO ATENDIMENTO" : "73",
    "SAMU": "76",  # Ou 42 (Unidade Móvel) dependendo do cadastro

    # --- DIAGNÓSTICO E TERAPIA ---
    "SADT": "39",
    "DIAGNOSTICO": "39",
    "LABORATORIO": "39",
    "FISIOTERAPIA": "36",  # Geralmente em clínicas (36) ou reabilitação (84)
    "CENTRO DE REABILITACAO": "84",

    # --- SAÚDE MENTAL ---
    "CAPS": "70",
    "CENTRO DE ATENCAO PSICOSSOCIAL": "70",

    # --- OUTROS SERVIÇOS ENCONTRADOS NO CSV ---
    "FARMACIA": "43",
    "ACADEMIA DA SAUDE": "74",
    "VIGILANCIA SANITARIA": "50",
    "VIGILANCIA EM SAUDE": "50",
    "SECRETARIA DE SAUDE": "68",
    "CENTRAL DE REGULACAO": "81",
    "COOPERATIVA": "60",
    "HOME CARE": "77",
    "ATENCAO DOMICILIAR": "77",
    "TELESSAUDE": "75",
    "CENTRO DE IMUNIZACAO": "85",
    "LABORATORIO DE SAUDE PUBLICA": "80",
    "LACEN": "80"
}