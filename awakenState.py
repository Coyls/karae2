from datetime import datetime
import time
from utils.protocol import ProtocolGenerator
from utils.speak import Speak
from utils.utils import speakSentence
# Dev
# from plantState import AwakeState

class AwakenState:

    stateName : str

    # ! awake : AwakeState --> pas possible d'importer ou de setup
    # ! l'IDE dectect un import circulair + class declarer avant son initialisation 
    # !!!!!!!!!!!!!!!!!!!!!!!!! vvvvvvvv Suprimer pour eviter les inport circulaire
    def __init__(self, awake):
        self.awake = awake

    def process(self):
        pass

    def handleDelay(self):
        pass

    def handleSwitch(self):
        pass

class AwakeHelloState(AwakenState):

    stateName = "hello-state"

    def process(self):
        Speak.speak("Contente de te voir j'èspere que tu vas bien !")
        self.awake.setState(AwakeSetupState(self.awake))
        
class AwakeSetupState(AwakenState):

    stateName = "setup-state"
    
    def process(self):
        losts = self.getConnectionLost()
        isBroken = self.checkConnectionLost(losts)
        if isBroken:
            print("Lost : ", losts)
            self.speakError(losts)
            self.awake.setState(AwakeEndState(self.awake))
        else :
            self.awake.setState(AwakeNeedState(self.awake))

    def getConnectionLost(self) -> list[str]:
        return self.awake.plant.connectionManager.discClients

    def checkConnectionLost(self, cl : list[str]) -> bool:
        if len(cl) > 0:
            return True
        else:
            return False

    def speakError(self, losts : list[str]):
        str = ""
        for lost in losts:
            str = str + f"{lost}, "
        str = f"Oups j’ai un petit soucis technique, les capteurs : {str}sont déconnectés. Je te conseille de me redemarer."
        Speak.speak(str)
           
class AwakeNeedState(AwakenState):

    stateName = "need-state"

    needs : list[list[str,str]] = []
    
    def process(self):
        self.checkNeeds()
        lengthNeeds = len(self.needs)
        if lengthNeeds > 0:
            # AwakeInfoMirrorState
            self.awake.setState(AwakeInfoMirrorState(self.awake, self.needs))
        else: 
            self.awake.setState(AwakeInfoGeneralState(self.awake))
    
    def checkNeeds(self):
        percent = self.checkWater()
        self.speakWater(percent)

    def checkWater(self):
        hg = self.awake.plant.storage.store["humidityground"]
        waterDb = datetime.strptime(hg, '%Y-%m-%d %H:%M:%S.%f')
        now = datetime.now()
        res = now - waterDb
        # !! Definir si second ou jours
        resRdy = int(res.total_seconds())
        delta = int(self.awake.plant.storage.plantCarac["deltaWater"])
        percent = int(100 * resRdy / delta) 
        return percent

    def speakWater(self, percent : int):
        MIN = 20
        TARGET = 80
        sentences = self.awake.plant.sentence["needs"]["water"]

        if (percent <= MIN):
            self.needs.append(["water","min"])
            speakSentence(sentences["min"])
        if (percent > MIN  and percent < TARGET):
            pass
        if (percent >= TARGET):
            self.needs.append(["water","max"])
            speakSentence(sentences["max"])
  
class AwakeInfoGeneralState(AwakenState):

    stateName = "info-general-state"

    def process(self):
        self.speakInfos()
        self.awake.setState(AwakeByeState(self.awake))

    def speakInfos(self):
        now = datetime.now()
        h = now.hour
        m = now.minute
        tmp = self.awake.plant.storage.store["temperature"]
        str = f"Il est {h} heures {m}, la temperature est de {tmp} degré. J'èspere que tu pass une bonne journée, pense à aller prendre l'air !"
        Speak.speak(str)

class AwakeInfoMirrorState(AwakenState):

    stateName = "info-mirror-state"

    def __init__(self, awake, needs : list[list[str,str]]):
        super().__init__(awake)
        self.needs = needs

    def process(self):
        self.speakInfos()
        self.awake.setState(AwakeStandbyAfterMirror(self.awake))

    def speakInfos(self):
        for need in self.needs:
            [root, key] = need
            sentences = self.awake.plant.sentence["mirror"][root][key]
            speakSentence(sentences) 

class AwakeStandbyAfterMirror(AwakenState):

    stateName = "standby-after-mirror"
    delay = 7   

    def process(self):
        Speak.speak("Souhaite tu plus d'info ?")
        # sentences = self.awake.plant.sentence["wake-up-state"]
        # speakSentence(sentences)
        cls = self.awake.plant.connectionManager.clients
        res = dict((v,k) for k,v in cls.items())
        cl = res["eureka"]
        data = ProtocolGenerator(self.stateName,str(self.delay))
        cl.send_message(data.create())

    def handleSwitch(self):
        print("Hello")
        self.awake.setState(AwakeInfoGeneralState(self.awake))

    def handleDelay(self):
        self.awake.setState(AwakeEndState(self.awake))

class AwakeByeState(AwakenState):

    stateName = "bye-state"
    
    def process(self):
        self.speakGreet()
        self.awake.setState(AwakeEndState(self.awake))

    def speakGreet(self):
        sentences = self.awake.plant.sentence["thanks"]
        speakSentence(sentences)

class AwakeEndState(AwakenState):

    stateName = "end-state"
    
    def process(self):
        print("AwakeEndState")
        Speak.speak("AHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHHAHAHAHAHA")
