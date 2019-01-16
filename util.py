import operator as op
from functools import reduce
import math

quadraticStepCount = 10000


class Util():
    def is_number(self, s):
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
    def nCr(self, n, r):
        r = min(r, n - r)
        numer = reduce(op.mul, range(n, n - r, -1), 1)
        denom = reduce(op.mul, range(1, r + 1), 1)
        return numer / denom

    #https://medium.freecodecamp.org/nerding-out-with-bezier-curves-6e3c0bc48e2f
    def generalQuadratic(self, points):
        tStep = 1.0/quadraticStepCount
        endPoint = points[len(points)-1]
        curvePoints = [points[0]]
        for i in range(0, quadraticStepCount):
            Bx = 0.0
            By = 0.0
            for index in range(len(points)):
                Bx = Bx + (self.nCr(len(points)-1,index)*(math.pow((1-(i*tStep)),len(points)-1-index))*math.pow((i*tStep),index)*points[index][0])
                By = By + (self.nCr(len(points)-1,index)*(math.pow((1-(i*tStep)),len(points)-1-index))*math.pow((i*tStep),index)*points[index][1])
            if curvePoints[len(curvePoints)-1] != (int(Bx), int(By)):
                curvePoints.append((int(Bx),int(By)))
        if curvePoints[len(curvePoints)-1] != (int(endPoint[0]), int(endPoint[1])):
            curvePoints.append((int(endPoint[0]), int(endPoint[1])))

        return curvePoints

    def parseNumberString(self, numString, scale=1):
        if "e" in numString:
            numParts = numString.split("e")
            trueNum = float(numParts[0])*math.pow(10, float(numParts[1]))
            return int(round(trueNum * scale))
        return int(round(float(numString) * scale))
