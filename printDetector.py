    # -*- encoding: utf-8 -*-
import glob, os, re

#Get all class names ->     m = re.findall('class (.*)\(.*\):', file_str)

def extract(file_str, filename):

	class_names = re.findall('print', file_str)
	if len(class_names) != 0:
		print "File " + filename + " has prints"

def write_matches(header, regex, string_were_we_look_for):
	container = re.findall(regex, string_were_we_look_for)
	container = sorted(set(container))
	output.write(header)
	for thing in container:
		output.write( "\t\t" + str(thing)+ "\n")
	output.write( "\n")


ignoredFiles = ['__init__.py', 'umlextractor.py', 'main.py', 'printDetector.py']
ext='.py'



for root, dirs, files in os.walk('.'):
    for currentFile in files:
        if currentFile.lower().endswith(ext) and currentFile.lower() not in ignoredFiles:
            file = open(os.path.join(root, currentFile), 'r')
            extract(file.read(), currentFile)
