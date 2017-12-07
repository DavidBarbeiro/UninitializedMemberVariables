import re
import glob, os
import sys

results = []

def readFile(filename):
	try:
		file = open(filename, 'r') 
		content = file.read()
		file.close()
		return content
	except IOError:
		return -1

def processHeader(filename):
	print "Parsing " + filename
	content = readFile(filename)
	content = removeComments(content)

	if (content.find("@interface") == -1):
		return

	pointerDeclarationList = []
	for match in re.findall("\n\s+\w+ *\*.*;", content):
		matchList = re.findall("\w+", match)
		if len(matchList) > 1:
			pointerDeclarationList.append(matchList[1])
	print pointerDeclarationList
	processImplementation(pointerDeclarationList,filename)

def processImplementation(pointerDeclarationList,filename):
	implementationExtensions = [".mm",".m"]
	dotIndex = filename.rfind(".")
	baseFilename = filename[:dotIndex]
	for extension in implementationExtensions:
		filename = baseFilename + extension
		content = readFile(filename)
		if content<0:
			continue
		content = removeComments(content)
		p = re.compile(" *[-+]\s*\(\s*\w*\s*[*&]*\s*\)\s*\w*(?:init|setup).*?{",re.DOTALL)
		for initMethod in p.findall(content):
			pointerIsInitialized(content,initMethod,pointerDeclarationList,filename)
	for pointer in pointerDeclarationList:
		results.append([pointer,filename])

def pointerIsInitialized(content,initMethod,pointerDeclarationList,filename):
	index = content.find(initMethod)
	index += len(initMethod) + 1
	initMethodBeginIndex = index-1
	bracketStackCount = 1
	while bracketStackCount != 0 and index < len(content):
		if content[index] == '{':
			bracketStackCount += 1
		elif content[index] == '}':
			bracketStackCount -= 1
		index+=1
	initMethod = content[initMethodBeginIndex:index]
	lines = initMethod.splitlines()
	for line in lines:
		for pointerName in pointerDeclarationList:
			match = re.match("\s*" + pointerName + "\s*=",line)
			if match is not None:
				pointerDeclarationList.remove(pointerName)

def removeComments(string):
    string = re.sub(re.compile("/\*.*?\*/",re.DOTALL ) ,"" ,string) # remove all occurance streamed comments (/*COMMENT */) from string
    string = re.sub(re.compile("//.*?\n" ) ,"" ,string) # remove all occurance singleline comments (//COMMENT\n ) from string
    return string


def walklevel(some_dir):
	paths = []
	for subdir, dirs, files in os.walk(some_dir):
	    for file in files:
	        paths.append(os.path.join(subdir, file))
	return paths

def filterHeaderFiles(filename):
	if filename.find("libs")>0:
		return False

	fileExtension = filterExtension(filename)
	if(fileExtension == "h" or fileExtension == "hpp"):
		return True
	return False

def filterImplementationFiles(filename):
	fileExtension = filterExtension(filename)
	if(fileExtension == "mm" or fileExtension == "cpp"):
		return filename

def filterExtension(filename):
	dotIndex = filename.rfind(".")
	if(dotIndex>0):
		return filename[dotIndex+1:]

def printResults():
	print "\n------Printing results:------\n"
	for result in results:
		print "Uninitialized pointer " + result[0] + " in file " + result[1]

def main():
	if(len(sys.argv) != 2):
		print("usage: pointerInitialisation.py [Path of root]")
		return

	print "\n------Started execution------\n"

	dir_path = os.path.dirname(os.path.realpath(sys.argv[1]))
	paths = walklevel(dir_path)

	for filename in paths:
		if filterHeaderFiles(filename):
			content = processHeader(filename)

	printResults()
	return 1

main()
