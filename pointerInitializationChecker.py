import re
import glob, os

def readFile(fileName):
	file = open(fileName, 'r') 
	content = file.read()
	file.close()
	return content

def processHeader(fileName):
	content = readFile(fileName)
	print content
	print "***************\n"
	for match in re.findall("\w+ *\*.*;", content):
		checkForPointerName(match,fileName)

def processImplementation(match,fileName):
	print match
	fileName = fileName[:-2] + ".mm"
	content = readFile(fileName)
	p = re.compile("\w*init\w* *\{.*}",re.DOTALL)
	matchList = p.findall(content)
	print matchList


def checkForPointerName(content,fileName):
	print content
	matchList = re.findall("\w+", content)
	processImplementation(matchList[1],fileName)



def main():
	#os.chdir("src")
	for filename in glob.glob("*.h"):
	    content = processHeader(filename)




main()