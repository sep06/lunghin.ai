# coding: utf-8
"""Agente cognitivo que interpreta juridicamente cláusulas contratuais via LLM (GPT-4)."""

from typing import Dict, Any
import openai
import os
import json

# Simulador inicial: coloque sua chave real se for usar em produção
oai_key = os.getenv("OPENAI_API_KEY") or "sk-FAKE-KEY-FOR-DEBUG"

openai.api_key = oai_key


# Prompt base para avaliação jurídica de cláusulas
def gerar_prompt(tipo: str, clausula: str) -> str:
    return f"""
Você é um advogado especialista em contratos empresariais. Analise a seguinte cláusula extraída de um contrato de prestação de serviços:

Cláusula: {clausula}

Tipo de cláusula: {tipo}

Com base nisso, responda com um JSON contendo:
- \"presente\": se a cláusula está presente e reconhecível
- \"completude\": um número de 0 a 100 indicando o quanto a cláusula cobre os elementos esperados
- \"juridicamente_aceitavel\": true ou false, baseado na qualidade da redação e segurança jurídica
- \"comentario\": uma breve análise crítica da cláusula
- \"risco\": classificado como \"baixo\", \"médio\" ou \"alto\"

Responda apenas com JSON.
"""


def parsear_resposta(resposta: str) -> Dict[str, Any]:
    try:
        return json.loads(resposta.strip())
    except json.JSONDecodeError:
        return {"erro": "Resposta inválida do modelo", "raw": resposta}


def diagnosticar_clausula(clausula: str, tipo: str, contexto: Dict[str, Any] = None) -> Dict[str, Any]:
    prompt = gerar_prompt(tipo, clausula)

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um advogado contratualista experiente."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=500,
        )
        resposta = completion.choices[0].message.content
        return parsear_resposta(resposta)
    except Exception as e:
        return {"erro": str(e)}


__all__ = ["diagnosticar_clausula"]
