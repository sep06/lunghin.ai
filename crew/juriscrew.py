"""Orquestrador principal do pipeline jurídico.

Este módulo centraliza as chamadas de cada agente do pipeline para que o
processo possa ser executado de forma encadeada e modular. O pipeline
atualmente conta com o agente de ingestão de documentos, o agente de
construção de grafos cognitivos e o agente revisor.
"""

from agents.ingestor import processar_documento
from agents.graph_builder import construir_grafo
from agents.revisor_contratos import revisar_contrato


def executar_ingestao(caminho_arquivo: str) -> dict:
    """Executa o agente de ingestão e retorna seus dados."""
    return processar_documento(caminho_arquivo)


def executar_graph_builder(texto: str) -> dict:
    """Executa o agente de construção do grafo a partir do texto."""
    return construir_grafo(texto)


def executar_revisor(entidades: list, relacoes: list) -> dict:
    """Executa o agente revisor e retorna o parecer."""
    return revisar_contrato(entidades, relacoes)


def run_pipeline(caminho_arquivo: str) -> dict:
    """Executa o pipeline completo: ingestão → grafo → revisão."""

    # 1) Ingestão do documento
    dados_ingestao = executar_ingestao(caminho_arquivo)

    # 2) Construção do grafo cognitivo com o texto extraído
    grafo = executar_graph_builder(dados_ingestao["texto"])

    # 3) Revisão jurídica com base no grafo
    parecer = executar_revisor(grafo["entidades"], grafo["relacoes"])

    # 4) Consolida a saída em um único dicionário de resposta
    return {
        "status": "ok",
        "etapa": "ingestor + graph_builder + revisor",
        "tipo_entrada": dados_ingestao["tipo_entrada"],
        "texto": dados_ingestao.get("texto"),
        "entidades": grafo["entidades"],
        "relacoes": grafo["relacoes"],
        "graph_id": grafo["graph_id"],
        "parecer": parecer,
    }
