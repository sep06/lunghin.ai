# coding: utf-8
"""Agent para construcao de grafos cognitivos focados em contratos de
prestacao de servicos empresariais."""

from __future__ import annotations

import re
import uuid
from typing import Any, Dict, List

import spacy

# Armazena grafos simulados em memoria
_GRAPHS: Dict[str, Dict[str, Any]] = {}


def extrair_entidades(texto: str) -> List[Dict[str, str]]:
    """Extrai entidades especificas de contratos de servicos empresariais."""

    nlp = spacy.load("pt_core_news_sm")
    doc = nlp(texto)

    entidades: set[tuple[str, str]] = set()

    # Reconhece pessoas e empresas
    for ent in doc.ents:
        if ent.label_ == "ORG":
            entidades.add((ent.text.strip(), "EMPRESA"))
        elif ent.label_ == "PERSON":
            entidades.add((ent.text.strip(), "PESSOA"))

    # Padroes regex para campos do contrato
    padrao_cnpj = re.compile(r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b")
    padrao_data = re.compile(r"\b\d{1,2}/\d{1,2}/\d{4}\b")
    padrao_valor = re.compile(r"R\$\s?\d+(?:\.\d{3})*(?:,\d{2})?")
    padrao_prazo = re.compile(r"\b\d+\s*(dias|meses|anos)\b", flags=re.I)
    padrao_contratante = re.compile(r"CONTRATANTE\s*:?[\s-]*([^\n]+)", re.I)
    padrao_contratado = re.compile(r"CONTRATADO\s*:?[\s-]*([^\n]+)", re.I)
    padrao_objeto = re.compile(r"OBJETO\s*:?[\s-]*([^\n]+)", re.I)

    for match in padrao_contratante.finditer(texto):
        entidades.add((match.group(1).strip(), "CONTRATANTE"))
    for match in padrao_contratado.finditer(texto):
        entidades.add((match.group(1).strip(), "CONTRATADO"))
    for match in padrao_objeto.finditer(texto):
        entidades.add((match.group(1).strip(), "OBJETO"))

    for cnpj in padrao_cnpj.findall(texto):
        entidades.add((cnpj, "CNPJ"))
    for valor in padrao_valor.findall(texto):
        entidades.add((valor, "VALOR"))
    for data in padrao_data.findall(texto):
        entidades.add((data, "DATA"))
    for prazo in padrao_prazo.findall(texto):
        entidades.add((prazo, "PRAZO"))

    if re.search(r"confidencialidade", texto, re.I):
        entidades.add(("CONFIDENCIALIDADE", "CONFIDENCIALIDADE"))
    if re.search(r"multa", texto, re.I):
        entidades.add(("MULTA", "MULTA"))
    if re.search(r"rescis[ãa]o", texto, re.I):
        entidades.add(("RESCISAO", "RESCISAO"))
    if re.search(r"foro", texto, re.I):
        entidades.add(("FORO", "FORO"))

    return [{"texto": t, "label": l} for t, l in sorted(entidades)]


def gerar_relacoes(entidades: List[Dict[str, str]], texto: str) -> List[Dict[str, str]]:
    """Gera relacoes basicas entre as entidades extraidas."""

    relacoes: List[Dict[str, str]] = []

    contratante = next((e["texto"] for e in entidades if e["label"] == "CONTRATANTE"), None)
    contratado = next((e["texto"] for e in entidades if e["label"] == "CONTRATADO"), None)
    valor = next((e["texto"] for e in entidades if e["label"] == "VALOR"), None)
    objeto = next((e["texto"] for e in entidades if e["label"] == "OBJETO"), None)
    prazo = next((e["texto"] for e in entidades if e["label"] == "PRAZO"), None)

    if contratante and contratado and valor:
        relacoes.append({
            "origem": contratante,
            "destino": contratado,
            "tipo": "pagamento",
            "valor": valor,
        })

    if objeto and prazo:
        relacoes.append({
            "origem": prazo,
            "destino": objeto,
            "tipo": "prazo_objeto",
        })

    if objeto and any(e["label"] == "MULTA" for e in entidades):
        relacoes.append({
            "origem": "MULTA",
            "destino": objeto,
            "tipo": "clausula",
        })

    if objeto and any(e["label"] == "CONFIDENCIALIDADE" for e in entidades):
        relacoes.append({
            "origem": "CONFIDENCIALIDADE",
            "destino": objeto,
            "tipo": "clausula",
        })

    return relacoes


def criar_grafo(entidades: List[Dict[str, str]], relacoes: List[Dict[str, str]]) -> str:
    """Cria um grafo cognitivo simples em memoria e retorna seu ID."""

    graph_id = str(uuid.uuid4())
    _GRAPHS[graph_id] = {"entidades": entidades, "relacoes": relacoes}
    return graph_id


def construir_grafo(texto: str) -> Dict[str, Any]:
    """Processa o texto e monta o grafo de conhecimento."""

    entidades = extrair_entidades(texto)
    relacoes = gerar_relacoes(entidades, texto)
    graph_id = criar_grafo(entidades, relacoes)
    return {"entidades": entidades, "relacoes": relacoes, "graph_id": graph_id}


__all__ = [
    "extrair_entidades",
    "gerar_relacoes",
    "criar_grafo",
    "construir_grafo",
]
