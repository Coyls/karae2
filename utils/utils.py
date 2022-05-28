import random
from utils.speak import Speak

def speakSentence(sentences : list[str]):
    s = random.choice(sentences)
    Speak.speak(s)