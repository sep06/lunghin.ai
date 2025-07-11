# agents/interpretadores/extrator_clausulas.py

import re
from typing import List, Dict


def segmentar_por_regex(texto: str) -> List[Dict]:
    """
    Segmenta o texto do contrato em blocos com base em títulos padrão de cláusulas.
    Usa regex para encontrar seções que começam com 'CLÁUSULA' seguida de qualquer texto.
    """
    padrao = r"(CLÁUSULA\s+[A-Zªº\d\w\s\-\.]+)(.*?)(?=CLÁUSULA\s+[A-Zªº\d\w\s\-\.]+|\Z)"
    matches = re.finditer(padrao, texto, re.IGNORECASE | re.DOTALL)

    blocos = []
    for m in matches:
        titulo = m.group(1).strip().replace("\n", " ")
        conteudo = m.group(2).strip()
        blocos.append({
            "titulo_original": titulo,
            "conteudo": conteudo
        })
    return blocos


def classificar_clausulas(blocos: List[Dict]) -> List[Dict]:
    """
    Classifica cada bloco segmentado em um tipo jurídico básico, com heurística + fallback.
    """
    resultado = []
    for bloco in blocos:
        texto = bloco["titulo_original"] + " " + bloco["conteudo"]
        tipo = classificar_tipo_clausula(texto)
        resultado.append({
            "tipo_clausula": tipo,
            "titulo_original": bloco["titulo_original"],
            "conteudo": bloco["conteudo"],
            "confianca": 0.90 if tipo != "OUTROS" else 0.65
        })
    return resultado


def classificar_tipo_clausula(texto: str) -> str:
    """
    Classifica o tipo da cláusula com base em palavras-chave. Pode ser substituído por LLM.
    """
    texto_lower = texto.lower()

    if "objeto" in texto_lower or "escopo" in texto_lower:
        return "OBJETO"
    if "prazo" in texto_lower or "vigência" in texto_lower:
        return "PRAZO"
    if "pagamento" in texto_lower or "remuneração" in texto_lower or "preço" in texto_lower:
        return "PAGAMENTO"
    if "multa" in texto_lower or "penalidade" in texto_lower:
        return "MULTA"
    if "rescisão" in texto_lower or "rescindir" in texto_lower:
        return "RESCISAO"
    if "foro" in texto_lower:
        return "FORO"
    if "sigilo" in texto_lower or "confidencialidade" in texto_lower:
        return "CONFIDENCIALIDADE"
    if "obrigações do contratado" in texto_lower:
        return "OBRIGACOES_CONTRATADO"
    if "obrigações do contratante" in texto_lower:
        return "OBRIGACOES_CONTRATANTE"
    if "disposições gerais" in texto_lower:
        return "DISPOSICOES_GERAIS"

    return "OUTROS"
