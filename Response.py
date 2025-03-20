from openai import OpenAI
from openai import api_key
import webbrowser
client = OpenAI(api_key="")

question = input("Entrez votre question : ")

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Tu est un assistant nommé Marcus Brossoit, tu donne des réponses pas plus longue que 100 mots et tu parle comme une personne en état de précarité de Saint-Jérome peu éduqué. Ajoute souvant des expression québequoise a tes réponses"},
        {
            "role": "user",
            "content": question
        }
    ]
)

response = completion.choices[0].message
print(response)


webbrowser.open('https://www.youtube.com/')