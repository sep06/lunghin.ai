# coding: utf-8
"""
Agente parecerista que pontua cláusulas contratuais com base em risco e qualidade.

Este módulo deve ser substituído futuramente por um modelo LLM ou motor simbólico.
"""

from __future__ import annotations
from typing import Dict


def pontuar_clausula(conteudo: str, tipo: str) -> Dict:
    """
    Retorna dicionário com:
    - risco (0-10)
    - qualidade (0-10)
    - justificativa jurídica simbólica ou textual
    """
    conteudo_lower = conteudo.lower()
    risco = 3
    qualidade = 8
    justificativa = "Cláusula adequada."

    if tipo == "OBJETO":
        if "prestação de serviços" in conteudo_lower or "serviços de" in conteudo_lower:
            qualidade = 9
        else:
            qualidade = 5
            risco = 7
            justificativa = "Cláusula vaga ou sem descrição clara dos serviços."

    elif tipo == "PRAZO":
        if "vigência" in conteudo_lower or "prazo de" in conteudo_lower:
            if "início" in conteudo_lower and "término" in conteudo_lower:
                qualidade = 9
            else:
                qualidade = 6
                risco = 6
                justificativa = "Cláusula sem definição clara de início e término."
        else:
            risco = 8
            qualidade = 5
            justificativa = "Cláusula sem referência direta a duração ou vigência."

    elif tipo == "MULTA":
        if "percentual" in conteudo_lower or "%" in conteudo_lower:
            qualidade = 8
        else:
            risco = 6
            qualidade = 5
            justificativa = "Cláusula de multa sem valor definido pode gerar insegurança jurídica."

    elif tipo == "CONFIDENCIALIDADE":
        if "sigilo" in conteudo_lower or "informações confidenciais" in conteudo_lower:
            qualidade = 8
        else:
            risco = 7
            justificativa = "Falta menção clara a dever de sigilo e escopo das informações protegidas."

    elif tipo == "FORO":
        if "comarca" in conteudo_lower:
            qualidade = 9
        else:
            risco = 6
            justificativa = "Foro não definido corretamente prejudica resolução de disputas."

    elif tipo == "RESCISAO":
        if "aviso prévio" in conteudo_lower:
            qualidade = 8
        else:
            risco = 7
            justificativa = "Ausência de condições claras para rescisão contratual."

    return {
        "risco": risco,
        "qualidade": qualidade,
        "justificativa": justificativa
    }
