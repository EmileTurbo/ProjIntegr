import speech_recognition as sr
from openai import OpenAI
import webbrowser
import textwrap
import os

client = OpenAI(api_key="")

r = sr.Recognizer()
m = sr.Microphone()

# Mot d'activation
activation_word = "marcus"  # You must say this word to activate the assistant

# Define trigger phrases and their corresponding actions
triggers = {
    "ouvre youtube": "https://www.youtube.com/",
    "ouvre google": "https://www.google.com/",
    "ouvre facebook": "https://www.facebook.com/"
}

# Command for writing to a text document**
write_command = "écris dans un document"

# Path to the text document
document_path = "marcus_notes.txt"

# Function to format the response with line breaks
def format_response(text, line_length=80):
    """Wraps the text with line breaks every `line_length` characters."""
    return "\n".join(textwrap.wrap(text, line_length))

# Function to write text to the document
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

        # Capture audio
        with m as source:
            audio = r.listen(source)

        print("🔎 Un instant...")

        try:
            # Recognize the speech
            value = r.recognize_google(audio, language="fr-FR").lower()
            print(f"✅ Tu as dit : {value}")

            # Check for activation word
            if activation_word in value:
                print("🚀 Activation détectée !")

                # Listen again for the actual command/question
                print("\n🔎 En attente de la commande...")
                with m as source:
                    audio = r.listen(source)

                # Recognize the next speech
                value = r.recognize_google(audio, language="fr-FR").lower()
                print(f"🎯 Commande détectée : {value}")

                # ✅ Check for triggers
                trigger_matched = False
                for trigger, url in triggers.items():
                    if trigger in value:
                        print(f"🌐 Ouverture de {url}")
                        webbrowser.open(url)
                        trigger_matched = True
                        break

                        # ✅ Check for "write to document" command
                if write_command in value:
                    print("✍️ Écriture dans le document...")

                    # Listen for the text to write
                    print("🗣️ Dis ce que tu veux écrire :")
                    with m as source:
                        audio = r.listen(source)

                    # Recognize the text to write
                    text_to_write = r.recognize_google(audio, language="fr-FR").lower()

                    # Write the spoken text to the document
                    write_to_document(text_to_write, document_path)
                    trigger_matched = True

                # ✅ If no trigger was detected, send to OpenAI
                if not trigger_matched:
                    completion = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system",
                             "content": "Tu es un assistant nommé Marcus Brossoit, tu donnes des réponses max 100 mots et tu parles comme une personne en précarité de Saint-Jérôme avec des expressions québécoises."},
                            {"role": "user", "content": value}
                        ]
                    )

                    # Display the response
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