from fastapi import APIRouter
from etl.loader import carregar_mapa_cidades

mapas_cidades = carregar_mapa_cidades()
router = APIRouter()

#@router.get("/busca/cep")
