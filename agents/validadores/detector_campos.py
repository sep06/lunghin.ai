import re
from typing import List

def detectar_campos_em_branco(texto: str) -> List[str]:
    """
    Detecta campos típicos não preenchidos em contratos.
    Retorna lista de ocorrências como placeholders, campos rasurados, tracinhos ou marcadores.
    """
    padroes = [
        r"___+",                          # Tracinhos
        r"X{3,}",                         # Placeholder tipo XXX
        r"\( ?[Xx] ?\)",                  # Opções em aberto (checkbox)
        r"\[MNg\d+\]",                    # Comentários internos como [MNg2]
        r"[A-Z ]{3,}[:：] ?_+",           # Campos do tipo "NOME: ____"
        r"\bFORO\b.*_+",                  # Cláusula de foro em branco
        r"R\$ ?_+",                       # Valores não definidos
    ]
    encontrados = []
    for padrao in padroes:
        encontrados.extend(re.findall(padrao, texto))
    return encontrados
