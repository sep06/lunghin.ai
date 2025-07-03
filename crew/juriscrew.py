def run_pipeline(caminho_arquivo: str):
    """
    Mock inicial do pipeline cognitivo jurídico.
    Retorna apenas uma resposta de teste.
    """
    return {
        "status": "ok",
        "mensagem": "Pipeline executado com sucesso.",
        "arquivo_recebido": caminho_arquivo
    }
