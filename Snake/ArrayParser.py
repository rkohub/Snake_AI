import numpy as np

def parseArray(arrayStr):
	start = arrayStr.find("[")
	end = arrayStr.rfind("]")
	print(start,end)
	if(start == -1 and end == -1):
		print(arrayStr)
		return
	nestedArrayStr = arrayStr[start+1:end]
	parseArray(nestedArrayStr)

	pass


#npA = np.arange(40, dtype = float).reshape(2,2,10)
npA = np.arange(5, dtype = float)

#print(npA)
#print(repr(npA))

#'''
file = open("./Storage/Gen0.txt",'w')
#The repr() function returns a printable representational string of the given object.
file.write(repr(npA))
file.close()
#'''


#'''
fileStr = open("./Storage/Gen0.txt",'r').read()
print(fileStr)
#Remove tabs, new lines and spaces.
fileStr = fileStr.replace("\t","").replace("\n","").replace(" ","")
print(fileStr)
parseArray(fileStr)
#'''