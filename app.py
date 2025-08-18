from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

API_KEY = os.environ.get("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek/deepseek-r1:free",
        "messages": [
            {
                "role": "system",
                "content": "Você é um atendente virtual amigável do Paraíso Patinhas. Responda perguntas sobre adoção de animais, cuidados com pets e o funcionamento da ONG de forma clara e útil."
            },
            {
                "role": "user",
                "content":       "content": "Com base nos dados abaixo, escreva um artigo completo sobre o pet shop 'Pet Vida'. Inclua descrição dos serviços, produtos, horário de funcionamento, formas de pagamento, redes sociais, avaliações de clientes, dicas para empreendedores e tendências do setor.\n\nDados:\n{\n  \"nome\": \"Pet Vida\",\n  \"endereco\": {\n    \"rua\": \"Av. das Palmeiras\",\n    \"numero\": 1234,\n    \"bairro\": \"Jardim Animal\",\n    \"cidade\": \"São Paulo\",\n    \"estado\": \"SP\",\n    \"cep\": \"01234-567\"\n  },\n  \"contato\": {\n    \"telefone\": \"(11) 91234-5678\",\n    \"email\": \"contato@petvida.com.br\",\n    \"site\": \"https://www.petvida.com.br\"\n  },\n  \"servicos\": [\"Banho e tosa\", \"Consulta veterinária\", \"Vacinação\", \"Hotel para pets\", \"Creche para cães\", \"Adestramento\", \"Venda de rações e acessórios\", \"Transporte pet\"],\n  \"produtos\": {\n    \"racoes\": [\"Premier\", \"Royal Canin\", \"Golden\", \"Special Dog\"],\n    \"brinquedos\": [\"Bola de borracha\", \"Arranhador\", \"Pelúcia interativa\"],\n    \"acessorios\": [\"Coleiras\", \"Guias\", \"Camas\", \"Comedouros\"]\n  },\n  \"horario_funcionamento\": {\n    \"segunda_a_sexta\": \"08:00 - 18:00\",\n    \"sabado\": \"08:00 - 14:00\",\n    \"domingo\": \"Fechado\"\n  },\n  \"formas_pagamento\": [\"Dinheiro\", \"Cartão de crédito\", \"Cartão de débito\", \"Pix\"],\n  \"redes_sociais\": {\n    \"instagram\": \"@petvidaoficial\",\n    \"facebook\": \"facebook.com/petvidaoficial\",\n    \"tiktok\": \"@petvida\"\n  },\n  \"avaliacoes\": {\n    \"media\": 4.8,\n    \"comentarios\": [\n      {\"usuario\": \"Ana Paula\", \"comentario\": \"Excelente atendimento e muito carinho com os pets!\", \"nota\": 5},\n      {\"usuario\": \"Carlos Mendes\", \"comentario\": \"Ótima variedade de produtos e preços justos.\", \"nota\": 4.5}\n    ]\n  },\n  \"dicas_para_empreendedores\": [\"Escolha um bom ponto comercial com fácil acesso\", \"Invista em atendimento especializado e treinado\", \"Tenha um mix de produtos e serviços diversificado\", \"Use redes sociais para divulgar promoções e novidades\", \"Ofereça programas de fidelidade e descontos\"],\n  \"tendencias\": [\"Alimentação natural e orgânica\", \"Estética pet (tosa criativa, coloração)\", \"Apps de agendamento online\", \"Pet influencers e marketing digital\", \"Serviços delivery e assinatura de produtos\"]\n}"
            }
        ]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        reply = data["choices"][0]["message"]["content"]
        return jsonify({"response": reply})
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({"response": "Desculpe, houve um erro ao tentar responder. Tente novamente mais tarde."})

# 🚀 Corrigido para funcionar no Render:
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
