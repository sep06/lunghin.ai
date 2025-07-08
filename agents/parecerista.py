# coding: utf-8
"""Agente parecerista do sistema juridico Lunghin.AI.

Este modulo recebe as entidades, relacoes e o parecer tecnico do revisor e
elabora um parecer textual completo e formal. O foco sao contratos de
prestacao de servicos empresariais.
"""

from __future__ import annotations

from typing import Dict, List


# ---------------------------------------------------------------------------
# Funcoes auxiliares
# ---------------------------------------------------------------------------

def gerar_parecer_estruturado(
    entidades: List[Dict[str, str]],
    relacoes: List[Dict[str, str]],
    parecer: Dict[str, List[str] | str],
) -> str:
    """Gera o texto do parecer a partir dos dados analisados."""

    linhas: List[str] = []
    linhas.append("Parecer Jurídico")
    linhas.append("=")

    if parecer.get("status") == "ok":
        linhas.append(
            "A análise do contrato de prestação de serviços empresariais não "
            "indicou ausência de cláusulas essenciais ou incoerências." 
        )
    else:
        clausulas_faltantes = parecer.get("clausulas_faltantes", [])
        inconsistencias = parecer.get("inconsistencias", [])

        if clausulas_faltantes:
            linhas.append(
                "Foram identificadas as seguintes cláusulas obrigatórias "
                "ausentes: " + ", ".join(clausulas_faltantes) + "."
            )
            linhas.append(
                "A inexistência destas disposições pode fragilizar a segurança "
                "jurídica do ajuste." 
            )
        if inconsistencias:
            linhas.append(
                "Inconsistências verificadas: " + "; ".join(inconsistencias) + "."
            )
    
        riscos = parecer.get("riscos", [])
        if riscos:
            linhas.append(
                "Principais riscos apurados: " + "; ".join(riscos) + "."
            )

    # Comentario final generico
    linhas.append(
        "Recomenda-se a revisão minuciosa do instrumento contratual para "
        "adequar as cláusulas à legislação aplicável e aos interesses das partes."
    )

    return "\n".join(linhas)


def gerar_recomendacao(parecer: Dict[str, List[str] | str]) -> str:
    """Define a recomendacao final com base nos achados."""

    if parecer.get("clausulas_faltantes") or parecer.get("inconsistencias"):
        return "Revisar e complementar as cláusulas faltantes antes da assinatura"
    return "Prosseguir com a formalização do contrato"


# ---------------------------------------------------------------------------
# Funcao principal do agente parecerista
# ---------------------------------------------------------------------------

def produzir_parecer(
    entidades: List[Dict[str, str]],
    relacoes: List[Dict[str, str]],
    parecer: Dict[str, List[str] | str],
) -> Dict[str, str]:
    """Produz o parecer jurídico final."""

    parecer_texto = gerar_parecer_estruturado(entidades, relacoes, parecer)
    recomendacao = gerar_recomendacao(parecer)
    status_final = (
        "revisão necessária"
        if parecer.get("clausulas_faltantes") or parecer.get("inconsistencias")
        else "ok para prosseguir"
    )

    return {
        "parecer_estruturado": parecer_texto,
        "recomendacao": recomendacao,
        "status_final": status_final,
    }


__all__ = [
    "gerar_parecer_estruturado",
    "gerar_recomendacao",
    "produzir_parecer",
]
