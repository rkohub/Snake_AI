import pygame
import sys
import math
import pyautogui
import random
import time
import numpy as np
from GeneticAlgo import GenAlgoLearning


class SnakeGame:
    def __init__(self):
        #20x20 grid
        self.gridDim = 21

        self.thickness = 5
        self.bO = 5 # Border Offset

        self.squareOffset = 35
        self.topOffset = 15

        self.squareLen = 25
        self.squareT   = 5

        self.size = self.width, self.height = 760,760

        self.white = [255,255,255]
        self.black = [0,0,0]
        self.red = [255,0,0]

    def basicRect(self, pos, color = [0,0,0]):
        pygame.draw.rect(self.screen,color,[pos[0],pos[1],self.squareLen,self.squareLen], self.squareT)

    def basicSnakeBody(self, cords, color = [0,0,0]):
        self.basicRect([self.topOffset + (self.squareOffset * cords[0]), self.topOffset + (self.squareOffset * cords[1])], color)

    def generatePoint(self):
        self.cords =  [int(random.random() * self.gridDim), int(random.random() * self.gridDim)]
        return self.cords

    def moveUp(self):
        #global moved, steps, stepsSinceLastFood
        self.newPos[1] = self.pos[1]-1
        self.moved = True
        self.steps += 1
        self.stepsSinceLastFood += 1

    def moveLeft(self):
        #global moved, steps, stepsSinceLastFood
        self.newPos[0] = self.pos[0]-1
        self.moved = True
        self.steps += 1
        self.stepsSinceLastFood += 1

    def moveDown(self):
        #global moved, steps, stepsSinceLastFood
        self.newPos[1] = self.pos[1]+1
        self.moved = True
        self.steps += 1
        self.stepsSinceLastFood += 1

    def moveRight(self):
        #global moved, steps, stepsSinceLastFood
        self.newPos[0] = self.pos[0]+1
        self.moved = True
        self.steps += 1
        self.stepsSinceLastFood += 1

    def moveOnDirNum(self, dirNum):
        if(dirNum == 0):
            self.moveUp()
        elif(dirNum == 1):
            self.moveLeft()
        elif(dirNum == 2):
            self.moveDown()
        else:
            self.moveRight()

    def getSenses(self, headPos):
        #Man again, I really want to do this really complexly
        #(reverseSnake)
        self.senses = [0] * 8
        self.directions = [[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1]] #Rotation starting from Top Clockwise.

        for i in range(0,len(self.directions)):
            #print("I: ",i)
            self.direction = np.array(self.directions[i])
            for distance in range(1,21): #start 1 away and check basically till we hit the wall and break
                self.checkPos = self.direction * distance + headPos #Elementwise because direction is np.array # Scale direction vector and add to position
                #print("Dist: ", distance)
                #print("Check: ", checkPos)
                #print(type(checkPos))
                if(np.prod(self.checkPos == self.foodPos)): #Prod is how you and the element wise array of booleans
                    #print("Food")
                    self.senses[i] = round(1 - ((distance-1)/20),3)
                    break
                if(list(self.checkPos) in self.reverseSnake):
                    #print("Self") 
                    self.senses[i] = round(((distance-1)/20) - 1,3)
                    break
                if((not np.prod(np.logical_not(self.checkPos < np.array([0,0])))) or (not np.prod(np.logical_not(self.checkPos > np.array([20,20]))))):
                    #print("Wall") 
                    self.senses[i] = round(((distance-1)/20) - 1,3)
                    break
        return self.senses

    def addTralingZeroes(self, array, wantedLength):
            #Make a zero array of the wanted longer length
            self.newArray = np.zeros(wantedLength)
            #make the first portion of that 0's array what the inputed array was.
            self.newArray[0:len(array)] = array
            return self.newArray

    def botStep(self, bot):
        self.senses = self.getSenses(self.pos)
        #print("Senses:", senses)

        #a,z = AI.population[chroIndex].forwardProp(addTralingZeroes(senses, max(AI.layers)))
        self.a,self.z = bot.forwardProp(self.addTralingZeroes(self.senses, max(bot.layers)))
        self.choice = self.a[-1]
        #sprint(choice)
        #The Biggest value in the output of the neural network
        self.moveDir = np.where(self.choice == max(self.choice))[0]
        #print(moveDir)#Where outputs an array of all the indexes where a conditino is true. We choose the first index where the value is the max in the array. AKA The index of the max value
        self.moveOnDirNum(self.moveDir)

    def runGame(self, thisBot, randomSeed, slow):
        #Initializes a screem wotj the set pixel size
        self.screen = pygame.display.set_mode(self.size)
        #Fill the screen with the RGB color
        self.screen.fill(self.white)
        #Surface to draw on, color, Rect(left,top,width height), line thickness
        #This is the screen Border
        pygame.draw.rect(self.screen, self.black, [self.bO,self.bO,self.width - (2 * self.bO),self.height - (2 * self.bO)], self.thickness)
        self.startPos = [int(self.gridDim/2) + 2, int(self.gridDim/2)]
        self.startLen = 4
        self.pos = []
        self.newPos = []
        self.foodOnField = False
        self.reverseSnake = [] #Corrcinates of all of the snakes nodes. In revers order so we can appedn
        for i in range(self.startLen-1,-1,-1):
            self.reverseSnake.append([self.startPos[0]-i,self.startPos[1]])
        for node in self.reverseSnake:
            self.basicSnakeBody(node)
        self.snakeLen = 1
        self.timeForStep = 1
        self.moved = False
        self.foodPos = []

        self.keys = [0] * 323
        self.lastKeys = self.keys

        self.steps = 0
        self.stepsSinceLastFood = 0
        self.foods = -1 #Starts at -1 so that the first food generation starts at 0

        self.botGo = True

        random.seed(randomSeed)

        while(True):
            self.pos = self.reverseSnake[-1]
            self.newPos = self.pos[:]
            self.moved = False

            if(not self.foodOnField):
                self.foods += 1
                self.stepsSinceLastFood = 0
                self.foodPos = self.generatePoint()
                while(self.foodPos in self.reverseSnake):
                    #print("Saved?")
                    self.foodPos = self.generatePoint()
                self.basicSnakeBody(self.foodPos, self.red)
                self.foodOnField = True

            #Array with values of 0 or 1 for each key. Each letter index is its ascii valur or ord
            self.lastKeys = self.keys
            self.keys = pygame.key.get_pressed()
            #If on the last frame each key wasn't pressed and now it is
            self.keyPressed = np.logical_and(np.logical_not(self.lastKeys),self.keys)

            if(self.keyPressed[ord('f')]):
                self.foodOnField = False

            if(self.keyPressed[ord('c')]):
                print(self.getSenses(self.pos))

            if(self.keyPressed[ord('b')]):
                self.botStep(thisBot)

            if(self.botGo):
                self.botStep(thisBot)
                if(self.keyPressed[ord('t')]):
                    slow = not slow
                time.sleep(0.1 if slow else 0)

            if(self.keyPressed[ord('w')]):
                self.moveUp()
            elif(self.keyPressed[ord('a')]):
                self.moveLeft()
            elif(self.keyPressed[ord('s')]):
                self.moveDown()
            elif(self.keyPressed[ord('d')]):
                self.moveRight()

            #If It moved and it moved into itself, or it moved into a wall, exit the game loop
            if( ((self.newPos != self.pos) and (self.newPos in self.reverseSnake[1:]))  or (self.newPos[0] < 0) or (self.newPos[0] > 20) or (self.newPos[1] < 0) or (self.newPos[1] > 20) ):
                break

            #If in a loop presumably
            if(self.stepsSinceLastFood > 1000):
                print("Killed For Stalling!")
                break

            if(self.moved):
                #I Could do something like
                #foodOnField = newPos == foodPos then
                #if(foodOnField): Erase Old Snake.sd
                #But that separates me from exactly what is happening.
                if(self.newPos == self.foodPos):
                    #If you run into food, dont erase the last node.
                    self.foodOnField = False
                else:
                    self.basicSnakeBody(self.reverseSnake[0],self.white)
                    del self.reverseSnake[0]

                self.reverseSnake.append(self.newPos)
                self.basicSnakeBody(self.newPos)

            
            #Update the full display surface to the screen. This is needed
            pygame.display.flip()

            #I believe this is if I click the X it quits python executing for me.
            for event in pygame.event.get():
        	    if event.type == pygame.QUIT:
        	        sys.exit()

            if(self.keyPressed[ord('q')]):
                sys.exit()

        return self.foods, self.steps, slow