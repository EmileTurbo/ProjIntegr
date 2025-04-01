import speech_recognition as sr
from openai import OpenAI
import webbrowser
import textwrap
import os

# OpenAI setup
client = OpenAI(api_key="")

# Speech recognition setup
r = sr.Recognizer()
m = sr.Microphone()

# Activation word
activation_word = "marcus"  # Mot d'activation

# Phrases de commandes
triggers = {
    "ouvre youtube": "https://www.youtube.com/",
    "ouvre google": "https://www.google.com/",
    "ouvre facebook": "https://www.facebook.com/"
}

# Phrase de fichier.txt
write_command = "écris dans le document"

# Path to the text document
document_path = "marcus_notes.txt"


# Fonction pour format le texte
def format_response(text, line_length=80):
    return "\n".join(textwrap.wrap(text, line_length))


# Fonction pour ecrire dans le ficher.txt
def write_to_document(text, path):
    """Writes the spoken text to a document."""
    mode = "a" if os.path.exists(path) else "w"  # Append if file exists, else create new
    with open(path, mode, encoding="utf-8") as file:
        file.write(text + "\n")
    print(f"📝 Texte ajouté au document : {path}")


try:
    print("Un moment de silence...")
    with m as source:
        r.adjust_for_ambient_noise(source)
    print("Seuil d'énergie minimum réglé à {}".format(r.energy_threshold))

    while True:
        print("\n🎤 Dis quelque chose (dit 'Marcus' pour activer) :")

        with m as source:
            audio = r.listen(source)

        try:
            # Reconnaissance vocale
            value = r.recognize_google(audio, language="fr-FR").lower()
            print(f"✅ Tu as dit : {value}")

            # Écoute pour le mot d'activation
            if activation_word in value:
                print("🚀 Activation détectée !")
                print(f"🤖 Marcus Brossoit:\nOui ?")

                # Ecoute pour la commande/question
                print("\n🔎 En attente de la commande...")
                with m as source:
                    audio = r.listen(source)

                value = r.recognize_google(audio, language="fr-FR").lower()
                print(f"🎯 Commande détectée : {value}")

                # ✅ Regarde pour des commandes
                trigger_matched = False
                for trigger, url in triggers.items():
                    if trigger in value:
                        print(f"🌐 Ouverture de {url}")
                        webbrowser.open(url)
                        trigger_matched = True
                        break

                        # ✅ Regarde si la commande d'écriture de fichier.txt est lancé
                if write_command in value:
                    print("✍️ Écriture dans le document...")

                    # Écoute pour le texte a écrire
                    print("🗣️ Dis ce que tu veux écrire :")
                    with m as source:
                        audio = r.listen(source)

                    text_to_write = r.recognize_google(audio, language="fr-FR").lower()

                    # Écrit dans la doc
                    write_to_document(text_to_write, document_path)
                    trigger_matched = True

                # ✅ Si aucune commandes vocale est dites
                if not trigger_matched:
                    completion = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system",
                             "content": "Tu es un assistant nommé Marcus Brossoit, tu donnes des réponses max 100 mots et tu parles comme une personne en précarité de Saint-Jérôme avec des expressions québécoises."},
                            {"role": "user", "content": value}
                        ]
                    )

                    # Affiche la réponse
                    response = completion.choices[0].message.content
                    formatted_response = format_response(response, line_length=80)
                    print(f"🤖 Marcus Brossoit:\n{formatted_response}")

            else:
                print("⏳ Aucun mot d'activation détecté, retour à l'écoute...")

        except sr.UnknownValueError:
            print("😕 Oops! J'ai pas bien compris")
        except sr.RequestError as e:
            print(f"🚫 Uh oh! Erreur de requête: {e}")

except KeyboardInterrupt:
    print("\n👋 Au revoir !")