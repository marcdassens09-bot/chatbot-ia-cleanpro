from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()
historique = []

print("Chatbot IA démarré ! Tape 'quitter' pour arrêter.")
print("-" * 40)

while True:
    message_utilisateur = input("Toi : ")
    
    if message_utilisateur.lower() == "quitter":
        print("Au revoir !")
        break
    
    historique.append({
        "role": "user",
        "content": message_utilisateur
    })
    
    reponse = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        messages=historique
    )
    
    texte_reponse = reponse.content[0].text
    
    historique.append({
        "role": "assistant",
        "content": texte_reponse
    })
    
    print(f"IA : {texte_reponse}")
    print("-" * 40)