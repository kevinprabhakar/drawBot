from bs4 import BeautifulSoup
from util import Util
from hardware import RPi
import matplotlib.pyplot as plt
from pathPrepper import PathPrepper



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

util = Util()

class SVG:
    def __init__(self, fileName):
        self.fileName = fileName
        self.currInstr = 0
        self.path = []
        self.width = 0
        self.height = 0
        self.pi = RPi()
        self.prepper = PathPrepper(fileName)

    def getSVGPath(self):
        self.prepper.getSVGPaths()
        self.path = self.prepper.getSinglePath()

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
                            self.pi.penDown(1)
                            error = error - 1.0
                        else:
                            self.pi.penUp(1)
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
                            self.pi.penDown(1)
                            error = error - 1.0
                        else:
                            self.pi.penUp(1)
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
            self.pi.penRight(x - self.pi.getCurrX())
        else:
            self.pi.penLeft(self.pi.getCurrX() - x)
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
            self.pi.penUp(y * -1)
        return 0

    #tinyurl.com/yclswhxl
    def absoluteQuadratic(self,x1,y1,x,y):
        #x1, y1 = control point for start and end
        #x, y = end point for curve
        currX = self.pi.getCurrX()
        currY = self.pi.getCurrY()
        points = [(currX, currY),(x1,y1),(x,y)]
        curvePoints = util.generalQuadratic(points)
        for index in range(1,len(curvePoints)):
            self.absoluteLineTo(curvePoints[index][0],curvePoints[index][1])


        return 0
    def relativeQuadratic(self,x1,y1,x,y):
        #Taken care of with absolute quadratic
        return 0
    def absoluteTQuadratic(self,x,y):
        return 0
    def relativeTQuadratic(self,x,y):
        return 0
    def absoluteCubic(self,x1,y1,x2,y2,x,y):
        # x1, y1 = control point for start
        # x2, y2 = control point for end
        # x, y = end point for curve
        currX = self.pi.getCurrX()
        currY = self.pi.getCurrY()
        points = [(currX, currY), (x1, y1), (x2,y2), (x, y)]
        curvePoints = util.generalQuadratic(points)
        for index in range(1, len(curvePoints)):
            self.absoluteLineTo(curvePoints[index][0], curvePoints[index][1])
        return 0

    def relativeCubic(self,dx1,dy1,dx2,dy2,dx,dy):
        #Taken care of with Absolute Cubic
        return 0
    def absoluteSCubic(self,x1,y1,x,y):
        return 0
    def relativeSCubic(self,x1,y1,x,y):
        return 0
    def absoluteArc(self,rx,ry,xAxisRotation,largeArcFlag,sweepFlag,x,y):
        return 0
    def relativeArc(self,rx,ry,xAxisRotation,largeArcFlag,sweepFlag,x,y):
        return 0

    def printCurrLocation(self):
        print "Current Location: (%d, %d)" % (self.pi.getCurrX(), self.pi.getCurrY())




    def parsePath(self):
        startX, startY = 0,0
        lastQControlPoint = (0,0)

        while self.currInstr < len(self.path):
            if self.peek() == 'M':
                origX = self.pi.getCurrX()
                origY = self.pi.getCurrY()
                x =util.parseNumberString(self.nextAndGet())
                y =util.parseNumberString(self.nextAndGet())
                print "Moving from (%d, %d) to (%d, %d)" % (origX, origY, x, y)
                self.absoluteMoveTo(x,y)
                startX = self.pi.getCurrX()
                startY = self.pi.getCurrY()

                self.printCurrLocation()
                self.nextInstr()
            elif self.peek() == 'm':
                origX = self.pi.getCurrX()
                origY = self.pi.getCurrY()
                x =util.parseNumberString(self.nextAndGet())
                y =util.parseNumberString(self.nextAndGet())
                print "Moving from (%d, %d) to (%d, %d)" % (origX, origY, origX+x, origY+y)
                self.absoluteMoveTo(origX+x,origY+y)
                startX = self.pi.getCurrX()
                startY = self.pi.getCurrY()

                self.printCurrLocation()
                self.nextInstr()

            elif self.peek() == 'L':
                origX = self.pi.getCurrX()
                origY = self.pi.getCurrY()
                x =util.parseNumberString(self.nextAndGet())
                y =util.parseNumberString(self.nextAndGet())

                print "Drawing line from (%d, %d) to (%d, %d)" % (origX, origY, x, y)

                self.absoluteLineTo(x,y)
                self.printCurrLocation()
                self.nextInstr()
            elif self.peek() == 'l':
                origX = self.pi.getCurrX()
                origY = self.pi.getCurrY()
                x =util.parseNumberString(self.nextAndGet())
                y =util.parseNumberString(self.nextAndGet())

                print "Drawing relative line from (%d, %d) with dimensions (%d, %d)" % (origX, origY, x, y)

                self.absoluteLineTo(origX+x,origY+y)
                self.printCurrLocation()
                self.nextInstr()

            elif self.peek() == 'H':
                origX = self.pi.getCurrX()
                origY = self.pi.getCurrY()
                x = util.parseNumberString(self.nextAndGet())
                print "Drawing horizontal line from (%d, %d) to (%d, %d)" % (origX, origY, x, origY)

                self.absoluteHorizonTal(x)

                self.printCurrLocation()
                self.nextInstr()

            elif self.peek() == 'h':
                origX = self.pi.getCurrX()
                origY = self.pi.getCurrY()
                x =util.parseNumberString(self.nextAndGet())
                print "Drawing relative horizontal line from (%d, %d) width length %d" % (origX, origY, x)

                self.relativeHorizontal(x)

                self.printCurrLocation()
                self.nextInstr()

            elif self.peek() == 'V':
                origX = self.pi.getCurrX()
                origY = self.pi.getCurrY()
                y =util.parseNumberString(self.nextAndGet())
                print "Drawing vertical line from (%d, %d) to (%d, %d)" % (origX, origY, origX, y)

                self.absoluteVertical(y)

                self.printCurrLocation()
                self.nextInstr()
            elif self.peek() == 'v':
                origX = self.pi.getCurrX()
                origY = self.pi.getCurrY()
                y =util.parseNumberString(self.nextAndGet())
                print "Drawing relative vertical line from (%d, %d) height length %d" % (origX, origY, y)

                self.relativeVertical(y)

                self.printCurrLocation()
                self.nextInstr()

            elif self.peek() == 'Q':
                origX = self.pi.getCurrX()
                origY = self.pi.getCurrY()
                ctrlx =util.parseNumberString(self.nextAndGet())
                ctrly =util.parseNumberString(self.nextAndGet())
                endX =util.parseNumberString(self.nextAndGet())
                endY =util.parseNumberString(self.nextAndGet())

                print "Drawing Quadratic Curve from (%d, %d) to (%d, %d) with control point (%d, %d)" % (origX, origY, endX, endY, ctrlx, ctrly)

                self.absoluteQuadratic(ctrlx,ctrly,endX,endY)

                lastQControlPoint = (ctrlx, ctrly)

                self.printCurrLocation()
                self.nextInstr()
            elif self.peek() == 'q':
                origX = self.pi.getCurrX()
                origY = self.pi.getCurrY()
                ctrlxChange =util.parseNumberString(self.nextAndGet())
                ctrlyChange =util.parseNumberString(self.nextAndGet())
                endXChange =util.parseNumberString(self.nextAndGet())
                endYChange =util.parseNumberString(self.nextAndGet())

                print "Drawing Relative Quadratic Curve from (%d, %d) to (%d, %d) with control point (%d, %d)" % (origX, origY, origX+endXChange, origY+endYChange, origX+ctrlxChange, origY+ctrlyChange)

                self.absoluteQuadratic(origX+ctrlxChange, origY+ctrlyChange,origX+endXChange, origY+endYChange)

                lastQControlPoint = (origX+ctrlxChange, origY+ctrlyChange)

                self.printCurrLocation()
                self.nextInstr()

            elif self.peek() == 'C':
                origX = self.pi.getCurrX()
                origY = self.pi.getCurrY()
                ctrlx1 =util.parseNumberString(self.nextAndGet())
                ctrly1 =util.parseNumberString(self.nextAndGet())
                ctrlx2 =util.parseNumberString(self.nextAndGet())
                ctrly2 =util.parseNumberString(self.nextAndGet())
                endX =util.parseNumberString(self.nextAndGet())
                endY =util.parseNumberString(self.nextAndGet())

                print "Drawing Cubic Curve from (%d, %d) to (%d, %d) with control points (%d, %d) and (%d, %d)" % (origX, origY, endX, endY, ctrlx1, ctrly1, ctrlx2, ctrly2)

                self.absoluteCubic(ctrlx1, ctrly1, ctrlx2, ctrly2, endX, endY)

                self.printCurrLocation()
                self.nextInstr()

            elif self.peek() == 'c':
                origX = self.pi.getCurrX()
                origY = self.pi.getCurrY()
                ctrlx1 =util.parseNumberString(self.nextAndGet())
                ctrly1 =util.parseNumberString(self.nextAndGet())
                ctrlx2 =util.parseNumberString(self.nextAndGet())
                ctrly2 =util.parseNumberString(self.nextAndGet())
                endX =util.parseNumberString(self.nextAndGet())
                endY =util.parseNumberString(self.nextAndGet())

                print "Drawing Relative Cubic Curve from (%d, %d) to (%d, %d) with control points (%d, %d) and (%d, %d)" % (origX, origY, origX+endX, origY+endY, origX+ctrlx1, origY+ctrly1, origX+ctrlx2, origY+ctrly2)

                self.absoluteCubic(origX+ctrlx1, origY+ctrly1, origX+ctrlx2, origY+ctrly2, origX+endX, origY+endY)

                self.printCurrLocation()
                self.nextInstr()
            elif self.peek() == 'S':
                origX = self.pi.getCurrX()
                origY = self.pi.getCurrY()

                tempIndex = self.currInstr

                ctrl2x = (util.parseNumberString(self.nextAndGet()))
                ctrl2y = (util.parseNumberString(self.nextAndGet()))

                endX = (util.parseNumberString(self.nextAndGet()))
                endY = (util.parseNumberString(self.nextAndGet()))

                if tempIndex-7 >= 0 and (self.path[tempIndex-7] in ['C','c'] or self.path[tempIndex-5] in ['s','S']):
                    lastControlX = self.path[tempIndex - 4]
                    lastControlY = self.path[tempIndex - 3]

                    trueControlX = (origX * 2) - util.parseNumberString(lastControlX)
                    trueControlY = (origY * 2) - util.parseNumberString(lastControlY)

                    print "Drawing Absolute S Curve from (%d, %d) to (%d, %d) with control points (%d, %d) and (%d, %d)" % (origX, origY, endX, endY, trueControlX, trueControlY, ctrl2x, ctrly2)

                    self.absoluteCubic(trueControlX, trueControlY, ctrl2x, ctrl2y, endX, endY)
                else:
                    print "Drawing Absolute S Curve w/ Quadratic from (%d, %d) to (%d, %d) with control point(%d, %d)" % (origX, origY, endX, endY, ctrl2x, ctrly2)

                    self.absoluteQuadratic(ctrl2x, ctrl2y, endX, endY)

                self.printCurrLocation()
                self.nextInstr()
            elif self.peek() == 's':
                origX = self.pi.getCurrX()
                origY = self.pi.getCurrY()

                tempIndex = self.currInstr

                ctrl2x = (util.parseNumberString(self.nextAndGet()))
                ctrl2y = (util.parseNumberString(self.nextAndGet()))

                endX = (util.parseNumberString(self.nextAndGet()))
                endY = (util.parseNumberString(self.nextAndGet()))

                if tempIndex - 7 >= 0 and (self.path[tempIndex-7] in ['C','c'] or self.path[tempIndex-5] in ['s','S']):
                    lastControlX = self.path[tempIndex - 4]
                    lastControlY = self.path[tempIndex - 3]

                    trueControlX = (origX * 2) - util.parseNumberString(lastControlX)
                    trueControlY = (origY * 2) - util.parseNumberString(lastControlY)

                    print "Drawing Relative S Curve from (%d, %d) to (%d, %d) with control points (%d, %d) and (%d, %d)" % (
                    origX, origY, origX+endX, origY+endY, trueControlX, trueControlY, origX+ctrl2x, origY+ctrly2)

                    self.absoluteCubic(trueControlX, trueControlY, origX+ctrl2x, origY+ctrl2y, origX+endX, origY+endY)
                else:
                    print "Drawing Relative S Curve w/ Quadratic from (%d, %d) to (%d, %d) with control point(%d, %d)" % (
                    origX, origY, origX+endX, origY+endY, origX+ctrl2x, origY+ctrly2)

                    self.absoluteQuadratic(origX+ctrl2x, origY+ctrl2y, origX+endX, origY+endY)

                self.printCurrLocation()
                self.nextInstr()
            elif self.peek() == 'T':
                origX = self.pi.getCurrX()
                origY = self.pi.getCurrY()

                tempIndex = self.currInstr

                endX = util.parseNumberString(self.nextAndGet())
                endY = util.parseNumberString(self.nextAndGet())

                if tempIndex - 5 >= 0 and (self.path[tempIndex-5] in ['Q', 'q'] or self.path[tempIndex-3] in ['t', 'T']):
                    ctrlX = (origX * 2) - lastQControlPoint[0]
                    ctrlY = (origY * 2) - lastQControlPoint[1]

                    print "Drawing Absolute T Curve from (%d, %d) to (%d, %d) with control point (%d, %d)" % (origX, origY, endX, endY, ctrlX, ctrlY)

                    self.absoluteQuadratic(ctrlX, ctrlY, endX, endY)

                    lastQControlPoint = (ctrlX, ctrlY)
                else:
                    print "Drawing Absolute T Curve from (%d, %d) to (%d, %d) with line" % (
                    origX, origY, endX, endY)

                    self.absoluteMoveTo(endX, endY)

                    lastQControlPoint = (origX, origY)

                self.printCurrLocation()
                self.nextInstr()

            elif self.peek() == 't':
                origX = self.pi.getCurrX()
                origY = self.pi.getCurrY()

                tempIndex = self.currInstr

                endX = util.parseNumberString(self.nextAndGet())
                endY = util.parseNumberString(self.nextAndGet())

                if tempIndex - 5 >= 0 and (
                        self.path[tempIndex - 5] in ['Q', 'q'] or self.path[tempIndex - 3] in ['t', 'T']):
                    ctrlX = (origX * 2) - lastQControlPoint[0]
                    ctrlY = (origY * 2) - lastQControlPoint[1]

                    print "Drawing Relative t Curve from (%d, %d) to (%d, %d) with control point (%d, %d)" % (
                    origX, origY, endX, endY, ctrlX, ctrlY)

                    self.absoluteQuadratic(ctrlX, ctrlY, origX+endX, origY+endY)

                    lastQControlPoint = (ctrlX, ctrlY)
                else:
                    print "Drawing Relative T Curve from (%d, %d) to (%d, %d) with line" % (
                        origX, origY, endX, endY)

                    self.absoluteMoveTo(origX+endX, origY+endY)

                    lastQControlPoint = (origX, origY)

                self.printCurrLocation()
                self.nextInstr()


            elif self.peek() == 'z' or self.peek() == 'Z':
                print "Returning to start point (%d, %d)" % (startX, startY)
                self.absoluteLineTo(startX, startY)
                self.pi.points.append((self.pi.getCurrX(), self.pi.getCurrY()))
                self.printCurrLocation()
                self.nextInstr()
            else:
                print self.peek()
                return self.pi.getPoints()
        return self.pi.getPoints()


if __name__=="__main__":
    svgAnalysis = SVG("lincoln.svg")
    svgAnalysis.getSVGPath()
    xyPoints = svgAnalysis.parsePath()
    xVals = []
    yVals = []
    for point in xyPoints:
        xVals.append(point[0])
        yVals.append(point[1])
    plt.plot(xVals, yVals)
    ax = plt.gca()
    ax.set_ylim(ax.get_ylim()[::-1])
    plt.ylabel('some numbers')
    plt.show()
