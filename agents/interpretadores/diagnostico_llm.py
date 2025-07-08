"""Orquestrador principal do pipeline jurídico.

Este módulo centraliza as chamadas de cada agente do pipeline para que o
processo possa ser executado de forma encadeada e modular. O pipeline
atualmente conta com:
- Agente de ingestão
- Agente de construção de grafo
- Agente revisor técnico
- Agente interpretador com LLM
- Agente parecerista
- Agente exportador (PDF)
"""

from agents.ingestores.ingestor import processar_documento
from agents.extratores.graph_builder import construir_grafo
from agents.revisores.revisor_contratos import revisar_contrato
from agents.interpretadores.avaliador_llm import avaliar_clausulas_com_llm
from agents.pareceristas.parecerista import produzir_parecer
from agents.exportadores.exportador import gerar_relatorio_pdf


def executar_ingestao(caminho_arquivo: str) -> dict:
    return processar_documento(caminho_arquivo)


def executar_graph_builder(texto: str) -> dict:
    return construir_grafo(texto)


def executar_revisor(entidades: list, relacoes: list) -> dict:
    return revisar_contrato(entidades, relacoes)


def executar_diagnostico_llm(entidades: list) -> list:
    return avaliar_clausulas_com_llm(entidades)


def executar_parecerista(entidades: list, relacoes: list, parecer: dict) -> dict:
    return produzir_parecer(entidades, relacoes, parecer)


def executar_exportador(
    dados_ingestao: dict,
    grafo: dict,
    parecer_tecnico: dict,
    parecer_final: dict,
) -> str:
    return gerar_relatorio_pdf(dados_ingestao, grafo, parecer_tecnico, parecer_final)


def run_pipeline(caminho_arquivo: str) -> dict:
    # 1) Ingestão do documento
    dados_ingestao = executar_ingestao(caminho_arquivo)

    # 2) Construção do grafo jurídico
    grafo = executar_graph_builder(dados_ingestao["texto"])

    # 3) Revisão jurídica técnica (simbólica)
    parecer_tecnico = executar_revisor(grafo["entidades"], grafo["relacoes"])

    # 4) Diagnóstico interpretativo via LLM
    diagnosticos_llm = executar_diagnostico_llm(grafo["entidades"])
    grafo["diagnosticos_llm"] = diagnosticos_llm

    # 5) Geração do parecer final
    parecer_final = executar_parecerista(grafo["entidades"], grafo["relacoes"], parecer_tecnico)

    # 6) Geração do relatório PDF final
    caminho_pdf = executar_exportador(dados_ingestao, grafo, parecer_tecnico, parecer_final)

    # 7) Resposta consolidada
    return {
        "status": "ok",
        "etapa": "pipeline completo",
        "tipo_entrada": dados_ingestao["tipo_entrada"],
        "texto": dados_ingestao.get("texto"),
        "entidades": grafo["entidades"],
        "relacoes": grafo["relacoes"],
        "graph_id": grafo["graph_id"],
        "diagnosticos_llm": diagnosticos_llm,
        "parecer_tecnico": parecer_tecnico,
        "parecer_final": parecer_final,
        "relatorio_pdf": caminho_pdf,
    }
