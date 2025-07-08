# coding: utf-8
"""Agente parecerista do sistema jurídico Lunghin.AI.

Este módulo recebe as entidades, relações e o parecer técnico do revisor e
elabora um parecer textual completo e formal. O foco são contratos de
prestação de serviços empresariais.
"""

from typing import Dict, List


# ---------------------------------------------------------------------------
# Funções auxiliares
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

    # Comentário final genérico
    linhas.append(
        "Recomenda-se a revisão minuciosa do instrumento contratual para "
        "adequar as cláusulas à legislação aplicável e aos interesses das partes."
    )

    return "\n".join(linhas)


def gerar_recomendacao(parecer: Dict[str, List[str] | str]) -> str:
    """Define a recomendação final com base nos achados."""

    if parecer.get("clausulas_faltantes") or parecer.get("inconsistencias"):
        return "Revisar e complementar as cláusulas faltantes antes da assinatura"
    return "Prosseguir com a formalização do contrato"


# ---------------------------------------------------------------------------
# Função principal do agente parecerista
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
