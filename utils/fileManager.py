from utils.protocol import DbLineGenerator


class FileManager:
    def __init__(self, filePath:str) -> None:
        self.filePath = filePath

    def createFile(self):
        try:
            f = open(self.filePath, "x")
            f.close()
        except:
            print("File already exist !")
        

    def getLines(self) -> list[str]:
        f = open(self.filePath, "r")
        lines = f.readlines()
        f.close()
        return lines

    def createLines(self,lines : list[str]):
        w = open(self.filePath, "w")
        w.writelines(lines)
        w.close()

    def addValue(self,key: str, data: str):
        lines = self.getLines()
        global id
        id = -1
        for i, line in enumerate(lines):
            if key in line:
                id = i
        rawData = DbLineGenerator(key,data)
        dataRdyToUse = rawData.create()
        if id == -1:
            lines.append(dataRdyToUse)
        else:
            lines[id] = dataRdyToUse
        self.createLines(lines)
        print(lines)