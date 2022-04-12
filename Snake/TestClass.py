import numpy as np

class ExampleClass:
	data = 8

	def __init__(self):
		pass

	def getData(self):
		return self.data

	def setData(self, data):
		self.data = data

dave = ExampleClass()

#print(f"Data 1: {dave.getData()}")
dave.setData(19)
#print(f"Data 2: {dave.getData()}")

#OPTION FOR ML
#MAKE THE ARRAY RECTANGLE AND HAVE 0's IN EXTRA SPOTS.

y = np.arange(35).reshape((5,7))
#print(y)
#print(y[1:5:2]) #The Second Colon is the increment. Like a range. Start: 1, End but dont include: 5, Increment:2, aka [1,3]
#print(y[1:5:2,::3]) #This one means full range like [:] means full range Increment 3. aka [0,3,6]

#print(y[np.array([0,2,4]), np.array([0,1,2])]) #Outer Arrays, 0,2,4 at positions 0,1,2. Does Element wise. I would think 9 points given, but only 3. 0:3, or 0:5:2 instead of 0,1,2/0,2,4 gives 9 pts

layers = [8,5,3]


rD = np.zeros([len(layers), max(layers)])
w = np.zeros([len(layers)-1, max(layers), max(layers)])

#print(rD)
#print(type(rD))
#print()
#print(w)
#print(rD[:,[3,5,8]])

def deleteTraling0s(ndarray):
	# nz = np.nonzero(ndarray == 0)
	# print(f"NZ: {nz}")
	# print(nz[0])
	# print(nz[0][0])

	#where = np.where(ndarray == 0, True, False) #Parameters, Conditional, If condition for element is true, pick element at same index of param 2, else pick element at same index of param 3
	#print(F"Where: {where}")
	#print(type(where))
	#print(where[0])
	#print(where[0][0])
	#print(where[0,0]) #Doesn't work
	#return 0
	#num = round(float(np.where(ndarray==0,ndarray,ndarray)[0]))
	#print(num)
	#print(type(num))
	#return ndarray[:round(float(np.where(ndarray==0,ndarray,ndarray)[0]))] #NEED TO ROUND AND CAST TO A FLoAT BECAUYSE IT RETURNS A NP.FLOAT which doesnt work well with round.



	# First Get a Tuple with an array of indexes where the array isn't equal to 0
	# np.nonzero(ndarray != 0)
	# Then get the array from that tuple
	# np.nonzero(ndarray != 0)[0]
	# Then Get the last non zero number
	# np.nonzero(ndarray != 0)[0][-1]
	# Then the last zero, or the end of the array is in the next index
	# np.nonzero(ndarray != 0)[0][-1] + 1
	# So then get and return the origonal array from the start through but not including the index of this last zero
	return ndarray[:np.nonzero(ndarray != 0)[0][-1] + 1] 
	# Confirmed to work when there are zeroes in the middle and if there are no traling zeros. :)

rD[:,0:3] = [1,2,3]
#print(rD)
#print(rD[0])
#print(deleteTraling0s(rD[0]))

a = np.arange(9,-1,-1)
a[5] = 0
print(a)
print(deleteTraling0s(a))
#print(np.where(a < 5, a, 10*a))
