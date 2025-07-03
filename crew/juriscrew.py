"""Orquestrador principal do pipeline jurídico."""

from agents.ingestor import processar_documento


def executar_ingestao(caminho_arquivo: str) -> dict:
    """Executa o agente de ingestão e retorna seus dados."""

    return processar_documento(caminho_arquivo)


def run_pipeline(caminho_arquivo: str) -> dict:
    """Inicia o pipeline chamando apenas o agente de ingestão."""

    dados_ingestao = executar_ingestao(caminho_arquivo)

    return {
        "status": "ok",
        "etapa": "ingestor",
        "tipo_entrada": dados_ingestao["tipo_entrada"],
        "texto": dados_ingestao["texto"],
    }
