
import subprocess

import gtts
from playsound import playsound

class Speak:

    def speak2(txt: str):
        subprocess.run(["sh","./scripts/speak.sh",txt])

    def speak(txt: str): # ja
        tts = gtts.gTTS(txt, lang="fr")
        tts.save("./audio/txt.mp3")
        playsound("./audio/txt.mp3")

