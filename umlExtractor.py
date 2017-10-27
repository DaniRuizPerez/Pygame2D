    # -*- encoding: utf-8 -*-
import glob, os, re
output_name = "uml.txt"
output = open(output_name, 'w')

#Get all class names ->     m = re.findall('class (.*)\(.*\):', file_str)

def extract(file_str, filename):

	output.write( "Fichero: " + filename + "\n" )
	class_names = re.findall('class (.*):', file_str)
	class_bodies = re.split('class .*\(.*\):.*', file_str)
	for i in range (1, len(class_bodies)):
		output.write( "\tClase: " + str(class_names[i-1]) + "\n" )
		write_matches("\tMetodos: \n", 'def (.*):', class_bodies[i])	
		write_matches("\tAtributos: \n", 'self\.([^.\s\n()\.\,\;\[\]+-\:]+)[=\s\.\[\,\;\:]', class_bodies[i])
	output.write("\n")

def write_matches(header, regex, string_were_we_look_for):
	container = re.findall(regex, string_were_we_look_for)
	container = sorted(set(container))
	output.write(header)
	for thing in container:
		output.write( "\t\t" + str(thing)+ "\n")
	output.write( "\n")


ignoredFiles = ['__init__.py', 'umlextractor.py', 'main.py', 'print_detector.py']
ext='.py'



for root, dirs, files in os.walk('.'):
    for currentFile in files:
        if currentFile.lower().endswith(ext) and currentFile.lower() not in ignoredFiles:
            file = open(os.path.join(root, currentFile), 'r')
            extract(file.read(), currentFile)

print "Generado archivo " + output_name + " con las firmas, atributos y herencias"

