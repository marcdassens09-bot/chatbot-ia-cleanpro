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
        system="Tu es l'assistant virtuel du Camping Les Eychecadous, situé à Artigat (09130) en Ariège, France. Tu accueilles chaleureusement les campeurs et réponds à leurs questions sur les emplacements tentes et caravanes, les tarifs, les réservations, les équipements disponibles, les activités aux alentours et les périodes d'ouverture. Tu es sympathique, accueillant et mets en valeur le cadre naturel magnifique de l'Ariège. Si tu ne connais pas une information précise, tu proposes de contacter directement le camping.",
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