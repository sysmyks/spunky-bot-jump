import openai
import sys
from unidecode import unidecode

# Définir votre clé d'API OpenAI
openai.api_key = "api key"

# Nom du fichier pour stocker l'historique des échanges
history_file = "conversation_history.txt"

def generate_response(prompt):
    # Charger l'historique des échanges précédents à partir du fichier
    with open(history_file, "r") as file:
        conversation_history = file.read()

    # Ajouter la nouvelle question au contexte
    full_prompt = conversation_history + "\n" + prompt

    # Appel à l'API OpenAI pour générer une réponse
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": full_prompt}
        ]
    )

    # Récupérer la réponse générée depuis la réponse de l'API
    generated_text = response.choices[0].message.content.strip()

    # Enregistrer le nouvel échange dans le fichier
    #with open(history_file, "a") as file:
    #    file.write(prompt + "\n" + generated_text + "\n")

    return generated_text

# Récupérer l'argument de ligne de commande contenant la demande de l'utilisateur
user_input = ' '.join(sys.argv[1:])

# Appeler la fonction de génération de réponse en passant la demande de l'utilisateur
generated_response = generate_response(user_input)
generated_response = unidecode(generated_response)
# Afficher la réponse générée
print("^1chat-Gpt ^7:^2", generated_response)
