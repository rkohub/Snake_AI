import pygame
import sys
import math
import pyautogui
import random
import time
import numpy as np

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
    global moved, steps
    newPos[1] = pos[1]-1
    moved = True
    steps += 1

def moveLeft():
    global moved, steps
    newPos[0] = pos[0]-1
    moved = True
    steps += 1

def moveDown():
    global moved, steps
    newPos[1] = pos[1]+1
    moved = True
    steps += 1

def moveRight():
    global moved, steps
    newPos[0] = pos[0]+1
    moved = True
    steps += 1

def moveOnDirNum(dirNum):
    if(dirNum == 0):
        moveUp()
    elif(dirNum == 1):
        moveLeft()
    elif(dirNum == 2):
        moveDown()
    else:
        moveRight()

def botStep():
    senses = getSenses(pos)
    #print("Senses:", senses)
    choice = forwardProp(senses, w, layers)
    #print(choice)
    moveDir = np.where(choice == max(choice))[0]
    #print(moveDir)#Where outputs an array of all the indexes where a conditino is true. We choose the first index where the value is the max in the array. AKA The index of the max value
    moveOnDirNum(moveDir)

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

def forwardProp(inputs,weights,layers):
    #Same shape as the layer array because the layer array describes nodes.
    #z array is for unsigmoided nodes while a is for sigmoided nodes
    a = np.array([np.zeros(layer) for layer in layers])
    #print(a)
    z = np.array([np.zeros(layer) for layer in layers])
    #print(z)

    #Weights are Left arrays of length Right.
    #Layer is one of array of length Left and the weights is Left arrays of length Right. So when they are dot producted, you get ore array of legnth Right aka the next layer.

    #The first row of nodes is the input layer
    a[0] = inputs
    #print(z,a)

    #Forward Propogaton. Running throught the network finding all of the values for the nodes
    for layer in range(1,len(layers)):#layers[1:]:  
        #print(layer)
        #print(a[layer-1],w[layer-1])
        z[layer] = np.dot(a[layer-1],w[layer-1]) #Takes the matrix for the weights of the last layer and dot products them with the vector of nodes from the first array. Matrix vector multiplication
        #print("DOT:", a[layer-1].dot(w[layer-1]))
        #print(z)
        #print("")
        a[layer] = sigmoid(z[layer])
        #print(z,a)
    return a[-1]

def scoresToFitness(botsScores):
    maxMoves = max(np.array(botsScores)[:,1])
    #print(maxMoves)
    for i in range(0,len(botsScores)):
        score = botsScores[i]
        #print(score,i)
        bots[i].append(score[0] + (score[1]/maxMoves))

def makeNewGeneration(bots):
    #The inputed Bots array is an array with elements sorted by the fitness of the bots, each elelent is the weights and the fitness.
    botCount = len(bots)
    newBots = np.array(list(np.array(bots)[0:int(botCount/2)][:,0]))
    #print("NB: " + str(newBots))
    #print(len(newBots))
    #print(newBots[0])
    #print(np.shape(newBots))
    #print(np.shape(newBots[0]))
    #print("")

    ave = []
    for i in range(0,np.shape(newBots)[1]):
        #print(newBots[1])
        ave.append(np.average(newBots[:,i]))

    #print(ave)

    #ave = np.average(newBots)

    adds = []
    for i in range(0,int(botCount/2)):
    #for i in range(0,1):
        adds.append(np.array(ave) + (np.array([(2 * np.random.random((layers[i],layers[i+1])) - 1) / 10 for i in range(0,len(layers)-1)])))
    #print(np.shape(adds))
    newBots = np.concatenate((newBots, adds))
    #print(np.shape(newBots))
    return newBots


botCount = 100
newGen = []
generations = 100

print()

'''
for gen in range(0,generations):
    bots = []
    botsScores = []
    for k in range(0,botCount):
        bots.append([])

#'''
#print("k:", k)

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


'''
layers = [8,5,4]
#w = np.array([0.5 * np.ones([layers[i],layers[i+1]]) for i in range(0,len(layers)-1)])

if (gen == 0):
    w = np.array([2 * np.random.random((layers[i],layers[i+1])) - 1 for i in range(0,len(layers)-1)])
else:
    #print("Used_New_Gen: " + str(k))
    #print(newGen)
    w = newGen[k]

if(k == 0):
    #print("Gen: " + str(gen) + " " + str(w))
    #print("Shape :" + str(np.shape(w)))
    pass

#bots[k].append("W" + str(k))
bots[k].append(w)
#print(w)

#'''

steps = 0
foods = -1 #Starts at -1 so that the first food generation starts at 0

botGo = False

while(True):
    pos = reverseSnake[-1]
    newPos = pos[:]
    moved = False

    if(not foodOnField):
        foods += 1
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
        botStep()

    if(botGo):
        botStep()
        #time.sleep(0.1)

    if(keyPressed[ord('w')]):
        moveUp()
    elif(keyPressed[ord('a')]):
        moveLeft()
    elif(keyPressed[ord('s')]):
        moveDown()
    elif(keyPressed[ord('d')]):
        moveRight()

    if( ((newPos != pos) and (newPos in reverseSnake[1:]))  or (newPos[0] < 0) or (newPos[0] > 20) or (newPos[1] < 0) or (newPos[1] > 20) ):
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

        #print(reverseSnake,reverseSnake[1:])
        #print("Change")

    #print(reverseSnake)

    #Fun line here.
    #basicSnakeBody(generatePoint(),[int(random.random() * 255),int(random.random() * 255),int(random.random() * 255)])

    # Learned that doesn't erase every frame.
    # if(first):
    # 	basicSnakeBody([12,12])
    # 	first = False
    
    #Update the full display surface to the screen. This is needed
    pygame.display.flip()

    #time.sleep(timeForStep)
    

    #I believe this is if I click the X it quits python executing for me.
    for event in pygame.event.get():
	    if event.type == pygame.QUIT:
	        sys.exit()

    if(keyPressed[ord('q')]):
        sys.exit()

        #print("Steps: ", steps)
        #print("Foods: ", foods)
        

        #botsScores.append([foods,steps])

    #print(botsScores)
    #print(bots)
    #print("Generation: " + str(gen))# + "_: " + str(np.shape(botsScores)))
    #scoresToFitness(botsScores)
    #print("ONEEEEE: " + str(bots[1]) + "_: " + str(np.shape(bots[1])))
    #bots = sorted(bots, key = lambda element: element[1], reverse = True) #key function is used to get the thing tat determines the sorting.
    #print(bots)
    #print("Top_Score: " + str(bots[0][1]))
    #newGen = makeNewGeneration(bots)
    #print(newGen[0])
    #print(newGen[0][1])
    #print("End_Generation")
   # print("\n")
print("Done")