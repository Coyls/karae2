import datetime
import random
import subprocess
from typing import Any
from awakenState import AwakeHelloState, AwakenState
from utils.protocol import ProtocolGenerator
from utils.speak import Speak
from utils.types import BtnType
from utils.utils import speakSentence
# Dev 
# from plant import Plant

class PlantState:
    stateName : str
    awakenState : Any = ""

    # ! plant : Plant --> pas possible d'importer ou de setup
    # ! l'IDE dectect un import circulair + class declarer avant son initialisation 
    def __init__(self, plant):
        self.plant = plant

    def handleSwitch(self):
        pass

    def handleProximity(self):
        pass

    def handleHumidityGround(self):
        pass

    def handleDelay(self,  acces : str):
        pass

    def handleButtons(self, type : BtnType):
        pass

    def process(self):
        pass

class SetupState(PlantState):
    # Wait for all connections

    stateName = "setup-state"

    twofa = 1

    def handleSwitch(self):
        pass

    def handleProximity(self):
        pass

    def handleDelay(self,  acces : str):
        pass

    def handleButtons(self, type : BtnType):
        pass

    def process(self):
        pass
        
class StandbyAfterSetup(PlantState):

    stateName = "standby-after-setup"

    def __init__(self, plant,delay: int):
        super().__init__(plant)
        Speak.speak("Appuie sur le collier pour lancer le tutoriel !")
        self.delay = delay
        cls = plant.connectionManager.clients
        res = dict((v,k) for k,v in cls.items())
        cl = res["eureka"]
        data = ProtocolGenerator(self.stateName,str(self.delay))
        cl.send_message(data.create())

    def handleSwitch(self):
        print("Go to TutorielState")
        self.plant.setState(TutorielState(self.plant))

    def handleProximity(self):
        pass

    def handleDelay(self,  acces : str):
        if (acces == self.stateName):
            Speak.speak("N'ésite pas a me reveiller, je te dirai ce dont j'ai besoin !")
            print("Go to SleepState")
            self.plant.setState(SleepState(self.plant))

    def handleButtons(self, type : BtnType):
        pass

    def process(self):
        pass

class TutorielState(PlantState):

    stateName = "tutoriel-state"

    def handleSwitch(self):
        pass

    def handleProximity(self):
        pass

    def handleDelay(self,  acces : str):
        pass

    def handleButtons(self, type : BtnType):
        pass

    def process(self):
        Speak.speak("Lancement du tutoriel")
        self.playTutorial()
        print("Go to SleepState")
        Speak.speak("N'ésite pas a me reveiller, je te dirai ce dont j'ai besoin !")
        self.plant.setState(SleepState(self.plant))
        
    # ----------------------------------------

    def playTutorial(self):
        print("Play tutorial")
        sentences = self.plant.sentence["tutorial"]
        speakSentence(sentences)

class SleepState(PlantState):
    
    stateName = "sleep-state"

    def handleSwitch(self):
        pass

    def handleProximity(self):
        print("Go to WakeUpState")
        date = datetime.datetime.now()
        self.plant.storage.saveOnStore("proximity", str(date))
        self.plant.storage.saveOnFile("proximity", str(date))
        self.plant.setState(WakeUpState(self.plant, 7))

    def handleDelay(self,  acces : str):
        pass

    def handleButtons(self, type : BtnType):
        print("Go to SelectPlantState")
        self.plant.setState(SelectPlantState(self.plant))

    def process(self):
        pass

class WakeUpState(PlantState):

    stateName = "wake-up-state"

    def __init__(self, plant,delay: int):
        super().__init__(plant)
        sentences = self.plant.sentence["wake-up-state"]
        speakSentence(sentences)
        self.delay = delay
        cls = plant.connectionManager.clients
        res = dict((v,k) for k,v in cls.items())
        cl = res["eureka"]
        data = ProtocolGenerator(self.stateName,str(self.delay))
        cl.send_message(data.create())

    def handleSwitch(self):
        print("Go To AwakeState")
        self.plant.setState(AwakeState(self.plant))

    def handleProximity(self):
        pass

    def handleDelay(self,  acces : str):
        print("Go to SleepState")
        if (acces == self.stateName):
            Speak.speak("Je retourne dormir !")
            self.plant.setState(SleepState(self.plant))

    def handleButtons(self, type : BtnType):
        print("Go to SelectPlantState")
        self.plant.setState(SelectPlantState(self.plant))

    def process(self):
        pass

class AwakeState(PlantState):

    stateName = "awake-state"
    awakeState : AwakenState

    def handleSwitch(self):
        self.awakeState.handleSwitch()

    def handleProximity(self):
        pass

    def handleDelay(self,  acces : str):
        if (acces == self.awakeState.stateName):
            print("self.awakeState.stateName",  self.awakeState.stateName)
            self.awakeState.handleDelay()

    def handleHumidityGround(self):
        self.awakeState.handleHumidityGround()

    def handleButtons(self, type : BtnType):
        pass

    def process(self):
        self.awakeStateSpeak()
        self.setState(AwakeHelloState(self))

    # ----------------------------------------

    def setState(self, awakeState : AwakenState):
        self.awakeState = awakeState
        self.awakeState.process()

    def awakeStateSpeak(self):
        sentences = self.plant.sentence["awake-state"]
        speakSentence(sentences)

    def goToNextState(self):
        self.plant.setState(StandbyAfterAwake(self.plant, 10))


class StandbyAfterAwake(PlantState):

    stateName = "standby-after-awake"
    
    def __init__(self,plant,delay: int):
        super().__init__(plant)
        self.delay = delay
        cls = plant.connectionManager.clients
        res = dict((v,k) for k,v in cls.items())
        cl = res["eureka"]
        data = ProtocolGenerator(self.stateName,str(self.delay))
        cl.send_message(data.create())

    def handleSwitch(self):
        print("Go to AwakeState")
        self.plant.setState(AwakeState(self.plant))

    def handleProximity(self):
        pass

    def handleDelay(self,  acces : str):
        print("Go to SleepState")
        if (acces == self.stateName):
            sentences = self.plant.sentence["return-to-sleep"]
            speakSentence(sentences)
            self.plant.setState(SleepState(self.plant))

    def handleButtons(self, type : BtnType):
        pass

    def process(self):
        pass

class SelectPlantState(PlantState):
    
    stateName = "select-plant-state"      

    def handleSwitch(self):
        pass

    def handleProximity(self):
        pass

    def handleDelay(self,  acces : str):
        pass

    def handleButtons(self, type : BtnType):
        if type == BtnType.OK.value:
            self.okButton()
        if type == BtnType.RIGHT.value:
            self.rightButton()
        if type == BtnType.LEFT.value:
            self.leftButton()

    def process(self, acces : str):
        Speak.speak("Selectionner votre plante.")

    # ----------------------------------------

    def rightButton(self):
        self.plant.storage.changePlantRight()

    def leftButton(self):
        self.plant.storage.changePlantLeft()

    def okButton(self):
        print("Go to SleepState")
        p = self.plant.storage.plantCarac["name"]
        Speak.speak(f"{p} a été selectionner !")
        self.plant.setState(SleepState(self.plant))
