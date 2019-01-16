from bs4 import BeautifulSoup
import re
from util import Util

newUtil = Util()

class PathPrepper():
    def __init__(self, fileName):
        self.fileName = fileName
        self.pathStrings = []
        self.path = []
    def getSVGPaths(self):
        svg = open(self.fileName, 'r').read()

        parsedSVG = BeautifulSoup(svg, "xml")

        allPaths = parsedSVG.find_all("path")
        for path in allPaths:
            self.pathStrings.append(str(path["d"]))
    def cleanSVGPath(self, pathstring):
        return(re.findall(r'-?\d+\.?\d*e-?\d+|[A-Za-z]|-?\d+\.\d+|-?\d+|-?\.\d+', pathstring))
    def insertExtraCommands(self, pathParts):
        index = 0
        truePath = []
        lastInstr = ""
        while index < len(pathParts):
            if pathParts[index].isalpha():
                truePath.append(pathParts[index])
                lastInstr = pathParts[index]
            else:
                numberCount = 0
                tempIndex = index
                while tempIndex < len(pathParts) and not pathParts[tempIndex].isalpha():
                    if numberCount == 1 and (lastInstr == "H" or lastInstr == "h" or lastInstr == "v" or lastInstr == "V"):
                        truePath.append(lastInstr)
                        numberCount = 0
                    elif numberCount == 2 and (lastInstr == "m" or lastInstr == "M"):
                        truePath.append(lastInstr)
                        numberCount = 0
                    elif numberCount == 2 and (lastInstr == "l" or lastInstr == "L"):
                        truePath.append(lastInstr)
                        numberCount = 0
                    elif numberCount == 4 and (lastInstr == "q" or lastInstr == "Q"):
                        truePath.append(lastInstr)
                        numberCount = 0
                    elif numberCount == 4 and (lastInstr == "s" or lastInstr == "S"):
                        truePath.append(lastInstr)
                        numberCount = 0

                    elif numberCount == 6 and (lastInstr == "c" or lastInstr == "C"):
                        truePath.append(lastInstr)
                        numberCount = 0

                    numberCount += 1
                    truePath.append(pathParts[tempIndex])
                    tempIndex += 1
                index = tempIndex-1
            index += 1
        return truePath
    def getSinglePath(self):
        tempPath = []
        for path in self.pathStrings:
            pathParts = self.cleanSVGPath(path)
            tempPath = tempPath + pathParts
        self.path = self.insertExtraCommands(tempPath)
        print self.path
        return self.path









