# coding: utf-8
"""Agente exportador do sistema jurídico Lunghin.AI.

Gera relatório PDF estruturado com dados de entrada, entidades, relações,
parecer técnico e parecer final. Foco em contratos de prestação de serviços.
"""

from __future__ import annotations

import os
from typing import Dict, List
from fpdf import FPDF
from pathlib import Path

_DEFAULT_FONT = "Helvetica"
FONT_PATH = Path(__file__).resolve().parent.parent / "fonts" / "DejaVuSans.ttf"



def _criar_pasta_reports() -> None:
    os.makedirs("reports", exist_ok=True)


def _texto_resumido(texto: str, limite: int = 500) -> str:
    texto_limpo = texto.strip()
    return texto_limpo[:limite] + "..." if len(texto_limpo) > limite else texto_limpo


def _carregar_fonte(pdf: FPDF) -> str:
    """Tenta carregar a fonte customizada e retorna o nome da fonte usada."""
    try:
        font_path = FONT_PATH.as_posix()
        if os.path.exists(font_path):
            pdf.add_font("DejaVu", "", font_path, uni=True)
            return "DejaVu"
        else:
            raise FileNotFoundError(f"Fonte não encontrada em {font_path}")
    except Exception as exc:
        print(f"⚠️ Erro ao carregar fonte personalizada: {exc}")
        print("🟡 Usando fonte padrão Helvetica.")
        return _DEFAULT_FONT


def _adicionar_titulo(pdf: FPDF, fonte: str) -> None:
    pdf.set_font(fonte, "", 16)
    pdf.cell(0, 10, "Relatório de Análise Contratual", ln=1, align="C")
    pdf.ln(5)


def _adicionar_secao_dados(pdf: FPDF, dados_ingestao: Dict[str, str], fonte: str) -> None:
    pdf.set_font(fonte, "", 12)
    pdf.cell(0, 10, "Dados do Contrato", ln=1)
    pdf.multi_cell(0, 10, f"Tipo de entrada: {dados_ingestao.get('tipo_entrada')}")
    texto = _texto_resumido(dados_ingestao.get("texto", ""))
    pdf.multi_cell(0, 10, texto)
    pdf.ln(2)


def _adicionar_entidades_relacoes(pdf: FPDF, grafo: Dict[str, List[Dict[str, str]]], fonte: str) -> None:
    pdf.set_font(fonte, "", 12)
    pdf.cell(0, 10, "Entidades", ln=1)
    for ent in grafo.get("entidades", []):
        linha = f"{ent.get('label')}: {ent.get('texto')}"
        pdf.multi_cell(0, 8, linha)
    pdf.ln(2)

    pdf.cell(0, 10, "Relações", ln=1)
    for rel in grafo.get("relacoes", []):
        linha = f"{rel.get('origem')} -> {rel.get('destino')} ({rel.get('tipo')})"
        pdf.multi_cell(0, 8, linha)
    pdf.ln(2)


def _adicionar_parecer_tecnico(pdf: FPDF, parecer_tecnico: Dict[str, List[str]], fonte: str) -> None:
    pdf.set_font(fonte, "", 12)
    pdf.cell(0, 10, "Parecer Técnico", ln=1)

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


def _adicionar_parecer_final(pdf: FPDF, parecer_final: Dict[str, str], fonte: str) -> None:
    pdf.set_font(fonte, "", 12)
    pdf.cell(0, 10, "Parecer Final", ln=1)
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
    """Gera um relatório PDF consolidado e retorna o caminho salvo."""
    _criar_pasta_reports()
    pdf = FPDF()
    pdf.add_page()

    fonte = _carregar_fonte(pdf)

    try:
        _adicionar_titulo(pdf, fonte)
        _adicionar_secao_dados(pdf, dados_ingestao, fonte)
        _adicionar_entidades_relacoes(pdf, grafo, fonte)
        _adicionar_parecer_tecnico(pdf, parecer_tecnico, fonte)
        _adicionar_parecer_final(pdf, parecer_final, fonte)
    except Exception as exc:  # noqa: BLE001
        print(f"Erro ao gerar relatorio: {exc}")

    caminho = os.path.join("reports", f"relatorio_{grafo.get('graph_id')}.pdf")
    pdf.output(caminho)
    return caminho


__all__ = ["gerar_relatorio_pdf"]
