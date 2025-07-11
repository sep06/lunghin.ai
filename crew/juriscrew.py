# coding: utf-8
"""
Orquestrador principal do pipeline jurídico.

Este módulo centraliza as chamadas de cada agente do pipeline para que o
processo possa ser executado de forma encadeada e modular. O pipeline
atualmente conta com:
- Agente de ingestão
- Agente de construção de grafo
- Agente revisor técnico
- Agente parecerista
- Agente exportador (PDF)
"""

import json
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

from agents.ingestores.ingestor import processar_documento
from agents.extratores.graph_builder import construir_grafo
from agents.revisores.revisor_contratos import revisar_contrato
from agents.pareceristas.parecerista import produzir_parecer
from agents.exportadores.relatorio_pdf import gerar_relatorio_pdf
from agents.interpretadores.avaliador_llm import avaliar_clausulas_com_llm
from agents.validadores.detector_campos import detectar_campos_em_branco  # NOVO

def executar_ingestao(caminho_arquivo: str) -> dict:
    return processar_documento(caminho_arquivo)

def executar_graph_builder(texto: str) -> dict:
    return construir_grafo(texto)

def executar_revisor(texto: str) -> dict:
    return revisar_contrato(texto)

def executar_parecerista(entidades: list, relacoes: list, parecer: dict) -> dict:
    return produzir_parecer(entidades, relacoes, parecer)

def executar_exportador(
    dados_ingestao: dict,
    grafo: dict,
    parecer_tecnico: dict,
    parecer_final: dict,
    avaliacoes_llm: list,
) -> str:
    return gerar_relatorio_pdf(dados_ingestao, grafo, parecer_tecnico, parecer_final, avaliacoes_llm)

def run_pipeline(caminho_arquivo: str) -> dict:
    print("🚀 Iniciando pipeline")
    dados_ingestao = executar_ingestao(caminho_arquivo)
    print("✅ Etapa 1: ingestão concluída")

    grafo = executar_graph_builder(dados_ingestao["texto"])
    print("✅ Etapa 2: grafo construído")

    parecer_tecnico = executar_revisor(dados_ingestao["texto"])
    print("✅ Etapa 3: revisão técnica concluída")

    avaliacoes_llm = avaliar_clausulas_com_llm(grafo["entidades"])
    print("🧠 Etapa 3.5: avaliação simbólica LLM concluída")

    parecer_final = executar_parecerista(grafo["entidades"], grafo["relacoes"], parecer_tecnico)
    print("✅ Etapa 4: parecer final gerado")

    campos_em_branco = detectar_campos_em_branco(dados_ingestao["texto"])
    print(f"🕳️ Etapa 4.5: campos em branco detectados: {len(campos_em_branco)} encontrados")

    caminho_pdf = executar_exportador(
        dados_ingestao, grafo, parecer_tecnico, parecer_final, avaliacoes_llm
    )
    print(f"✅ Etapa 5: relatório PDF gerado em {caminho_pdf}")

    resultado = {
        "status": "ok",
        "etapa": "pipeline completo",
        "tipo_entrada": dados_ingestao["tipo_entrada"],
        "texto": dados_ingestao.get("texto"),
        "entidades": grafo["entidades"],
        "relacoes": grafo["relacoes"],
        "graph_id": grafo["graph_id"],
        "parecer_tecnico": parecer_tecnico,
        "parecer_final": parecer_final,
        "avaliacoes_llm": avaliacoes_llm,
        "campos_em_branco": campos_em_branco,
        "relatorio_pdf": str(caminho_pdf) if isinstance(caminho_pdf, Path) else caminho_pdf,
    }

    try:
        print("📦 Resultado final:")
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"❌ Erro ao serializar JSON final: {e}")

    return resultado


__all__ = ["run_pipeline"]
