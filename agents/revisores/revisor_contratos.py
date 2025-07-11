# coding: utf-8
"""
Agente revisor de contratos de prestação de serviços empresariais (v1.1).

Este módulo utiliza a nova arquitetura com extração inteligente de cláusulas,
pontuação de risco, e validação de coerência jurídica.
"""

from __future__ import annotations

from typing import Dict, List
from agents.pareceristas.lawlinker import justificar_clausula
from agents.validadores.clause_correlator import verificar_dependencias
from agents.interpretadores.extrator_clausulas import (
    segmentar_por_regex,
    classificar_clausulas,
)
from agents.pareceristas.clause_scorer import pontuar_clausula
# from agents.validadores.clause_correlator import verificar_dependencias

# Cláusulas consideradas obrigatórias para um contrato de prestação de serviços
MANDATORY_CLAUSES = [
    "OBJETO",
    "PRAZO",
    "PAGAMENTO",
    "MULTA",
    "FORO",
    "RESCISAO",
    "CONFIDENCIALIDADE",
]


def revisar_contrato(texto_contrato: str) -> Dict:
    """
    Realiza a revisão completa do contrato textual:
    - Extrai cláusulas
    - Classifica tipos
    - Identifica faltantes
    - Aponta riscos e inconsistências com pontuação simbólica
    """

    # Etapa 1: Segmentar e classificar cláusulas
    blocos = segmentar_por_regex(texto_contrato)
    clausulas = classificar_clausulas(blocos)
    clausulas_index = {c["tipo_clausula"]: c for c in clausulas}

    # Etapa 2: Verificar cláusulas obrigatórias ausentes
    faltantes = [cl for cl in MANDATORY_CLAUSES if cl not in clausulas_index]

    # Etapa 3: Pontuar cada cláusula e vincular justificativa legal
    parecer_por_clausula = []
    for clausula in clausulas:
        tipo = clausula["tipo_clausula"]
        conteudo = clausula["conteudo"]

        pontuacao = pontuar_clausula(conteudo, tipo)
        base_legal = justificar_clausula(tipo)

        parecer_por_clausula.append(
            {
                "tipo": tipo,
                "risco": pontuacao["risco"],
                "qualidade": pontuacao["qualidade"],
                "justificativa": pontuacao["justificativa"],
                "base_legal": base_legal["justificativa"],
                "fonte": base_legal["fonte"],
            }
        )

    # Etapa 4: (futura) Correlação jurídica entre cláusulas
    correlacoes = verificar_dependencias(clausulas_index)  # verificar_dependencias(clausulas_index)

    # Etapa 5: Compilar parecer
    return {
        "clausulas_detectadas": [c["tipo_clausula"] for c in clausulas],
        "clausulas_faltantes": faltantes,
        "parecer_clausulas": parecer_por_clausula,
        "correlacoes": correlacoes,
        "status": "atencao" if faltantes else "ok",
    }


__all__ = ["revisar_contrato"]
