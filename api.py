from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import uuid
from dotenv import load_dotenv
load_dotenv()


from crew.juriscrew import run_pipeline  # Certifique-se que isso existe ou crie um mock por enquanto

app = FastAPI()


@app.post("/executar-pipeline")
async def executar_pipeline(documento: UploadFile = File(...)):
    try:
        # Cria um caminho temporário para salvar o arquivo
        extensao = documento.filename.split(".")[-1]
        nome_temp = f"temp_{uuid.uuid4()}.{extensao}"
        caminho_arquivo = os.path.join("temp_uploads", nome_temp)

        # Garante que o diretório existe
        os.makedirs("temp_uploads", exist_ok=True)

        # Salva o arquivo
        with open(caminho_arquivo, "wb") as f:
            f.write(await documento.read())

        # Executa o pipeline principal
        resultado = run_pipeline(caminho_arquivo)

        # Retorna o resultado em JSON
        return JSONResponse(content=resultado)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao executar pipeline: {str(e)}")
