# coding: utf-8
"""Agente exportador do sistema jurídico Lunghin.AI.

Este módulo gera um relatório PDF estruturado a partir dos dados de
ingestão, do grafo de entidades e relações, do parecer técnico e do
parecer final. O foco é contrato de prestação de serviços empresariais.
"""

import os
from typing import Dict, List
from fpdf import FPDF


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
    """Adiciona o título principal do relatório."""
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Relatório de Análise Contratual", ln=1, align="C")
    pdf.ln(5)


def _adicionar_secao_dados(pdf: FPDF, dados_ingestao: Dict[str, str]) -> None:
    """Insere a seção de dados do contrato."""
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Dados do Contrato", ln=1)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"Tipo de entrada: {dados_ingestao.get('tipo_entrada')}")
    texto = _texto_resumido(dados_ingestao.get("texto", ""))
    pdf.multi_cell(0, 10, texto)
    pdf.ln(2)


def _adicionar_entidades_relacoes(pdf: FPDF, grafo: Dict[str, List[Dict[str, str]]]) -> None:
    """Adiciona as entidades e relações em formato simples de tabela."""
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Entidades", ln=1)
    pdf.set_font("Arial", size=12)
    for ent in grafo.get("entidades", []):
        linha = f"{ent.get('label')}: {ent.get('texto')}"
        pdf.multi_cell(0, 8, linha)
    pdf.ln(2)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Relações", ln=1)
    pdf.set_font("Arial", size=12)
    for rel in grafo.get("relacoes", []):
        linha = f"{rel.get('origem')} -> {rel.get('destino')} ({rel.get('tipo')})"
        pdf.multi_cell(0, 8, linha)
    pdf.ln(2)


def _adicionar_parecer_tecnico(pdf: FPDF, parecer_tecnico: Dict[str, List[str]]) -> None:
    """Insere as informações do parecer técnico em bullets."""
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Parecer Técnico", ln=1)
    pdf.set_font("Arial", size=12)

    clausulas = parecer_tecnico.get("clausulas_faltantes", [])
    if clausulas:
        pdf.multi_cell(0, 8, "Cláusulas faltantes: " + ", ".join(clausulas))

    inconsistencias = parecer_tecnico.get("inconsistencias", [])
    if inconsistencias:
        pdf.multi_cell(0, 8, "Inconsistências: " + ", ".join(inconsistencias))

    riscos = parecer_tecnico.get("riscos", [])
    if riscos:
        pdf.multi_cell(0, 8, "Riscos: " + "; ".join(riscos))
    pdf.ln(2)


def _adicionar_parecer_final(pdf: FPDF, parecer_final: Dict[str, str]) -> None:
    """Adiciona o parecer jurídico final e a recomendação."""
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Parecer Final", ln=1)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 8, parecer_final.get("parecer_estruturado", ""))
    pdf.ln(2)
    pdf.multi_cell(0, 8, "Recomendação: " + parecer_final.get("recomendacao", ""))
    pdf.multi_cell(0, 8, "Status: " + parecer_final.get("status_final", ""))
    pdf.ln(2)


def gerar_relatorio_pdf(
    dados_ingestao: Dict[str, str],
    grafo: Dict[str, List[Dict[str, str]]],
    parecer_tecnico: Dict[str, List[str]],
    parecer_final: Dict[str, str],
) -> str:
    """Gera um relatório PDF consolidando todas as informações.
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
