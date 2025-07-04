"""Orquestrador principal do pipeline jurídico.

Este módulo centraliza as chamadas de cada agente do pipeline para que o
processo possa ser executado de forma encadeada e modular. O pipeline
atualmente conta com:
- Agente de ingestão
- Agente de construção de grafo
- Agente revisor
- Agente parecerista
"""

from agents.ingestor import processar_documento
from agents.graph_builder import construir_grafo
from agents.revisor_contratos import revisar_contrato
from agents.parecerista import produzir_parecer


def executar_ingestao(caminho_arquivo: str) -> dict:
    """Executa o agente de ingestão e retorna seus dados."""
    return processar_documento(caminho_arquivo)


def executar_graph_builder(texto: str) -> dict:
    """Executa o agente de construção do grafo a partir do texto."""
    return construir_grafo(texto)


def executar_revisor(entidades: list, relacoes: list) -> dict:
    """Executa o agente revisor e retorna o parecer técnico."""
    return revisar_contrato(entidades, relacoes)


def executar_parecerista(entidades: list, relacoes: list, parecer: dict) -> dict:
    """Executa o agente parecerista e retorna o parecer final."""
    return produzir_parecer(entidades, relacoes, parecer)


def run_pipeline(caminho_arquivo: str) -> dict:
    """Executa o pipeline completo: ingestão → grafo → revisão → parecer final."""

    # 1) Ingestão do documento
    dados_ingestao = executar_ingestao(caminho_arquivo)

    # 2) Construção do grafo cognitivo com o texto extraído
    grafo = executar_graph_builder(dados_ingestao["texto"])

    # 3) Revisão jurídica com base no grafo
    parecer_tecnico = executar_revisor(grafo["entidades"], grafo["relacoes"])

    # 4) Geração do parecer jurídico final
    parecer_final = executar_parecerista(grafo["entidades"], grafo["relacoes"], parecer_tecnico)

    # 5) Consolida a saída em um único dicionário de resposta
    return {
        "status": "ok",
        "etapa": "ingestor + graph_builder + revisor + parecerista",
        "tipo_entrada": dados_ingestao["tipo_entrada"],
        "texto": dados_ingestao.get("texto"),
        "entidades": grafo["entidades"],
        "relacoes": grafo["relacoes"],
        "graph_id": grafo["graph_id"],
        "parecer_tecnico": parecer_tecnico,
        "parecer_final": parecer_final,
    }
