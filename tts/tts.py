from gtts import gTTS

def save(text : str, filename : str):
    tts = gTTS(text)
    tts.save(filename)
