import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import json
from pathlib import Path
from crew.juriscrew import run_pipeline

def processar_em_lote(pasta_entrada: str, pasta_saida: str) -> None:
    contratos = list(Path(pasta_entrada).glob("*.pdf"))

    if not contratos:
        print("⚠️ Nenhum arquivo PDF encontrado na pasta de entrada.")
        return

    for contrato_path in contratos:
        nome = contrato_path.stem
        print(f"\n📄 Processando: {nome}")

        try:
            resultado = run_pipeline(contrato_path.as_posix())

            # Criar pasta de saída individual para o contrato
            pasta_saida_individual = Path(pasta_saida) / nome
            pasta_saida_individual.mkdir(parents=True, exist_ok=True)
            print(f"📁 Pasta criada: {pasta_saida_individual}")

            # Copiar PDF final
            pdf_path = Path(resultado["relatorio_pdf"])
            if pdf_path.exists():
                destino_pdf = pasta_saida_individual / "relatorio.pdf"
                destino_pdf.write_bytes(pdf_path.read_bytes())

            # Salvar JSON com parecer final
            with open(pasta_saida_individual / "parecer.json", "w", encoding="utf-8") as f:
                json.dump(resultado["parecer_final"], f, indent=2, ensure_ascii=False)

            # Salvar entidades + relações
            with open(pasta_saida_individual / "entidades.json", "w", encoding="utf-8") as f:
                json.dump({
                    "entidades": resultado["entidades"],
                    "relacoes": resultado["relacoes"]
                }, f, indent=2, ensure_ascii=False)

            # Salvar campos em branco detectados
            with open(pasta_saida_individual / "campos_em_branco.json", "w", encoding="utf-8") as f:
                json.dump(resultado["campos_em_branco"], f, indent=2, ensure_ascii=False)

            print(f"✅ {nome} processado com sucesso.")

        except Exception as e:
            print(f"❌ Erro ao processar {nome}: {e}")


if __name__ == "__main__":
    pasta_entrada = "contratos_teste"
    pasta_saida = "outputs"
    processar_em_lote(pasta_entrada, pasta_saida)
