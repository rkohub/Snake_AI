import numpy as np
from GeneticAlgo import GenAlgoLearning
from RunSnake import SnakeGame

def scoresToFitness(botsScores):
    fitnesses = []
    maxMoves = max(np.array(botsScores)[:,1])
    for i in range(0,len(botsScores)):
        score = botsScores[i]
        fitnesses.append(score[0] + (score[1]/maxMoves))
    return fitnesses

myLayers = [8,10,4]
chromosomes = 50

AI = GenAlgoLearning(myLayers, chromosomes)

slow = True

generations = 1000

game = SnakeGame()

for gen in range(0,generations):

    botScores = []

    for botIndex in range(0,AI.populationSize):

        seed = (gen * 100) + botIndex

        foods, steps, slow = game.runGame(AI.population[botIndex], seed, slow)

        print(f"Generation #: {gen} Bot #: {botIndex} collected {foods} foods and steped {steps} steps. Seed: {seed}")
        botScores.append([foods,steps])

    botScores = np.array(botScores)
    botFitnesses = scoresToFitness(botScores)
    AI.updateFitness(botFitnesses)
    AI.sortBots()
    AI.printFitness()
    AI.makeNewGeneration()
    print("\n")