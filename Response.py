import win32com.client


def list_voices():
    """List all installed TTS voices, including OneCore voices."""
    sapi = win32com.client.Dispatch("SAPI.SpVoice")
    tokens = sapi.GetVoices()

    for i, token in enumerate(tokens):
        print(f"Voice {i}: {token.GetDescription()}")


# List all voices, including hidden ones
list_voices()