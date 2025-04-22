import edge_tts
import asyncio

async def speak_edge(text):
    # Utilise une voix masculine en français canadien
    communicator = edge_tts.Communicate(text, voice="fr-CA-AntoineNeural")

    try:
        # Sauvegarde le son dans un fichier MP3
        await communicator.save("output.mp3")

        # Lire le fichier MP3 avec pygame (tu peux aussi utiliser un autre lecteur)
        import pygame
        pygame.mixer.init()
        pygame.mixer.music.load("output.mp3")
        pygame.mixer.music.play()

        # Attendre que la musique finisse
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.1)

        pygame.mixer.music.unload()
        print("🎤 Voix jouée avec succès !")

    except Exception as e:
        print(f"⚠️ Erreur : {e}")

# Teste la fonction
asyncio.run(speak_edge("Bonjour, je suis Marcus Brossoit."))