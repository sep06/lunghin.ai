# coding: utf-8
"""Executa diagnósticos LLM sobre cláusulas extraídas do grafo."""

from typing import List, Dict
from agents.interpretadores.diagnostico_llm import diagnosticar_clausula


def avaliar_clausulas_com_llm(entidades: List[Dict[str, str]]) -> List[Dict[str, any]]:
    """
    Recebe uma lista de entidades com cláusulas extraídas e retorna diagnósticos LLM
    sobre cada cláusula relevante (OBJETO, MULTA, RESCISAO, CONFIDENCIALIDADE, etc).
    """
    tipos_criticos = {"MULTA", "RESCISAO", "CONFIDENCIALIDADE", "PRAZO", "OBJETO"}
    resultados = []

    for entidade in entidades:
        tipo = entidade.get("label")
        texto = entidade.get("texto")

        if tipo in tipos_criticos:
            resultado = diagnosticar_clausula(clausula=texto, tipo=tipo)
            resultado.update({"tipo": tipo, "clausula": texto})
            resultados.append(resultado)

    return resultados


__all__ = ["avaliar_clausulas_com_llm"]
