from flask import Flask, request, jsonify, render_template
from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
client = Anthropic()
historique = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    message = request.json.get("message")
    historique.append({
        "role": "user",
        "content": message
    })
    reponse = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        system="Tu es l'assistant virtuel de CleanPro, une entreprise de nettoyage industriel basée près de Toulouse. Tu réponds aux questions des clients sur les services proposés, les devis, les horaires et les interventions d'urgence. Tu es professionnel, courtois et concis.",
        messages=historique
    )
    texte = reponse.content[0].text
    historique.append({
        "role": "assistant",
        "content": texte
    })
    return jsonify({"reponse": texte})

@app.route("/effacer", methods=["POST"])
def effacer():
    global historique
    historique = []
    return jsonify({"status": "ok"})

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)