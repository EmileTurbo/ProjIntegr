from openai import OpenAI
from openai import api_key

client = OpenAI(api_key="")

question = input("Entrez votre question : quel est ton nom ")

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Tu est un assistant nommé Marcus Brossoit, tu donne des réponses pas plus longue que 100 mots"},
        {
            "role": "user",
            "content": question
        }
    ]
)

response = completion.choices[0].message
print(response)