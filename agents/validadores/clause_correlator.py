# coding: utf-8
"""
Agente correlacionador de cláusulas jurídicas.

Detecta dependências obrigatórias e possíveis contradições entre cláusulas contratuais.
"""

from __future__ import annotations
from typing import List, Dict


# Mapa de dependência entre cláusulas
DEPENDENCIAS = {
    "MULTA": ["PRAZO"],
    "CONFIDENCIALIDADE": ["PENALIDADE", "MULTA"],
    "RESCISAO": ["OBJETO"],
    "PAGAMENTO": ["OBJETO", "PRAZO"]
}

# Regras que indicam contradições ou alertas se a dependência estiver ausente
def verificar_dependencias(clausulas_index: Dict[str, Dict]) -> List[str]:
    """
    Recebe um dicionário indexado por tipo de cláusula e retorna uma lista de alertas de correlação.
    """
    alertas = []

    for clausula, dependencias in DEPENDENCIAS.items():
        if clausula in clausulas_index:
            for dependente in dependencias:
                if dependente not in clausulas_index:
                    alertas.append(
                        f"A cláusula '{clausula}' exige a presença de '{dependente}', mas esta está ausente."
                    )

    return alertas
