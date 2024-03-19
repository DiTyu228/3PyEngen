import string




class OpenModel():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.Cx = 0
        self.Cy = 0
        self.Cz = 0
        self.Cw = 0
    def f3model(self, model_way):
        file = open(model_way, "r", encoding="utf8")
        code = file.readline(500)
        while True:
            if code.startswith("3F"):
                cords = code.replace("3F", " ")
                return cords
            if code.startswith("x"):
                cords = code.replace("X", " ")
                num = int(cords)
                fnum = num / 100
                return fnum
            if code.startswith("Y"):
                cords = code.replace("Y", " ")
                num = int(cords)
                fnum = num / 100
                return fnum
            if code.startswith("Z"):
                cords = code.replace("Z", " ")
                num = int(cords)
                fnum = num / 100
                return fnum
            if code.startswith("STOP"):
                file.close()
                break
                return 9999