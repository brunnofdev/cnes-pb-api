from fastapi import APIRouter, HTTPException
from psycopg2.extras import RealDictCursor

from config.path import data_raw, data_processed
from etl.helpers import remover_acentos, MAPA_TIPOS
from etl.loader import carregar_mapa_cidades, setup_inicial_banco, get_conn

from etl.pipeline import run_pipeline

print("Carregando mapa de cidades!")
MAPA_CIDADES = carregar_mapa_cidades()
print("CArregamento concluído!")
print(MAPA_CIDADES.get("MONTEIRO"))
router = APIRouter()


@router.get("/cnes/buscar")
def buscar_hospitais(cidade: str = None, tipo: str = None):
    """
    Busca hospitais filtrando por Cidade (Nome) e/ou Tipo de Unidade.
    """
    conn = None
    cur = None

    try:
        # 1. Conexão Manual
        conn = get_conn()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # 2. Preparação dos Filtros
        filtros = []
        params = []

        # --- Filtro de Cidade ---
        if cidade:
            nome_limpo = remover_acentos(cidade)
            cod_ibge = MAPA_CIDADES.get(nome_limpo)

            if not cod_ibge:
                raise HTTPException(404, f"Cidade '{cidade}' não encontrada.")

            filtros.append("e.co_ibge = %s")
            params.append(cod_ibge)

        # --- Filtro de Tipo ---
        if tipo:
            tipo_limpo = remover_acentos(tipo)
            # Aqui está a mágica: Tenta traduzir, se não der, usa o original
            cod_tipo = MAPA_TIPOS.get(tipo_limpo, tipo_limpo)

            filtros.append("h.tp_unidade = %s")
            params.append(cod_tipo)

        # 3. Montagem do SQL
        # Se não tiver filtros, where_clause fica vazia e traz tudo (limitado)
        where_clause = "AND " + " AND ".join(filtros) if filtros else ""

        sql = f"""
            SELECT 
                h.no_fantasia, 
                h.nu_telefone, 
                h.no_email,
                e.no_bairro, 
                e.no_logradouro,
                esf.descricao as esfera,
                trn.descricao as turno
            FROM hospitais_pb h
            JOIN enderecos e ON h.co_cnes = e.co_cnes
            LEFT JOIN esferas_administrativas esf ON h.esfera_id = esf.id
            LEFT JOIN turnos_atendimento trn ON h.turno_id = trn.id
            WHERE 1=1 {where_clause}
            LIMIT 50
        """

        # 4. Execução
        cur.execute(sql, tuple(params))
        resultados = cur.fetchall()

        return {
            "filtros": {"cidade": cidade, "tipo": tipo},
            "total": len(resultados),
            "dados": resultados
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(500, f"Erro interno: {e}")
    finally:
        if cur: cur.close()
        if conn: conn.close()



@router.post("/cnes/atualizar")
def atualizar_sistema():
    # Lógica síncrona para garantir consistência
    try:
        setup_inicial_banco()
        run_pipeline(data_raw, data_processed)
        return {"status": "ok", "msg": "Banco atualizado com sucesso."}
    except Exception as e:
        raise HTTPException(500, f"Falha na atualização: {e}")