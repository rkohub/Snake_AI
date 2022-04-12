import pygame
import sys
import math
import pyautogui
import random
import time
import numpy as np
from GeneticAlgo import GenAlgoLearning

#20x20 grid
gridDim = 21

thickness = 5
bO = 5 # Border Offset

squareOffset = 35
topOffset = 15

squareLen = 25
squareT   = 5

size = width, height = 760,760

white = [255,255,255]
black = [0,0,0]
red = [255,0,0]

def sigmoid(x,der = False):
    if(der):
        return x * (1 - x)
    else:
        return 1 / (1 + np.exp(-x))

def basicRect(pos, color = black):
    pygame.draw.rect(screen,color,[pos[0],pos[1],squareLen,squareLen], squareT)

def basicSnakeBody(cords, color = black):
    basicRect([topOffset + (squareOffset * cords[0]), topOffset + (squareOffset * cords[1])], color)

def generatePoint():
    cords =  [int(random.random() * gridDim), int(random.random() * gridDim)]
    #print(cords)
    return cords

def moveUp():
    global moved, steps, stepsSinceLastFood
    newPos[1] = pos[1]-1
    moved = True
    steps += 1
    stepsSinceLastFood += 1

def moveLeft():
    global moved, steps, stepsSinceLastFood
    newPos[0] = pos[0]-1
    moved = True
    steps += 1
    stepsSinceLastFood += 1

def moveDown():
    global moved, steps, stepsSinceLastFood
    newPos[1] = pos[1]+1
    moved = True
    steps += 1
    stepsSinceLastFood += 1

def moveRight():
    global moved, steps, stepsSinceLastFood
    newPos[0] = pos[0]+1
    moved = True
    steps += 1
    stepsSinceLastFood += 1

def moveOnDirNum(dirNum):
    if(dirNum == 0):
        moveUp()
    elif(dirNum == 1):
        moveLeft()
    elif(dirNum == 2):
        moveDown()
    else:
        moveRight()

def getSenses(headPos):
    #Man again, I really want to do this really complexly
    #(reverseSnake)
    senses = [0] * 8
    directions = [[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1]] #Rotation starting from Top Clockwise.

    for i in range(0,len(directions)):
        #print("I: ",i)
        direction = np.array(directions[i])
        for distance in range(1,21): #start 1 away and check basically till we hit the wall and break
            checkPos = direction * distance + headPos #Elementwise because direction is np.array # Scale direction vector and add to position
            #print("Dist: ", distance)
            #print("Check: ", checkPos)
            #print(type(checkPos))
            if(np.prod(checkPos == foodPos)): #Prod is how you and the element wise array of booleans
                #print("Food")
                senses[i] = round(1 - ((distance-1)/20),3)
                break
            if(list(checkPos) in reverseSnake):
                #print("Self") 
                senses[i] = round(((distance-1)/20) - 1,3)
                break
            if((not np.prod(np.logical_not(checkPos < np.array([0,0])))) or (not np.prod(np.logical_not(checkPos > np.array([20,20]))))):
                #print("Wall") 
                senses[i] = round(((distance-1)/20) - 1,3)
                break
    return senses

def addTralingZeroes(array, wantedLength):
        #Make a zero array of the wanted longer length
        newArray = np.zeros(wantedLength)
        #make the first portion of that 0's array what the inputed array was.
        newArray[0:len(array)] = array
        return newArray

def botStep(chroIndex):
    senses = getSenses(pos)
    #print("Senses:", senses)

    a,z = AI.population[chroIndex].forwardProp(addTralingZeroes(senses, max(AI.layers)))
    choice = a[-1]
    #sprint(choice)
    moveDir = np.where(choice == max(choice))[0]
    #print(moveDir)#Where outputs an array of all the indexes where a conditino is true. We choose the first index where the value is the max in the array. AKA The index of the max value
    moveOnDirNum(moveDir)

def scoresToFitness(botsScores):
    fitnesses = []
    maxMoves = max(np.array(botsScores)[:,1])
    #print(maxMoves)
    for i in range(0,len(botsScores)):
        score = botsScores[i]
        #print(score,i)
        fitnesses.append(score[0] + (score[1]/maxMoves))
    return fitnesses

myLayers = [8,10,4]
chromosomes = 50

AI = GenAlgoLearning(myLayers, chromosomes)
#AI.printFitness()
#print(AI.population)
#print(AI.populationSize)
slow = True

generations = 1000

for gen in range(0,generations):

    botScores = []

    for botIndex in range(0,AI.populationSize):

        #Initializes a screem wotj the set pixel size
        screen = pygame.display.set_mode(size)
        #Fill the screen with the RGB color
        screen.fill(white)
        #Surface to draw on, color, Rect(left,top,width height), line thickness
        #This is the screen Border
        pygame.draw.rect(screen, black, [bO,bO,width - (2 * bO),height - (2 * bO)], thickness)
        startPos = [int(gridDim/2) + 2, int(gridDim/2)]
        startLen = 4
        pos = []
        newPos = []
        foodOnField = False
        reverseSnake = [] #Corrcinates of all of the snakes nodes. In revers order so we can appedn
        for i in range(startLen-1,-1,-1):
            reverseSnake.append([startPos[0]-i,startPos[1]])
        for node in reverseSnake:
            basicSnakeBody(node)
        snakeLen = 1
        timeForStep = 1
        moved = False
        foodPos = []

        keys = [0] * 323
        lastKeys = keys

        steps = 0
        stepsSinceLastFood = 0
        foods = -1 #Starts at -1 so that the first food generation starts at 0

        botGo = True
        
        seed = (gen * 100) + botIndex
        random.seed(seed)

        while(True):
            pos = reverseSnake[-1]
            newPos = pos[:]
            moved = False

            if(not foodOnField):
                foods += 1
                stepsSinceLastFood = 0
                foodPos = generatePoint()
                while(foodPos in reverseSnake):
                    #print("Saved?")
                    foodPos = generatePoint()
                basicSnakeBody(foodPos, red)
                foodOnField = True

            #Array with values of 0 or 1 for each key. Each letter index is its ascii valur or ord
            lastKeys = keys
            keys = pygame.key.get_pressed()
            #If on the last frame each key wasn't pressed and now it is
            keyPressed = np.logical_and(np.logical_not(lastKeys),keys)

            if(keyPressed[ord('f')]):
                foodOnField = False

            if(keyPressed[ord('c')]):
                print(getSenses(pos))

            if(keyPressed[ord('b')]):
                botStep(botIndex)

            if(botGo):
                botStep(botIndex)
                if(keyPressed[ord('t')]):
                    slow = not slow
                time.sleep(0.1 if slow else 0)

            if(keyPressed[ord('w')]):
                moveUp()
            elif(keyPressed[ord('a')]):
                moveLeft()
            elif(keyPressed[ord('s')]):
                moveDown()
            elif(keyPressed[ord('d')]):
                moveRight()

            #If It moved and it moved into itself, or it moved into a wall, exit the game loop
            if( ((newPos != pos) and (newPos in reverseSnake[1:]))  or (newPos[0] < 0) or (newPos[0] > 20) or (newPos[1] < 0) or (newPos[1] > 20) ):
                break

            #If in a loop presumably
            if(stepsSinceLastFood > 1000):
                print("Killed For Stalling!")
                break

            if(moved):
                #I Could do something like
                #foodOnField = newPos == foodPos then
                #if(foodOnField): Erase Old Snake.sd
                #But that separates me from exactly what is happening.
                if(newPos == foodPos):
                    #If you run into food, dont erase the last node.
                    foodOnField = False
                else:
                    basicSnakeBody(reverseSnake[0],white)
                    del reverseSnake[0]

                reverseSnake.append(newPos)
                basicSnakeBody(newPos)

            
            #Update the full display surface to the screen. This is needed
            pygame.display.flip()

            #I believe this is if I click the X it quits python executing for me.
            for event in pygame.event.get():
        	    if event.type == pygame.QUIT:
        	        sys.exit()

            if(keyPressed[ord('q')]):
                sys.exit()

        print(f"Generation #: {gen} Bot #: {botIndex} collected {foods} foods and steped {steps} steps. Seed: {seed}")
        botScores.append([foods,steps])
        #print(f"Final Scores {botScores}")
    botScores = np.array(botScores)
    #print(f"Final Scores {botScores}")
    botFitnesses = scoresToFitness(botScores)
    #print(botFitnesses)
    #AI.printFitness()
    AI.updateFitness(botFitnesses)
    #AI.printFitness()
    #print(AI.population)
    AI.sortBots()
    AI.printFitness()
    #print(AI.population)
    AI.makeNewGeneration()
    #AI.printFitness()
    #print(AI.population)
    print("\n")
