"""Modulo de ingestao de documentos juridicos.

Este modulo identifica o tipo de arquivo (PDF escaneado, PDF editavel ou DOCX)
 e extrai o texto correspondente. Utiliza PyMuPDF para PDFs, PaddleOCR para
 PDFs escaneados e docx2txt para arquivos DOCX.
"""

from typing import Dict, Tuple

import fitz  # PyMuPDF
from paddleocr import PaddleOCR
import docx2txt
from PIL import Image
import numpy as np


def is_pdf_scanned(caminho_pdf: str) -> bool:
    """Verifica se um PDF possui texto extraivel.

    Retorna True se todas as paginas nao contiverem texto (PDF escaneado).
    """
    with fitz.open(caminho_pdf) as doc:
        for page in doc:
            if page.get_text().strip():
                return False
    return True


def _ocr_scanned_pdf(caminho_pdf: str) -> str:
    """Realiza OCR em um PDF escaneado usando PaddleOCR."""
    ocr = PaddleOCR(show_log=False)
    texto_paginas = []
    with fitz.open(caminho_pdf) as doc:
        for page in doc:
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            resultado = ocr.ocr(np.array(img), cls=False)
            if resultado:
                linhas = [linha[1][0] for linha in resultado[0]]
                texto_paginas.append("\n".join(linhas))
    return "\n".join(texto_paginas)


def _extrair_texto_pdf_editavel(caminho_pdf: str) -> str:
    """Extrai texto de PDF editavel usando PyMuPDF."""
    texto_paginas = []
    with fitz.open(caminho_pdf) as doc:
        for page in doc:
            texto_paginas.append(page.get_text("text"))
    return "\n".join(texto_paginas)


def extrair_texto_pdf(caminho_pdf: str) -> Tuple[str, str]:
    """Extrai texto de um arquivo PDF e indica o tipo de PDF."""
    if is_pdf_scanned(caminho_pdf):
        texto = _ocr_scanned_pdf(caminho_pdf)
        tipo = "pdf_escaneado"
    else:
        texto = _extrair_texto_pdf_editavel(caminho_pdf)
        tipo = "pdf_editavel"
    return texto, tipo


def extrair_texto_docx(caminho_docx: str) -> str:
    """Extrai texto de um arquivo DOCX."""
    return docx2txt.process(caminho_docx)


def processar_documento(caminho: str) -> Dict[str, str]:
    """Processa um documento juridico em PDF ou DOCX.

    Args:
        caminho: caminho do arquivo a ser processado.

    Returns:
        dict com chaves "texto" e "tipo_entrada".
    """
    caminho_lower = caminho.lower()
    if caminho_lower.endswith(".pdf"):
        texto, tipo = extrair_texto_pdf(caminho)
    elif caminho_lower.endswith(".docx"):
        texto = extrair_texto_docx(caminho)
        tipo = "docx"
    else:
        raise ValueError("Formato de arquivo nao suportado: %s" % caminho)

    return {"texto": texto.strip(), "tipo_entrada": tipo}

