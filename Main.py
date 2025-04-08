import speech_recognition as sr
from openai import OpenAI
import webbrowser
import textwrap
import os
import urllib.parse
import time

# OpenAI setup
client = OpenAI(api_key="")

# Speech recognition setup
r = sr.Recognizer()
m = sr.Microphone()

# Mots d'activations
activation_word = "marcus"  # Mot d'activation
exit_command = "au revoir"

# Phrases de commandes
triggers = {
    "ouvre youtube": "https://www.youtube.com/",
    "ouvre google": "https://www.google.com/",
    "ouvre facebook": "https://www.facebook.com/",
    "ouvre amazon": "https://www.amazon.ca/-/fr/",
    "ouvre omnivox": "https://cstj.omnivox.ca/Login/Account/"
}

# Commandes spéciales
write_command = "écris dans le document"
search_command = "recherche"

# Path to the text document
document_path = "marcus_notes.txt"

# Temps d'inactivité avant retour en veille
timeout = 15  # secondes
max_no_response = 3  # Nombre d'erreurs avant mise en veille

# Fonction pour format le texte
def format_response(text, line_length=80):
    return "\n".join(textwrap.wrap(text, line_length))

# Fonction pour ecrire dans le ficher.txt
def write_to_document(text, path):
    mode = "a" if os.path.exists(path) else "w"  # Append if file exists, else create new
    with open(path, mode, encoding="utf-8") as file:
        file.write(text + "\n")
    print(f"📝 Texte ajouté au document : {path}")

# Fonction pour effectuer une recherche Google
def search_google(query):
    encoded_query = urllib.parse.quote(query)  # Encode la requête pour URL
    url = f"https://www.google.com/search?q={encoded_query}"
    print(f"🔍 Recherche Google : {query}")
    webbrowser.open(url)

try:
    print("Un moment de silence...")
    with m as source:
        r.adjust_for_ambient_noise(source)
    print(f"Seuil d'énergie minimum réglé à {r.energy_threshold}")

    while True:
        print("\n🎤 Dis quelque chose (dis 'Marcus' pour activer) :")

        with m as source:
            audio = r.listen(source)

        try:
            value = r.recognize_google(audio, language="fr-FR").lower()
            print(f"✅ Tu as dit : {value}")

            # Écoute pour le mot d'activation
            if activation_word in value:
                print("🚀 Activation détectée ! Mode conversation activé.")
                print(f"🤖 Marcus Brossoit:\nOui ?")
                active = True
                last_activity_time = time.time()
                no_response_count = 0  # Réinitialise le compteur d'erreurs

                while active:
                    print("\n🔎 En attente d'une commande...")

                    # Vérifie si le temps d'inactivité est dépassé
                    if time.time() - last_activity_time > timeout:
                        print("⏳ Temps d'inactivité dépassé, retour en veille...")
                        active = False
                        break

                    with m as source:
                        audio = r.listen(source)

                    try:
                        value = r.recognize_google(audio, language="fr-FR").lower()
                        print(f"🎯 Commande détectée : {value}")

                        # Vérifie si on doit quitter la conversation
                        if exit_command in value:
                            print("👋 Au revoir ! Marcus retourne en veille.")
                            active = False
                            break

                        trigger_matched = False

                        # ✅ Ouvrir un site web si une commande correspond
                        for trigger, url in triggers.items():
                            if trigger in value:
                                print(f"🌐 Ouverture de {url}")
                                webbrowser.open(url)
                                trigger_matched = True

                        # ✅ Recherche Google
                        if search_command in value:
                            query = value.replace(search_command, "").strip()
                            if query:
                                search_google(query)
                                trigger_matched = True
                            else:
                                print("❌ Pas de terme de recherche détecté.")

                        # ✅ Écriture dans un fichier
                        elif write_command in value:
                            print("✍️ Écriture dans le document...")

                            print("🗣️ Dis ce que tu veux écrire :")
                            with m as source:
                                audio = r.listen(source)

                            text_to_write = r.recognize_google(audio, language="fr-FR").lower()
                            write_to_document(text_to_write, document_path)
                            trigger_matched = True

                        # ✅ Si aucune commande spécifique n'est reconnue, envoie à OpenAI
                        if not trigger_matched:
                            completion = client.chat.completions.create(
                                model="gpt-3.5-turbo",
                                messages=[
                                    {"role": "system",
                                     "content": "Tu es un assistant nommé Marcus Brossoit, tu donnes des réponses max 150 mots et tu parles comme une personne en précarité de Saint-Jérôme avec des expressions québécoises. Tu est légèrement agressif quand quelqu'un te parle avec méchancité"},
                                    {"role": "user", "content": value}
                                ]
                            )

                            response = completion.choices[0].message.content
                            formatted_response = format_response(response, line_length=80)
                            print(f"🤖 Marcus Brossoit:\n{formatted_response}")

                        # 🔄 Réinitialise le timer et le compteur d'erreurs
                        last_activity_time = time.time()
                        no_response_count = 0

                    except sr.UnknownValueError:
                        no_response_count += 1
                        print(f"🤖 Marcus Brossoit:\nJ'ai pas compris... ({no_response_count}/{max_no_response})")

                        # Si Marcus ne comprend pas 3 fois, il retourne en veille
                        if no_response_count >= max_no_response:
                            print("⏳ Trop d'erreurs, retour en veille...")
                            active = False

                    except sr.RequestError as e:
                        print(f"🚫 Uh oh! Erreur de requête: {e}")

            else:
                print("⏳ Aucun mot d'activation détecté, retour à l'écoute...")

        except sr.UnknownValueError:
            print(f"🤖 Marcus Brossoit:\nJ'ai pas compris...")

        except sr.RequestError as e:
            print(f"🚫 Uh oh! Erreur de requête: {e}")

except KeyboardInterrupt:
    print("\n👋 Au revoir !")