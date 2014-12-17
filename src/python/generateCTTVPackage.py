from urllib2 import *
from pprint import pprint
import python_jsonschema_objects as pjs
import json 
import copy
import sys
import re
import shutil
import optparse

parser = optparse.OptionParser()
parser.add_option('-d', '--directory', default='../../build', dest='exportDirectory')
parser.add_option('-u', '--uri', default='https://raw.githubusercontent.com/CTTV/input_data_format/master/json_schema/evidence_string_schema.json', dest='json_schema_uri')

options, args = parser.parse_args()

pattern = re.compile('^urn:jsonschema:(.+)$')
classfile = 0

if not os.path.exists(options.exportDirectory):
    os.makedirs(options.exportDirectory)

def generate_classes(skeleton, bCreateFile, propertyName, depth):
	myMap = {}
	myMap['attributes'] = {}
	myMap['classes'] = list()
	myMap['isAClass'] = False
	textindent = "\t"*depth
	print textindent + "--------------"
	if propertyName:
		print textindent + propertyName
	print textindent + ','.join(skeleton.keys())
	if (type(skeleton) is dict):
		if (type(skeleton['type']) is list):
			print textindent + "DataType: %s" %(','.join(skeleton['type']))
			# horrible hack
			dataType = skeleton['type'][0]
		else:
			dataType = skeleton['type']
			print textindent + "DataType: %s" %(dataType)
			
		if dataType == 'object':
			className = None
			if (skeleton.has_key('id')):
				myMap['isAClass'] = True
				classId = skeleton['id']
				print textindent + classId
				# get the properties and call recursively
				# urn:jsonschema:org:cttv:input:model:EvidenceProperties
				m = re.match("^urn:jsonschema:(.+)$", classId)
				if m:
					result = m.groups()[0]
					# split path and className
					p = re.compile(r':')
					raw = p.split(result)
					len(raw)
					dirpath = '/'.join(raw[:len(raw)-1])
					print textindent + dirpath
					print textindent + raw[-1]
					className = raw[-1]
					if bCreateFile:
						# remove existing package to replace with new version
						if os.path.exists(options.exportDirectory + "/" + raw[0]):
							shutil.rmtree(options.exportDirectory + "/" + raw[0])
						# create directory recursively
						if not os.path.exists(options.exportDirectory + "/" + dirpath):
							os.makedirs(options.exportDirectory + "/" + dirpath)
						# create an init file recursively too (use the raw variable)
						index = 0
						for i in range(len(raw)-1):
							# __init__.py
							classfile = open(options.exportDirectory + "/" + "/".join(raw[index:i]) + "/__init__.py", 'w')
							classfile.write('#package ' + ".".join(raw[index:i]))
							classfile.close()
						# Finally create a file there and keep the file handler open
						classfile = open(options.exportDirectory + "/" + dirpath + "/__init__.py", 'w')
			if (skeleton.has_key('properties')):
				for attribute_key in skeleton['properties']:
					childMap = generate_classes(skeleton['properties'][attribute_key], False, attribute_key, depth+1)
					myMap['attributes'][attribute_key] = childMap
					# extends the classes definition with the one from this map
					myMap['classes'].extend(childMap['classes'])
			elif (className == 'AssociationScore'):
				# this is a hack since the JSON Schema is not consistent
				for attribute_key in ['probability', 'pvalue']:
					childMap = generate_classes(skeleton[attribute_key], False, attribute_key, depth+1)
					myMap['attributes'][attribute_key] = childMap
					# extends the classes definition with the one from this map
					myMap['classes'].extend(childMap['classes'])
			elif (className == 'EvidenceProperties'):
				# this is a hack since the JSON Schema is not consistent
				for attribute_key in ['experiment_specific', 'evidence_chain']:
					childMap = generate_classes(skeleton[attribute_key], False, attribute_key, depth+1)
					myMap['attributes'][attribute_key] = childMap
					# extends the classes definition with the one from this map
					myMap['classes'].extend(childMap['classes'])					
			elif (className == 'ProbabilityScore' or className == 'PValueScore'):
				# this is a hack since the JSON Schema is not consistent
				for attribute_key in ['value', 'method']:
					childMap = generate_classes(skeleton[attribute_key], False, attribute_key, depth+1)
					myMap['attributes'][attribute_key] = childMap
					# extends the classes definition with the one from this map
					myMap['classes'].extend(childMap['classes'])
			# describes properties not accounted for by the "properties" or "patternProperties" keywords
			# If this value is not specified (or is boolean true, then additional properties can contain anything
			# now generate the python code
			indent = "\t"*2
			if propertyName:
				myMap['__init__'] = indent + "\n" + 	indent + "# Name: " + propertyName + "\n"
				if (skeleton.has_key('additionalProperties')):
					if (skeleton.has_key('required')) and skeleton['required']:
						myMap['__init__'] += indent + "self." + propertyName + "= {}\n"
					else:
						myMap['__init__'] += indent + "self." + propertyName + "= None\n"
				elif myMap['isAClass']:
					myMap['__init__'] += indent + "self." + propertyName + "= " + className + "()\n"
			if myMap['isAClass']:
				
				# generate the python class specification
				classDefinition = ""
				if classId:
					classDefinition += "# " + classId + "\n"
				classDefinition += "class " + className + "(object):\n"
				classDefinition += "\tdef __init__(self):\n"
				for attribute_key in myMap['attributes']:
					classDefinition += myMap['attributes'][attribute_key]['__init__']
				myMap['classes'].extend(classDefinition)
		else:
			# this is a property of a class, we generate the python code to initialise the variable in the default 
			# constructor
			indent = "\t"*2
			myMap['__init__'] = indent + "\n" + indent + "# Name: " + propertyName + "\n"
			myMap['__init__'] += indent + "# Type: " + dataType + "\n"
			if (skeleton.has_key('description')):
				myMap['__init__'] += indent + "# Description: " + skeleton['description'] + "\n"
			if (skeleton.has_key('required')):
				#'{:%Y-%m-%d %H:%M:%S}'.format, gen
				#myMap['__init__'] += indent + '#Required: {%r}\n'.format %(skeleton['required']))
				myMap['__init__'] += indent + ('#Required: {%r}\n' % (skeleton['required'])) + "\n"
			if (skeleton.has_key('format')):
				myMap['__init__'] += indent + "# String format: " + skeleton['format'] + "\n"
			if dataType == 'string':
				myMap['__init__'] += indent + "self." + propertyName + " = None\n"
			elif dataType == 'boolean':
				myMap['__init__'] += indent + "self." + propertyName + " = False" + "\n"
			elif dataType == 'number':
				myMap['__init__'] += indent + "self." + propertyName + " = 0\n" 
			elif dataType == 'array':
				myMap['__init__'] += indent + "self." + propertyName + " = []\n"
	else:
		print textindent + "Can't process type %s" %(type(skeleton))
	if bCreateFile:
		# dump
		#classfile.write('\n'.join(myMap['classes']))
		for c in myMap['classes']:
			classfile.write(c)
		classfile.close()
	return myMap
	
def generate_setup():
	setupString = "from setuptools import setup\n"
	setupString += "	setup(name='org.targetvalidation',\n"
	setupString += "version='0.1',\n"
	setupString += "description='Python class and validation generator',\n"
	setupString += "url='http://github.com/CTTV',\n"
	setupString += "author='Gautier Koscielny',\n"
	setupString += "author_email='cttv@targetvalidation.org',\n"
	setupString += "license='Apache2',\n"
	setupString += "packages=['org.targetvalidation'],\n"
	setupString += "zip_safe=False)\n"  


# read directly from the URL
data = urlopen( options.json_schema_uri ).read()
decoded = json.loads(data)
generate_classes(decoded, True, 0, 0)
generate_setup()

#pprint(data)

# try to deserialize the json file
#with open("evidence_string_schema.json") as json_file:
#     json_data = json.load(json_file)
#     pprint(json_data)

print 'DECODED :', type(decoded)

print 'The package has been generated in ', options.exportDirectory
# exit here
sys.exit()

