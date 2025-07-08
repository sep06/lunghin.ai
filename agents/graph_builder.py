# coding: utf-8
"""Agent para construção de grafos cognitivos focados em contratos de prestação de serviços empresariais."""

from __future__ import annotations

import re
import uuid
from typing import Any, Dict, List

import spacy

# Armazena grafos simulados em memória
_GRAPHS: Dict[str, Dict[str, Any]] = {}


def extrair_entidades(texto: str) -> List[Dict[str, str]]:
    """Extrai entidades específicas de contratos de prestação de serviços empresariais."""

    nlp = spacy.load("pt_core_news_sm")
    doc = nlp(texto)

    entidades: set[tuple[str, str]] = set()

    def limpar(texto_raw: str) -> str:
        """Remove quebras de linha, espaços duplicados e normaliza maiúsculas."""
        return re.sub(r'\s+', ' ', texto_raw.strip()).upper()

    # Reconhecimento de entidades nomeadas (NER)
    for ent in doc.ents:
        texto_ent = limpar(ent.text)
        if len(texto_ent) <= 2:
            continue
        if ent.label_ == "ORG":
            entidades.add((texto_ent, "EMPRESA"))
        elif ent.label_ == "PERSON":
            entidades.add((texto_ent, "PESSOA"))

    # Regex patterns
    padroes = {
        "CNPJ": re.compile(r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b"),
        "DATA": re.compile(r"\b\d{1,2}/\d{1,2}/\d{4}\b"),
        "VALOR": re.compile(r"R\$\s?\d+(?:\.\d{3})*(?:,\d{2})?"),
        "PRAZO": re.compile(r"\b\d+\s*(DIAS|MESES|ANOS)\b", flags=re.I),
        "CONTRATANTE": re.compile(r"CONTRATANTE\s*:?[\s-]*([^\n]+)", re.I),
        "CONTRATADO": re.compile(r"CONTRATADO\s*:?[\s-]*([^\n]+)", re.I),
        "OBJETO": re.compile(r"OBJETO\s*:?[\s-]*([^\n]+)", re.I),
    }

    for label, padrao in padroes.items():
        for match in padroes[label].finditer(texto):
            valor = limpar(match.group(1) if match.groups() else match.group())
            if len(valor) > 2 and not valor.isdigit():
                entidades.add((valor, label))

    # Cláusulas importantes por palavras-chave
    clausulas = {
        "CONFIDENCIALIDADE": r"confidencialidade",
        "MULTA": r"\bmulta\b",
        "RESCISAO": r"rescis[ãa]o",
        "FORO": r"\bforo\b",
    }

    for label, pattern in clausulas.items():
        if re.search(pattern, texto, re.I):
            entidades.add((label, label))

    # Limpeza final
    entidades_limpa = []
    vistos = set()

    for texto_final, label_final in sorted(entidades):
        chave = (texto_final, label_final)
        if chave in vistos:
            continue
        # Filtros específicos
        if label_final == "OBJETO" and texto_final in ["SERVIÇOS", "OBJETO"]:
            continue
        if label_final == "VALOR" and not re.search(r"\d", texto_final):
            continue
        vistos.add(chave)
        entidades_limpa.append({"texto": texto_final, "label": label_final})

    return entidades_limpa


def gerar_relacoes(entidades: List[Dict[str, str]], texto: str) -> List[Dict[str, str]]:
    """Gera relações básicas entre as entidades extraídas."""

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
            "tipo": "cláusula",
        })

    if objeto and any(e["label"] == "CONFIDENCIALIDADE" for e in entidades):
        relacoes.append({
            "origem": "CONFIDENCIALIDADE",
            "destino": objeto,
            "tipo": "cláusula",
        })

    return relacoes


def criar_grafo(entidades: List[Dict[str, str]], relacoes: List[Dict[str, str]]) -> str:
    """Cria um grafo cognitivo simples em memória e retorna seu ID."""

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
