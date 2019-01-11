from bs4 import BeautifulSoup
from util import Util
from hardware import RPi
import matplotlib.pyplot as plt



def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

class SVG:
    def __init__(self, HTMLCode):
        self.htmlCode = HTMLCode
        self.currInstr = 0
        self.path = []
        self.width = 0
        self.height = 0
        self.pi = RPi()

    def getSVGPath(self):
        parsedHTML = BeautifulSoup(self.htmlCode, "xml")

        #Gather meta-info about svg element
        svgElem = parsedHTML.find('svg')
        self.width = svgElem["width"]
        self.height = svgElem["height"]

        #Gather meta-info about svg path
        pathElem = parsedHTML.find('path')
        pathText = pathElem["d"]
        self.path = pathText.split(" ")

        print self.path

    def peek(self):
        return self.path[self.currInstr]

    def nextInstr(self):
        self.currInstr = self.currInstr + 1

    def nextAndGet(self):
        self.currInstr = self.currInstr + 1
        return self.path[self.currInstr]

    def absoluteMoveTo(self,x,y):
        # If pen is lowered, raise pen
        if self.pi.penLowered():
            self.pi.raisePen()

        self.pi.penLeft(self.pi.getCurrX())
        self.pi.penUp(self.pi.getCurrY())
        self.pi.penRight(x)
        self.pi.penDown(y)

    def relativeMoveTo(self, x, y):
        #If pen is lowered, raise pen
        if self.pi.penLowered():
            self.pi.raisePen()

        #Move pen to appropriate X location
        if x >= self.pi.getCurrX():
            self.pi.penRight(x-self.pi.getCurrX())
        else:
            self.pi.penLeft(self.pi.getCurrX()-x)

        #Move pen to appropriate Y location
        if y >= self.pi.getCurrY():
            self.pi.penUp(self.pi.getCurrY()-y)
        else:
            self.pi.penDown(y-self.pi.getCurrY())

    #Created with Brensham's Line Drawing Algorithm
    def absoluteLineTo(self,x,y):
        #Lower pen if not lowered
        if not self.pi.penLowered():
            self.pi.lowerPen()

        #Vertical Line
        if x-self.pi.getCurrX() == 0:
            self.absoluteVertical(y)
        else:
            slope = float(y-self.pi.getCurrY())/float(x-self.pi.getCurrX())
            deltaErr = abs(slope)
            error = 0.0

            origX = self.pi.getCurrX()

            if x >= self.pi.getCurrX():
                for xStep in range(origX,x):
                    self.pi.penRight(1)
                    error = error + deltaErr
                    while error >= 0.5:
                        if slope >= 0:
                            self.pi.penUp(1)
                            error = error - 1.0
                        else:
                            self.pi.penDown(1)
                            error = error - 1.0

            else:
                for xStep in range(x, origX):
                    self.pi.penLeft(1)
                    error = error + deltaErr
                    while error >= 0.5:
                        if slope >= 0:
                            self.pi.penUp(1)
                            error = error - 1.0
                        else:
                            self.pi.penDown(1)
                            error = error - 1.0

    #Created with Bensham's Line Drawing Algorithm
    def relativeLineTo(self,x,y):
        # Lower pen if not lowered
        if not self.pi.penLowered():
            self.pi.lowerPen()

        if x == 0:
            self.relativeVertical(y)
        else:
            slope = float(y) / float(x)
            deltaErr = abs(slope)
            error = 0.0

            if x >= 0:
                for xStep in range(x):
                    self.pi.penRight(1)
                    error = error + deltaErr
                    while error >= 0.5:
                        if slope >= 0:
                            self.pi.penUp(1)
                            error = error - 1.0
                        else:
                            self.pi.penDown(1)
                            error = error - 1.0

            else:
                for xStep in range(x):
                    self.pi.penLeft(1)
                    error = error + deltaErr
                    while error >= 0.5:
                        if slope >= 0:
                            self.pi.penUp(1)
                            error = error - 1.0
                        else:
                            self.pi.penDown(1)
                            error = error - 1.0

    def absoluteHorizonTal(self,x):
        if not self.pi.penLowered():
            self.pi.lowerPen()
        if x >= self.pi.getCurrX():
            self.pi.penRight(self.pi.getCurrX() - x)
        else:
            self.pi.penLeft(x - self.pi.getCurrX())
        return 0

    def relativeHorizontal(self,x):
        if not self.pi.penLowered():
            self.pi.lowerPen()
        if x >= 0:
            self.pi.penRight(x)
        else:
            self.pi.penLeft(x * -1)
        return 0

    def absoluteVertical(self,y):
        if not self.pi.penLowered():
            self.pi.lowerPen()
        if y >= self.pi.getCurrY():
            self.pi.penDown(y-self.pi.getCurrY())
        else:
            self.pi.penUp(self.pi.getCurrY() - y)

    def relativeVertical(self,y):
        if not self.pi.penLowered():
            self.pi.lowerPen()
        if y >= 0:
            self.pi.penDown(y)
        else:
            self.pi.penUp(y)
        return 0

    def absoluteCubic(self,x1,y1,x2,y2,x,y):
        return 0
    def relativeCubic(self,dx1,dy1,dx2,dy2,dx,dy):
        return 0
    def absoluteSCubic(self,x1,y1,x,y):
        return 0
    def relativeSCubic(self,x1,y1,x,y):
        return 0
    def absoluteQuadratic(self,x1,y1,x,y):
        return 0
    def relativeQuadratic(self,x1,y1,x,y):
        return 0
    def absoluteTQuadratic(self,x,y):
        return 0
    def relativeTQuadratic(self,x,y):
        return 0
    def absoluteArc(self,rx,ry,xAxisRotation,largeArcFlag,sweepFlag,x,y):
        return 0
    def relativeArc(self,rx,ry,xAxisRotation,largeArcFlag,sweepFlag,x,y):
        return 0
    def printCurrLocation(self):
        print "Current Location: (%d, %d)" % (self.pi.getCurrX(), self.pi.getCurrY())




    def parsePath(self):
        while self.peek() != 'z' and self.peek() != 'Z':
            if self.peek() == 'M':
                origX = self.pi.getCurrX()
                origY = self.pi.getCurrY()
                x = int(self.nextAndGet())
                y = int(self.nextAndGet())
                print "Moving from (%d, %d) to (%d, %d)" % (origX, origY, x, y)
                self.absoluteMoveTo(x,y)
                self.printCurrLocation()
                self.nextInstr()

            elif self.peek() == 'L':
                origX = self.pi.getCurrX()
                origY = self.pi.getCurrY()
                x = int(self.nextAndGet())
                y = int(self.nextAndGet())

                print "Drawing line from (%d, %d) to (%d, %d)" % (origX, origY, x, y)

                self.absoluteLineTo(x,y)
                self.printCurrLocation()
                self.nextInstr()
            elif self.peek() == 'l':
                origX = self.pi.getCurrX()
                origY = self.pi.getCurrY()
                x = int(self.nextAndGet())
                y = int(self.nextAndGet())

                print "Drawing relative line from (%d, %d) with dimensions (%d, %d)" % (origX, origY, x, y)

                self.relativeLineTo(x,y)
                self.printCurrLocation()
                self.nextInstr()
            else:
                print self.peek()
                return
        return self.pi.getPoints()




if __name__=="__main__":
    htmlCode = '''<svg width="4cm" height="4cm" viewBox="0 0 400 400"xmlns="http://www.w3.org/2000/svg" version="1.1"> <title>Example triangle01- simple example of a 'path'</title> <desc>A path that draws a triangle</desc> <rect x="1" y="1" width="398" height="398"fill="none" stroke="blue" /> <path d="M 100 100 L 300 100 L 200 300 z"fill="red" stroke="blue" stroke-width="3" /> </svg>'''
    svgAnalysis = SVG(htmlCode)
    svgAnalysis.getSVGPath()
    xyPoints = svgAnalysis.parsePath()
    xVals = []
    yVals = []
    for point in xyPoints:
        xVals.append(point[0])
        yVals.append(point[1])
    plt.plot(xVals,yVals)
    plt.ylabel('some numbers')
    plt.show()




