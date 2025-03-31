import speech_recognition as sr
from openai import OpenAI
from openai import api_key
import webbrowser
import textwrap

client = OpenAI(api_key="")

r = sr.Recognizer()
m = sr.Microphone()

# Define trigger phrases and their corresponding actions
triggers = {
    "ouvre YouTube": "https://www.youtube.com/",
    "ouvre Google": "https://www.google.com/",
    "ouvre Facebook": "https://www.facebook.com/"
}

# Function to format the response with line breaks
def format_response(text, line_length=80):
    """Wraps the text with line breaks every `line_length` characters."""
    return "\n".join(textwrap.wrap(text, line_length))

try:
    print("Un moment de silence...")
    with m as source:
        r.adjust_for_ambient_noise(source)
    print("Seuil d'énergie minimum réglé à {}".format(r.energy_threshold))

    while True:
        print("\n🎤 Dis quelque chose ! :")

        # Capture audio
        with m as source:
            audio = r.listen(source)

        print("🔎 Un instant...")

        try:
            # Recognize speech
            value = r.recognize_google(audio, language="fr-FR")
            print(f"✅ Tu as dit : {value}")

            # Check for trigger phrases
            for trigger, url in triggers.items():
                if trigger in value:
                    print(f"🌐 Ouverture de {url}")
                    webbrowser.open(url)
                    break  # Exit the loop after opening the site

            # Send the recognized speech to OpenAI
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

        except sr.UnknownValueError:
            print("😕 Oops! J'ai pas bien compris")
        except sr.RequestError as e:
            print(f"🚫 Uh oh! Erreur de requête: {e}")

except KeyboardInterrupt:
    print("\n👋 Au revoir !")