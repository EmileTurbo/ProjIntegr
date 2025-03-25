import speech_recognition as sr
from openai import OpenAI
from openai import api_key
import webbrowser
import textwrap
import pyttsx3  # Pour le text-to-speech

client = OpenAI(api_key="")

# Initialise le TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speech speed (adjust as needed)
engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)

# Initialise le reconnaisseur vocal
r = sr.Recognizer()
m = sr.Microphone()

# Dictionnaire de definitions des commandes vocales
triggers = {
    "ouvre YouTube": "https://www.youtube.com/",
    "ouvre Google": "https://www.google.com/",
    "ouvre Facebook": "https://www.facebook.com/"
}

# Fonction pour alligné le texte
def format_response(text, line_length=80):
    """Wraps the text with line breaks every `line_length` characters."""
    return "\n".join(textwrap.wrap(text, line_length))

# Fonction pour parler
def speak(text):
    """Speaks the given text using pyttsx3."""
    engine.say(text)
    engine.runAndWait()

try:
    print("Un moment de silence...")
    with m as source:
        r.adjust_for_ambient_noise(source) # Ajuste le bruit de fond
    print("Seuil d'énergie minimum réglé à {}".format(r.energy_threshold))

    while True:
        print("\n🎤 Dis quelque chose ! :")

        # Capture audio
        with m as source:
            audio = r.listen(source)

        print("🔎 Un instant...")

        try:
            # Reconnaissance vocal
            value = r.recognize_google(audio, language="fr-FR")
            print(f"✅ Tu as dit : {value}")

            skip_openai = False

            # Check for trigger phrases
            for trigger, url in triggers.items():
                if trigger in value:
                    print(f"🌐 Ouverture de {url}")
                    webbrowser.open(url)
                    skip_openai = True # Si une commande vocal est dites, le AI ne va pas donner une réponse
                    break

            if skip_openai: # Skip le AI
                continue

            # Send the recognized speech to OpenAI
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                     "content": "Tu es un assistant nommé Marcus Brossoit, tu donnes des réponses max 150 mots et tu parles comme une personne en précarité de Saint-Jérôme avec des expressions québécoises."},
                    {"role": "user", "content": value}
                ]
            )

            # Affiche la réponse du AI
            response = completion.choices[0].message.content
            formatted_response = format_response(response, line_length=80)
            print(f"🤖 Marcus Brossoit:\n{formatted_response}")

            # Audio de Marcus
            speak(response)

        except sr.UnknownValueError:
            print("😕 Oops! J'ai pas bien compris")
        except sr.RequestError as e:
            print(f"🚫 Uh oh! Erreur de requête: {e}")

except KeyboardInterrupt:
    print("\n👋 Au revoir !")