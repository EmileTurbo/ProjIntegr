import speech_recognition as sr

r = sr.Recognizer()
m = sr.Microphone()

try:
    print("Un moment de silence...")
    with m as source: r.adjust_for_ambient_noise(source)
    print("Set minimum energy threshold to {}".format(r.energy_threshold))
    while True:
        print("Dit quelque chose ! :")
        with m as source: audio = r.listen(source)
        print("Got it! Now to recognize it...")
        try:
            # recognize speech using Google Speech Recognition
            value = r.recognize_google(audio, language="fr-FR")

            print("Tu a dit : {}".format(value))
        except sr.UnknownValueError:
            print("Oops! J'ai pas bien compris")
        except sr.RequestError as e:
            print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
except KeyboardInterrupt:
    pass
print("test")