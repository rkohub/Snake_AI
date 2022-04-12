from MLNPY import ML
import numpy as np
import random
import copy

class GenAlgoLearning:
	def __init__(self, layers, populationSize = 100):
		#Makes a population
		self.layers = np.array(layers)
		self.populationSize = populationSize
		self.population = self.initialisePopulation(self.layers, self.populationSize)

	def sortBots(self):
		#Sorts the bots by fitness
		self.population = np.array(sorted(self.population, key = lambda element: element.fitness, reverse = True))

	def initialisePopulation(self,layers, populationSize):
		#Makes a random population of solutions
		return np.array([ML(layers) for i in range(0,populationSize)])

	def getFitnesses(self):
		fitnesses = np.vectorize(lambda chro: chro.fitness) #Way 2. Vectorise works like making a function with another. 
		return fitnesses(self.population) #now when we run the new fintessES function it will take every input and return its fitness

	def printFitness(self):
		#print([chromosome.fitness for chromosome in self.population]) #1 Way
		print(self.getFitnesses())

	def sumFitness(self):
		return np.sum(self.getFitnesses())

	def updateFitness(self, newFitness):
		#self.getFitnesses() = newFitness # I was trying to find a way to update them all at onece but I don't think that is going to work
		for i in range(0,self.populationSize):
			self.population[i].fitness = newFitness[i]
		pass

	def makeNewGeneration(self):
		newGeneration = []
		self.sortBots()
		#print(self.population)
		#print(type(self.population))
		#print(round(self.populationSize/2.0))
		#For loop for half the number of rounds for kinds, because every round will yield 2 kids.
		for newChild in range(0, round(self.populationSize/2.0)):
			#Choose parents, Crossover, and mutate
			parent1 = self.chooseParent()
			parent2 = self.chooseParent()
			#print(parent1,parent2)
			#DEep copy, coppies and dissassociates objects
			child1, child2 = self.crossoverBreed(copy.deepcopy(parent1),copy.deepcopy(parent2))
			
			child1.fitness = 0
			child2.fitness = 0
			#Then add to the start of the next generation
			newGeneration = np.append(newGeneration, [self.mutate(copy.deepcopy(child1)), copy.deepcopy(self.mutate(child2))])
		#print(newGeneration)
		self.population = newGeneration

	def chooseParent(self):
		#ok so picture we hjave the the fitneesses as rectangles all pushed together with the length of the rectangles being relative to the fitness. If we choose a random number between 0 and the sum, this is a weighted selection.
		#https://en.wikipedia.org/wiki/Fitness_proportionate_selection
		sumFitness = self.sumFitness()
		randVal = random.random() * sumFitness
		#print(randVal)
		runningSum = 0
		fitness = self.getFitnesses()
		for i in range(0, self.populationSize):
			#We find which rectangle the random number seelcted by running and addin the rectangles till we pass the number. THen the rectange we just ran by is the one it picked.
			runningSum += fitness[i]
			if(runningSum > randVal):
				return self.population[i]
		return self.population[0]

	def crossoverBreed(self, parent1, parent2):
		# parent1 = np.copy(parent1)
		# parent2 = np.copy(parent2)
		#Inspiration Here
		#https://stackoverflow.com/questions/31708478/how-to-evolve-weights-of-a-neural-network-in-neuroevolution
		#Returns 2 children
		#High chance to swap all the weights comming out of a node, and low chance to swap an entire layer
		if(random.random() > 0.7):
			#print("Swap Layer")
			#print(F"p1: {parent1.weights } \n p2: {parent2.weights}")
			#print(f"layerSwap {int(random.random() * (len(self.layers) - 1))}")
			swapLayer = int(random.random() * (len(self.layers) - 1))
			#print(f"layerSwap {swapLayer}")
			temp = np.copy(parent1.weights[swapLayer])
			#print(f"temp {temp}")
			parent1.weights[swapLayer] = parent2.weights[swapLayer]
			parent2.weights[swapLayer] = temp
			#print(f"temp {temp}")
			#print(F"p1: {parent1.weights } \n p2: {parent2.weights}")
		else:
			#print("Swap Node")
			swapLayer = int(random.random() * (len(self.layers) - 1))
			swapNode  = int(random.random() * (self.layers[swapLayer]))
			#print(f"Swap {swapLayer,swapNode}")
			#print(parent1.weights[swapLayer,swapNode])
			#print(F"p1: {parent1.weights } \n p2: {parent2.weights}")
			temp = np.copy(parent1.weights[swapLayer,swapNode])
			parent1.weights[swapLayer,swapNode] = parent2.weights[swapLayer,swapNode]
			parent2.weights[swapLayer,swapNode] = temp
			#print(F"p1: {parent1.weights } \n p2: {parent2.weights}")
		return parent1, parent2

	def mutate(self, chromosome):
		randomChoice = random.random()
		#Again link
		#https://stackoverflow.com/questions/31708478/how-to-evolve-weights-of-a-neural-network-in-neuroevolution
		#4 different mutation options for a random weigth
		swapLayer  = int(random.random() * (len(self.layers) - 1))
		swapNodeL   = int(random.random() * (self.layers[swapLayer]))
		swapNodeR   = int(random.random() * (self.layers[swapLayer+1]))
		#print(swapLayer,swapNodeL,swapNodeR)
		#print(chromosome.weights)
		#print(chromosome.weights[swapLayer,swapNodeL,swapNodeR])
		if(randomChoice < 0.25):
			#print(f"1 {randomChoice}")
			#print("New Random Value")
			#New Value from -1,1
			chromosome.weights[swapLayer,swapNodeL,swapNodeR] = 2 * random.random() - 1
		elif(randomChoice < 0.5):
			#print(f"2 {randomChoice}")
			#print("Precentage Multiplication")
			#Scale between x0 to x2 aka 1/2 is x0.5 or 3/2 is x1.5
			chromosome.weights[swapLayer,swapNodeL,swapNodeR] *= random.random() * 2
		elif(randomChoice < 0.75):
			#print(f"3 {randomChoice}")
			#print("Random Addition or subtraction")
			#Add a random value to the weight. The second part is 1 and -1 half of the time so it is random either additnio or subtracton
			chromosome.weights[swapLayer,swapNodeL,swapNodeR] += random.random() * (2 * (random.random() > 0.5) - 1)
		else:
			#print(f"4 {randomChoice}")
			#print("Sign Switch")
			chromosome.weights[swapLayer,swapNodeL,swapNodeR] *= -1
		#print(chromosome.weights)
		#print(chromosome.weights[swapLayer,swapNodeL,swapNodeR])
		return chromosome







'''

myLayers = [8,10,4]
chromosomes = 10

AI = GenAlgoLearning(myLayers, chromosomes)
#print(AI.population)
newFit = np.arange(0,2 * chromosomes,2)
#print(newFit)
AI.updateFitness(newFit)
AI.sortBots()
AI.printFitness()
#print(AI.population[0].fitness)


print(AI.population)
AI.makeNewGeneration()
print(AI.population)

#'''

#print(2 * (0.4 > 0.5))
'''
bots = np.array([])

for i in range(0, 10):
	newLayers = [8,10,4]
	bot = ML(newLayers)
	bot.fitness = i + i % 4
	bots = np.append(bots, bot)
#'''

