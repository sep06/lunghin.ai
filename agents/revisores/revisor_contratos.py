# coding: utf-8
"""Agente revisor de contratos de prestacao de servicos empresariais.

Este modulo analisa as entidades e relacoes extraidas do contrato para
identificar clausulas obrigatorias ausentes, inconsistencias e possiveis
riscos juridicos. A ideia e simular a atuacao de um advogado revisor de
forma automatizada.
"""

from __future__ import annotations

from typing import Dict, List
import re

MANDATORY_CLAUSES = [
    "OBJETO",
    "PRAZO",
    "VALOR",
    "MULTA",
    "FORO",
    "RESCISAO",
    "CONFIDENCIALIDADE",
]


def verificar_clausulas_obrigatorias(entidades: List[Dict[str, str]]) -> List[str]:
    """Retorna a lista de clausulas obrigatorias ausentes, com fallback semantico para PRAZO."""

    labels = {e.get("label") for e in entidades}
    texto_completo = " ".join(e["texto"] for e in entidades)

    # Fallback para identificar "PRAZO" com base em menções a "vigência"
    if "PRAZO" not in labels:
        if re.search(r"\bvig[êe]ncia\b", texto_completo, re.I) or re.search(r"prazo indeterminado", texto_completo, re.I):
            labels.add("PRAZO")

    return [cl for cl in MANDATORY_CLAUSES if cl not in labels]


def detectar_inconsistencias(
    entidades: List[Dict[str, str]], relacoes: List[Dict[str, str]]
) -> List[str]:
    """Detecta incoerencias basicas entre as entidades e relacoes."""

    labels = {e.get("label") for e in entidades}
    inconsistencias: List[str] = []

    if "VALOR" in labels and ("CONTRATANTE" not in labels or "CONTRATADO" not in labels):
        inconsistencias.append(
            "VALOR presente sem especificacao de CONTRATANTE ou CONTRATADO"
        )

    if "PRAZO" in labels and "OBJETO" not in labels:
        inconsistencias.append("PRAZO estabelecido sem definir o OBJETO do contrato")

    if "MULTA" not in labels and any(r.get("tipo") == "pagamento" for r in relacoes):
        inconsistencias.append(
            "Nao ha clausula de MULTA mesmo existindo obrigacao de pagamento"
        )

    return inconsistencias


def avaliar_riscos_juridicos(
    clausulas_faltantes: List[str], inconsistencias: List[str]
) -> List[str]:
    """Gera observacoes de risco a partir das falhas detectadas."""

    riscos: List[str] = []
    for clausula in clausulas_faltantes:
        riscos.append(
            f"Ausencia da clausula {clausula} pode comprometer a seguranca juridica"
        )
    for inc in inconsistencias:
        riscos.append(f"Inconsistencia detectada: {inc}")
    return riscos


def revisar_contrato(
    entidades: List[Dict[str, str]], relacoes: List[Dict[str, str]]
) -> Dict[str, List[str] | str]:
    """Executa todas as analises e retorna o parecer sintetico."""

    clausulas_faltantes = verificar_clausulas_obrigatorias(entidades)
    inconsistencias = detectar_inconsistencias(entidades, relacoes)
    riscos = avaliar_riscos_juridicos(clausulas_faltantes, inconsistencias)
    status = "ok" if not clausulas_faltantes and not inconsistencias else "atencao"

    return {
        "clausulas_faltantes": clausulas_faltantes,
        "inconsistencias": inconsistencias,
        "riscos": riscos,
        "status": status,
    }


__all__ = [
    "verificar_clausulas_obrigatorias",
    "detectar_inconsistencias",
    "avaliar_riscos_juridicos",
    "revisar_contrato",
]
