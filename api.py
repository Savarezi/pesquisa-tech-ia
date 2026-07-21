import json
import os
from flask import Flask, jsonify, request

app = Flask(__name__)

ARQUIVO_JSON = "respostas.json"


@app.route("/webhook", methods=["POST"])
def webhook():
  try:
    # Pega os dados enviados pelo Typebot
    dados_recebidos = request.get_json(silent=True)

    if not dados_recebidos:
      dados_recebidos = request.form.to_dict()

    if not dados_recebidos:
      return (
          jsonify(
              {"sucesso": False, "mensagem": "Nenhum dado foi enviado."}
          ),
          400,
      )

    # 1. Carrega o que já tem no arquivo JSON local
    lista_respostas = []
    if os.path.exists(ARQUIVO_JSON):
      try:
        with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
          conteudo = f.read().strip()
          if conteudo:
            lista_respostas = json.loads(conteudo)
            if not isinstance(lista_respostas, list):
              lista_respostas = [lista_respostas]
      except Exception:
        lista_respostas = []

    # 2. Adiciona a nova resposta que acabou de chegar
    lista_respostas.append(dados_recebidos)

    # 3. Salva de volta no arquivo respostas.json do Codespace
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
      json.dump(lista_respostas, f, ensure_ascii=False, indent=4)

    print("⚡ Novo dado salvo com sucesso localmente:", dados_recebidos)

    return (
        jsonify({
            "sucesso": True,
            "mensagem": "Salvo localmente com sucesso no dashboard!",
        }),
        200,
    )

  except Exception as e:
    print("❌ Erro:", str(e))
    return jsonify({"sucesso": False, "erro": str(e)}), 500


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)