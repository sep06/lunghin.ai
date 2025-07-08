import os

import pytest

from agents.exporter import gerar_relatorio_pdf


def test_gerar_relatorio_pdf(tmp_path):
    dados_ingestao = {"tipo_entrada": "pdf", "texto": "Contrato de exemplo"}
    grafo = {
        "entidades": [{"texto": "Empresa X", "label": "CONTRATANTE"}],
        "relacoes": [],
        "graph_id": "test123",
    }
    parecer_tecnico = {"clausulas_faltantes": [], "inconsistencias": [], "riscos": []}
    parecer_final = {
        "parecer_estruturado": "Parecer simples",
        "recomendacao": "Prosseguir",
        "status_final": "ok para prosseguir",
    }

    os.chdir(tmp_path)
    caminho = gerar_relatorio_pdf(dados_ingestao, grafo, parecer_tecnico, parecer_final)
    assert os.path.exists(caminho)
