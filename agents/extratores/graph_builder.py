# coding: utf-8
"""
Módulo refatorado de extração e construção de grafo jurídico.
Foco em contratos de prestação de serviços empresariais.
"""

import re
import uuid
from typing import Any, Dict, List
import spacy

_GRAPHS: Dict[str, Dict[str, Any]] = {}

MAPEAMENTO_TIPOS = {
    "OBJETO": ["objeto", "escopo", "atividade"],
    "PRAZO": ["prazo", "vigência", "período"],
    "MULTA": ["multa", "penalidade", "sanção"],
    "FORO": ["foro", "jurisdição", "competência"],
    "RESCISAO": ["rescisão", "rompimento"],
    "LGPD": ["lgpd", "proteção de dados", "lei 13.709"],
}


def segmentar_clausulas(texto: str) -> List[Dict[str, str]]:
    padrao = re.compile(r'(CL[ÁA]USULA.*?)(?=CL[ÁA]USULA|DO\s|DA\s|\Z)', re.IGNORECASE | re.DOTALL)
    matches = padrao.findall(texto)

    secoes = []
    for trecho in matches:
        trecho_limpo = trecho.strip()
        titulo = trecho_limpo.split("\n")[0][:100]
        label_detectado = "OUTRA"
        for label, palavras in MAPEAMENTO_TIPOS.items():
            if any(p in trecho_limpo.lower() for p in palavras):
                label_detectado = label
                break
        secoes.append({
            "titulo": titulo,
            "texto": trecho_limpo,
            "label": label_detectado
        })

    return secoes



def extrair_entidades(texto: str) -> List[Dict[str, str]]:
    nlp = spacy.load("pt_core_news_sm")
    doc = nlp(texto)
    entidades: List[Dict[str, str]] = []

    def limpar(txt):
        return re.sub(r'\s+', ' ', txt.strip()).upper()

    # NER básico
    for ent in doc.ents:
        texto_ent = limpar(ent.text)
        if len(texto_ent) <= 2:
            continue
        if ent.label_ == "ORG":
            entidades.append({"texto": texto_ent, "label": "EMPRESA"})
        elif ent.label_ == "PERSON":
            entidades.append({"texto": texto_ent, "label": "PESSOA"})

    # Regex padrão
    padroes_regex = {
        "CNPJ": re.compile(r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b"),
        "DATA": re.compile(r"\b\d{1,2}/\d{1,2}/\d{4}\b"),
        "VALOR": re.compile(r"R\$\s?\d+(?:\.\d{3})*(?:,\d{2})?"),
        "PRAZO": re.compile(r"\b\d+\s*(DIAS|MESES|ANOS)\b", re.I),
    }
    for label, padrao in padroes_regex.items():
        for m in padrao.findall(texto):
            entidades.append({"texto": limpar(m), "label": label})

    # Cláusulas segmentadas
    secoes = segmentar_clausulas(texto)
    for s in secoes:
        if s["label"] != "OUTRA":
            entidades.append({"texto": s["texto"][:300], "label": s["label"]})

    return entidades


def gerar_relacoes(entidades: List[Dict[str, str]], texto: str) -> List[Dict[str, str]]:
    relacoes = []
    contratante = next((e["texto"] for e in entidades if e["label"] == "CONTRATANTE"), None)
    contratado = next((e["texto"] for e in entidades if e["label"] == "CONTRATADO"), None)
    valor = next((e["texto"] for e in entidades if e["label"] == "VALOR"), None)
    prazo = next((e["texto"] for e in entidades if e["label"] == "PRAZO"), None)

    if contratante and contratado and valor:
        relacoes.append({"origem": contratante, "destino": contratado, "tipo": "remunera", "valor": valor})

    if contratado and prazo:
        relacoes.append({"origem": contratado, "destino": prazo, "tipo": "prazo_execucao"})

    return relacoes


def criar_grafo(entidades: List[Dict[str, str]], relacoes: List[Dict[str, str]]) -> str:
    graph_id = str(uuid.uuid4())
    _GRAPHS[graph_id] = {"entidades": entidades, "relacoes": relacoes}
    return graph_id


def construir_grafo(texto: str) -> Dict[str, Any]:
    entidades = extrair_entidades(texto)
    relacoes = gerar_relacoes(entidades, texto)
    graph_id = criar_grafo(entidades, relacoes)
    return {"entidades": entidades, "relacoes": relacoes, "graph_id": graph_id}


__all__ = ["segmentar_clausulas", "extrair_entidades", "gerar_relacoes", "criar_grafo", "construir_grafo"]
