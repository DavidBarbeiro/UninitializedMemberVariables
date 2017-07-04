import re
import glob, os

def readFile(fileName):
	file = open(fileName, 'r') 
	content = file.read()
	file.close()
	return content

def processHeader(fileName):
	content = readFile(fileName)
	checkForPointer(content,fileName)

def processImplementation(match,fileName):
	print match
	file = readFile(fileName)
	#checkForPointer(content,fileName)

def checkForPointer(content,fileName):
	print content
	print "***************\n"
	for match in re.findall("\w+ *\*.*;", content):
		checkForPointerName(match,fileName)

def checkForPointerName(content,fileName):
	print content
	matchList = re.findall("\w+", content)
	processImplementation(matchList[1],fileName)



def main():
	os.chdir("src")
	for file in glob.glob("*.h"):
	    content = processHeader(file)




main()