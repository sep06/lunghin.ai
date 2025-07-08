# coding: utf-8
"""Agente exportador do sistema juridico Lunghin.AI.

Este modulo gera um relatorio PDF estruturado a partir dos dados de
ingestao, do grafo de entidades e relacoes, do parecer tecnico e do
parecer final. O foco eh contrato de prestacao de servicos empresariais.
"""

from __future__ import annotations

import os
from typing import Dict, List

# A biblioteca externa usada para gerar o PDF
from fpdf import FPDF


# ---------------------------------------------------------------------------
# Funcoes auxiliares de geracao do PDF
# ---------------------------------------------------------------------------

def _criar_pasta_reports() -> None:
    """Garante que a pasta reports/ exista."""

    os.makedirs("reports", exist_ok=True)


def _texto_resumido(texto: str, limite: int = 500) -> str:
    """Resumo simples do texto para inserir no PDF."""

    texto_limpo = texto.strip()
    if len(texto_limpo) > limite:
        return texto_limpo[:limite] + "..."
    return texto_limpo


def _adicionar_titulo(pdf: FPDF) -> None:
    """Adiciona o titulo principal do relatorio."""

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Relat\xf3rio de An\xe1lise Contratual", ln=1, align="C")
    pdf.ln(5)


def _adicionar_secao_dados(pdf: FPDF, dados_ingestao: Dict[str, str]) -> None:
    """Insere a secao de dados do contrato."""

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Dados do Contrato", ln=1)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"Tipo de entrada: {dados_ingestao.get('tipo_entrada')}")
    texto = _texto_resumido(dados_ingestao.get("texto", ""))
    pdf.multi_cell(0, 10, texto)
    pdf.ln(2)


def _adicionar_entidades_relacoes(pdf: FPDF, grafo: Dict[str, List[Dict[str, str]]]) -> None:
    """Adiciona as entidades e relacoes em formato simples de tabela."""

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Entidades", ln=1)
    pdf.set_font("Arial", size=12)
    for ent in grafo.get("entidades", []):
        linha = f"{ent.get('label')}: {ent.get('texto')}"
        pdf.multi_cell(0, 8, linha)
    pdf.ln(2)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Rela\xe7\xf5es", ln=1)
    pdf.set_font("Arial", size=12)
    for rel in grafo.get("relacoes", []):
        linha = f"{rel.get('origem')} -> {rel.get('destino')} ({rel.get('tipo')})"
        pdf.multi_cell(0, 8, linha)
    pdf.ln(2)


def _adicionar_parecer_tecnico(pdf: FPDF, parecer_tecnico: Dict[str, List[str]]) -> None:
    """Insere as informacoes do parecer tecnico em bullets."""

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Parecer T\xe9cnico", ln=1)
    pdf.set_font("Arial", size=12)

    clausulas = parecer_tecnico.get("clausulas_faltantes", [])
    if clausulas:
        pdf.multi_cell(0, 8, "Cl\xe1usulas faltantes: " + ", ".join(clausulas))

    inconsistencias = parecer_tecnico.get("inconsistencias", [])
    if inconsistencias:
        pdf.multi_cell(0, 8, "Inconsist\xeancias: " + ", ".join(inconsistencias))

    riscos = parecer_tecnico.get("riscos", [])
    if riscos:
        pdf.multi_cell(0, 8, "Riscos: " + "; ".join(riscos))
    pdf.ln(2)


def _adicionar_parecer_final(pdf: FPDF, parecer_final: Dict[str, str]) -> None:
    """Adiciona o parecer juridico final e a recomendacao."""

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Parecer Final", ln=1)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 8, parecer_final.get("parecer_estruturado", ""))
    pdf.ln(2)
    pdf.multi_cell(0, 8, "Recomenda\xe7\xe3o: " + parecer_final.get("recomendacao", ""))
    pdf.multi_cell(0, 8, "Status: " + parecer_final.get("status_final", ""))
    pdf.ln(2)


def gerar_relatorio_pdf(
    dados_ingestao: Dict[str, str],
    grafo: Dict[str, List[Dict[str, str]]],
    parecer_tecnico: Dict[str, List[str]],
    parecer_final: Dict[str, str],
) -> str:
    """Gera um relatorio PDF consolidando todas as informacoes.

    Retorna o caminho do arquivo gerado.
    """

    _criar_pasta_reports()

    pdf = FPDF()
    pdf.add_page()

    _adicionar_titulo(pdf)
    _adicionar_secao_dados(pdf, dados_ingestao)
    _adicionar_entidades_relacoes(pdf, grafo)
    _adicionar_parecer_tecnico(pdf, parecer_tecnico)
    _adicionar_parecer_final(pdf, parecer_final)

    caminho = os.path.join("reports", f"relatorio_{grafo.get('graph_id')}.pdf")
    pdf.output(caminho)
    return caminho


__all__ = ["gerar_relatorio_pdf"]
