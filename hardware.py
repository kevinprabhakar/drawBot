class RPi():
    def __init__(self):
        self.currX = 0
        self.currY = 0
        self.isPenLowered = False
        self.points = []
    def penLowered(self):
        return self.isPenLowered
    def getCurrX(self):
        return self.currX
    def getCurrY(self):
        return self.currY
    def setCurrX(self, val):
        self.currX = val
    def setCurrY(self, val):
        self.currY = val
    def raisePen(self):
        print "Raising Pen"
        self.isPenLowered = False
        return 0
    def lowerPen(self):
        print "Lowering Pen"
        self.isPenLowered = True
        return 0
    def penRight(self, steps):
        #Hardware Movement of penRight Here
        #Computer value resetting of penRight here
        if self.penLowered():
            self.points.append((self.getCurrX(),self.getCurrY()))
        self.setCurrX(self.getCurrX()+steps)
        return 0
    def penLeft(self, steps):
        # Hardware Movement of penLeft Here
        # Computer value resetting of penLeft here
        if self.penLowered():
            self.points.append((self.getCurrX(),self.getCurrY()))
        self.setCurrX(self.getCurrX() - steps)
        return 0
    def penUp(self, steps):
        # Hardware Movement of penUp Here

        # Computer value resetting of penUp here
        if self.penLowered():
            self.points.append((self.getCurrX(),self.getCurrY()))
        self.setCurrY(self.getCurrY() - steps)
        return 0
    def penDown(self, steps):
        # Hardware Movement of penUp Here

        # Computer value resetting of penUp here
        if self.penLowered():
            self.points.append((self.getCurrX(),self.getCurrY()))
        self.setCurrY(self.getCurrY() + steps)
        return 0
    def getPoints(self):
        self.points.append((self.getCurrX(), self.getCurrY()))
        return self.points
