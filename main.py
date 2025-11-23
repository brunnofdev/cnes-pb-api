import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from etl.loader import verificar_tabela, setup_inicial_banco
from etl.pipeline import run_pipeline
from config.path import data_raw, data_processed

@asynccontextmanager
async def lifespan(app: FastAPI):
    #startup da API
    try:
        # Lógica inteligente de carga inicial
        if verificar_tabela("hospitais_pb"):
            print("-Iniciando API...")
        else:
            print("-Banco de Dados vazio, iniciando leitura de arquivo .csv")
            setup_inicial_banco()
            run_pipeline(data_raw, data_processed)
            print("-Tabelas criadas e preenchidas com sucesso!")
    except Exception as e:
        print(f"-Erro: {e}")

    #Recebe requisições nesse estágio.
    yield

    #Quando a execução da API é encerrada
    print("-Desligando API....")

app = FastAPI(title="API CNES Paraíba",
    description="Sistema de consulta de dados hospitalares normalizados.",
    version="1.0",
    lifespan=lifespan)
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

if __name__ == "__main__":
    # Permite rodar como script Python normal: python main.py
    uvicorn.run(app, host="127.0.0.1", port=8000)