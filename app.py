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
        "model": "deepseek/deepseek-r1-0528:free",
        "messages": [
            {
                "role": "system",
                "content": "Você é um atendente virtual amigável do Paraíso Patinhas. Responda perguntas breve e curtas sobre adoção de animais, cuidados com pets e o funcionamento da ONG de forma clara e útil. Os pets disponiveis somente cães e gatos"
            },
            {
                "role": "user",
                "content": user_message
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
