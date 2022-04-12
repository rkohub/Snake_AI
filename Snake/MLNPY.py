import numpy as np
import random

class ML:
	def __init__ (self, layers, weights = None):
		self.layers = layers
		self.fitness = 0
		#If you input your own weights it uses thoes, otherwise it makes its own based off of the layers.
		if(weights != None):
			self.weights = weights
		else:
			self.makeWeights()

	def sigmoid(self, x, der = False):
		if(der):
			return x * (1 - x)
		else:
			return 1 / (1 + np.exp(-x))

	def makeWeights(self):
		#Fill the entire array with zeroes
		self.weights = np.zeros((len(self.layers)-1, max(self.layers), max(self.layers)))
		for i in range(0, len(self.layers)-1):
			#Set the necessary range of weights to be random based off of layers. 
			self.weights[i,0:self.layers[i],0:self.layers[i+1]] = 2 * np.random.rand(self.layers[i],self.layers[i+1]) - 1
		#print(self.weights)

	def forwardProp(self, inputLayer):
		#Make it rectangle, and based off of the layers array.
		a = np.zeros((len(self.layers), max(self.layers)))
		z = np.zeros((len(self.layers), max(self.layers)))
		#Set the first layer of nodes equal to the inputed imput layer.
		a[0] = inputLayer
		z[0] = inputLayer
		for layer in range(1, len(a)):
			#For each layer, take the dotproduct of each node and the Weights conencted to it, and store that as the next layers.
			#Keeps unused nodes at 0 because all weights going there are 0 
			#Sigmoid the Z
			z[layer] = np.dot(a[layer-1], self.weights[layer-1])
			#Only Sigmoid the needed ones.
			a[layer,0:self.layers[layer]] = self.sigmoid(z[layer,0:self.layers[layer]])
			#print(a[layer], type(a[layer]))
		#print(a)
		#print(z)
		return a, z #self.removeTralingZeroes(a[-1])

	def removeTralingZeroes(self, ndarray):
		#First Get a Tuple with an array of indexes where the array isn't equal to 0
		# np.nonzero(ndarray != 0)
		#Then get the array from that tuple
		# np.nonzero(ndarray != 0)[0]
		#Then Get the last non zero number
		# np.nonzero(ndarray != 0)[0][-1]
		#Then the last zero, or the end of the array is in the next index
		# np.nonzero(ndarray != 0)[0][-1] + 1
		#So then get and return the origonal array from the start through but not including the index of this last zero
		return ndarray[:np.nonzero(ndarray != 0)[0][-1] + 1] 
		#Confirmed to work when there are zeroes in the middle and if there are no traling zeros. :)

	def addTralingZeroes(self, array, wantedLength):
		#Make a zero array of the wanted longer length
		newArray = np.zeros(wantedLength)
		#make the first portion of that 0's array what the inputed array was.
		newArray[0:len(array)] = array
		return newArray

	def backProp(self, inputLayer, expectedOutputLayer):
		#Make an expectedOuts array that fits the size of the other arrays.
		expectedOutputLayer = self.addTralingZeroes(expectedOutputLayer,max(self.layers))
		#Returns adjustments for each weight
		dwL = np.zeros((len(self.layers)-1,max(self.layers),max(self.layers)))
		#Running Derivitive for layers. Going backwards through backpropogation
		rD = np.zeros((len(self.layers), max(self.layers)))
		#A and Z arrays from the forward Propogation.
		a, z = self.forwardProp(inputLayer)
		#Go Backwards throught the weight layers. Not Including the last layer.
		for layer in range(len(a)-1,0,-1): 
			#print(f"layer, {layer}")
			if(layer == len(a)-1):
				#First Layer, special case
				rD[layer] = 2 * (a[-1] - expectedOutputLayer)
				#print(rD)
			else:
				for node in range(0,len(a[layer])):
					rD[layer,node] = np.sum([rD[layer+1,llNode] * self.sigmoid(z[layer+1,llNode], True) * self.weights[layer,node,llNode] for llNode in range(0,len(a[layer+1]))])
					#rD[layer,node] = np.sum(np.nan_to_num([dwL[layer,node,llNode] / a[layer,node] 		* self.weights[layer,node,llNode] for llNode in range(0,len(a[layer+1]))]))

					#llNode = last layer node
					#print(f"len: {a[layer+1]}")
					#print(f"1: {[rD[layer+1,ll] * self.sigmoid(z[layer+1,ll], True) * self.weights[layer,node,ll] for ll in range(0,len(a[layer+1]))]}, {[dwL[layer,node,ll] / a[layer+1,ll] for ll in range(0,len(a[layer+1]))]}")
					#print(f"{[dwL[layer,node,ll] for ll in range(0,len(a[layer+1]))]} , {[a[layer,ll] for ll in range(0,len(a[layer]))]}")
					# if(node == 0):
					#print(f"OTHER: layer: {layer} dwL: {dwL[layer,node,0]}, rD: {rD[layer+1,0]}, sig: {self.sigmoid(z[layer+1,0], True)}, a {a[layer,0]}")#" full a {a}")
					#print(f"out {[dwL[layer,node,llNode] / a[layer,node] for llNode in range(0,len(a[layer+1]))]}")
					#print(f"NODE: {node} val: {val} , {rD[layer+1]},  {self.weights[layer,node]}")
			#print(f"rD: {rD}")

			for lNode in range(0,len(a[layer-1])):
				dwL[layer-1,lNode] = rD[layer] * self.sigmoid(z[layer], True) * a[layer-1,lNode]
				#The derivitive for the weights for a certain left node are the running derivitive from the last layer element wise multiplied with the derivitive sigmoid from the previous layer, and finally, the current node because they all connect to it.
				#print(f"lNode: {lNode}, {rD[layer] * self.sigmoid(z[layer], True)}")
				#if(layer == 2):
					#print(f"layer {layer} dwL: {dwL[layer-1,lNode]}, rD: {rD[layer]}, sig: {self.sigmoid(z[layer], True)}, a {a[layer,lNode]}")
					#pass
			#print(f"dwL: {dwL} W: {self.weights}")
		self.weights -= dwL


# np.random.seed(1)

# myLayers = [8,5,3]
# myIns = np.ones(8)
#myIns[4] = 0

# expectedOuts = [0,0,1]





# dave = ML(myLayers)
#myOuts = dave.forwardProp(myIns)
#print(myOuts)
#changes = dave.backProp(myIns, expectedOuts)
#print(changes)

# arr = np.array([1,2,0])
# brr = np.array([1,1,0])

# crr = arr/brr 
# print(f"crr {crr}")
# #print(np.sum(crr))
# print(crr[2])
# print(crr[2] == crr[2])
# print(np.isnan(crr[2]))
# print(np.array(0) / np.array(0))
# print(np.nan_to_num(crr))

# for ele in crr:
# 	if(np.isnan(ele)):
# 		print("I AM NAN")
# 	else:
# 		print("I AM NOT NAN")


'''
ins = 	[	[1,0,0],
			[1,1,0],
			[0,0,0],
			[1,1,0]	]
#'''

'''
outs = [	[0],
			[1],
			[0],
			[1]	]
#'''

'''
newLayers = [3,1]
bot = ML(newLayers)

examples = 10

for i in range(0,examples):
	bot.backProp(ins[i%4],outs[i%4])
print(bot.weights)
for i in range(0,len(ins)):
	a,z = bot.forwardProp(ins[i])
	print(a[-1])
#'''