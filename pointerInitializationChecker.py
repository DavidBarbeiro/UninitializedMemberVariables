import re
import glob, os

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
	content = readFile(filename)
	content = removeComments(content)
	for match in re.findall("\w+ *\*.*;", content):
		checkForPointerDeclaration(match,filename)

def processImplementation(pointerName,filename):
	implementationExtensions = [".mm",".cpp",".m"]
	dotIndex = filename.index(".")
	baseFilename = filename[:dotIndex]
	for extension in implementationExtensions:
		filename = baseFilename + extension
		content = readFile(filename)
		if content<0:
			continue
		print "process" + filename
		content = removeComments(content)
		#p = re.compile(" *[-+]\s*\(\s*\w*\s*[*&]*\s*\)\s*\w*init\w*\s*{",re.DOTALL)
		p = re.compile(" *[-+]\s*\(\s*\w*\s*[*&]*\s*\)\s*\w*init\w*\s*{",re.DOTALL)
		for initMethod in p.findall(content):
			print "yay"
			print initMethod
			if pointerIsInitialized(initMethod,pointerName,filename):
				return
		
	results.append([pointerName,filename])

def checkForPointerDeclaration(pointerName,filename):
	print "checkForPointerDeclaration" + pointerName
	matchList = re.findall("\w+", pointerName)
	processImplementation(matchList[1],filename)

def pointerIsInitialized(initMethod,pointerName,filename):
	lines = initMethod.splitlines()
	for line in lines:
		match = re.match("\s*" + pointerName + "\s*=",line)
		if match is not None:
			return True
	return False

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
	fileExtension = filterExtension(filename)
	if(fileExtension == "h" or fileExtension == "hpp"):
		return filename

def filterImplementationFiles(filename):
	fileExtension = filterExtension(filename)
	if(fileExtension == "mm" or fileExtension == "cpp"):
		return filename

def filterExtension(filename):
	dotIndex = filename.index(".")
	if(dotIndex>0):
		return filename[dotIndex+1:]

def printResults():
	for result in results:
		print "Uninitialized pointer " + result[0] + " in file " + result[1]

def main():
	print "\n\n\n\n\n"
	dir_path = os.path.dirname(os.path.realpath(__file__))
	paths = walklevel(dir_path)

	for filename in paths:
		if filterHeaderFiles(filename):
			content = processHeader(filename)

	printResults()
	return 1

main()