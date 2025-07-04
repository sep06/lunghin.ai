"""Orquestrador principal do pipeline jurídico.

Este módulo centraliza as chamadas de cada agente do pipeline para que o
processo possa ser executado de forma encadeada e modular. O pipeline
atualmente conta com o agente de ingestão de documentos e o agente de
construção de grafos cognitivos.
"""

from agents.ingestor import processar_documento
from agents.graph_builder import construir_grafo


def executar_ingestao(caminho_arquivo: str) -> dict:
    """Executa o agente de ingestão e retorna seus dados."""

    return processar_documento(caminho_arquivo)


def executar_graph_builder(texto: str) -> dict:
    """Executa o agente de construção do grafo a partir do texto."""

    return construir_grafo(texto)


def run_pipeline(caminho_arquivo: str) -> dict:
    """Executa o pipeline completo de ingestão e construção do grafo."""

    # 1) Ingestão do documento
    dados_ingestao = executar_ingestao(caminho_arquivo)

    # 2) Construção do grafo cognitivo com o texto extraído
    grafo = executar_graph_builder(dados_ingestao["texto"])

    # 3) Consolida a saída em um único dicionário de resposta
    return {
        "status": "ok",
        "etapa": "ingestor + graph_builder",
        "tipo_entrada": dados_ingestao["tipo_entrada"],
        "texto": dados_ingestao.get("texto"),
        "entidades": grafo["entidades"],
        "relacoes": grafo["relacoes"],
        "graph_id": grafo["graph_id"],
    }
