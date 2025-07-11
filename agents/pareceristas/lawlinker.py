# coding: utf-8
"""
Agente justificativo legal: fornece base normativa para cláusulas contratuais específicas.

Versão inicial com mapeamento manual. Futuro: integração com RAG jurídico.
"""

from __future__ import annotations
from typing import Dict


BASE_JURIDICA = {
    "OBJETO": {
        "justificativa": "Todo contrato deve conter objeto claro e determinado. Ausência compromete a validade do negócio jurídico.",
        "fonte": "Código Civil, art. 104, I"
    },
    "PRAZO": {
        "justificativa": "É essencial estabelecer vigência contratual para caracterizar obrigações no tempo.",
        "fonte": "Código Civil, art. 421-A, §1º"
    },
    "PAGAMENTO": {
        "justificativa": "A contraprestação deve ser definida para caracterizar sinalagmática. Omissão pode gerar nulidade.",
        "fonte": "Código Civil, art. 319"
    },
    "MULTA": {
        "justificativa": "A multa contratual funciona como cláusula penal e deve seguir limites de razoabilidade.",
        "fonte": "Código Civil, art. 408"
    },
    "FORO": {
        "justificativa": "Definir o foro competente previne conflitos de jurisdição em caso de litígio.",
        "fonte": "CPC, art. 63"
    },
    "RESCISAO": {
        "justificativa": "Deve haver previsão de rescisão contratual unilateral e bilateral com aviso prévio.",
        "fonte": "CLT, art. 473, II / Código Civil, art. 473"
    },
    "CONFIDENCIALIDADE": {
        "justificativa": "Proteção de informações sensíveis é obrigatória em relações com acesso a dados sigilosos.",
        "fonte": "LGPD, art. 6º, I / Código Civil, art. 422"
    }
}


def justificar_clausula(tipo_clausula: str) -> Dict:
    """
    Retorna uma justificativa jurídica padrão para o tipo de cláusula fornecido.
    """
    base = BASE_JURIDICA.get(tipo_clausula.upper(), None)
    if base:
        return {
            "justificativa": base["justificativa"],
            "fonte": base["fonte"]
        }
    return {
        "justificativa": "Nenhuma base legal mapeada para esta cláusula.",
        "fonte": "Desconhecida"
    }
