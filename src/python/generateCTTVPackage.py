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

def generate_classes(skeleton, bCreateFile, propertyName=None, parentName=None, depth=0):
    '''
     This method generates all the python classes representing evidence string concepts
     as defined in the JSON Schema definition.
     It creates simple constructor, deep-copy constructors, validation methods to check
     if required fields are defined, in the correct format (date, email) or following a
     specific pattern rule (identifiers, etc.)
    '''
    myMap = {}
    myMap['attributes'] = {}
    myMap['classes'] = list()
    myMap['isAClass'] = False
    baseindent = "  "
    textindent = baseindent*depth
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
                    childMap = generate_classes(skeleton['properties'][attribute_key], False, attribute_key, className, depth+1)
                    myMap['attributes'][attribute_key] = childMap
                    # extends the classes definition with the one from this map
                    myMap['classes'].extend(childMap['classes'])
            elif (className == 'AssociationScore'):
                # this is a hack since the JSON Schema is not consistent
                for attribute_key in ['probability', 'pvalue']:
                    childMap = generate_classes(skeleton[attribute_key], False, attribute_key, className, depth+1)
                    myMap['attributes'][attribute_key] = childMap
                    # extends the classes definition with the one from this map
                    myMap['classes'].extend(childMap['classes'])
            elif (className == 'EvidenceProperties'):
                '''
                 this is a hack since the JSON Schema is not consistent in the way
                 concepts are defined.
                '''
                for attribute_key in ['experiment_specific', 'evidence_chain']:
                    childMap = generate_classes(skeleton[attribute_key], False, attribute_key, className, depth+1)
                    myMap['attributes'][attribute_key] = childMap
                    # extends the classes definition with the one from this map
                    myMap['classes'].extend(childMap['classes'])					
            elif (className == 'ProbabilityScore' or className == 'PValueScore'):
                # this is a hack since the JSON Schema is not consistent
                for attribute_key in ['value', 'method']:
                    childMap = generate_classes(skeleton[attribute_key], False, attribute_key, className, depth+1)
                    myMap['attributes'][attribute_key] = childMap
                    # extends the classes definition with the one from this map
                    myMap['classes'].extend(childMap['classes'])
            indent = "  "*2
            if propertyName:
                myMap['__init__'] = indent + "\n" + 	indent + "# Name: " + propertyName + "\n"
                myMap['__assign__'] = indent + "self." + propertyName + " = " + propertyName + "\n"
                '''
                 describes properties not accounted for by the "properties" or "patternProperties" keywords
                 If this value is not specified (or is boolean true, then additional properties can contain anything
                 now generate the python code
                '''
                if (skeleton.has_key('additionalProperties')):
                    if (skeleton.has_key('required')) and skeleton['required']:
                        myMap['__init__'] += indent + "self." + propertyName + " = {}\n"
                        myMap['__default__'] = propertyName + " = {}"
                        myMap['__clone__'] = indent + "obj." + propertyName + " = clone." + propertyName + "\n"
                        myMap['__map__'] = indent + "obj." + propertyName + " = map['" + propertyName + "']\n"
                    else:
                        myMap['__init__'] += indent + "self." + propertyName + " = None\n"
                        myMap['__default__'] = propertyName + " = None"
                        myMap['__clone__'] = indent + "if clone." + propertyName + ":\n"
                        myMap['__clone__'] += indent*2 + "obj." + propertyName + " = clone." + propertyName + "\n"
                        myMap['__map__'] = indent + "if map.has_key('" + propertyName + "'):\n"
                        myMap['__map__'] += indent*2 + "obj." + propertyName + " = map['" + propertyName + "']\n"
                    if skeleton.has_key('pattern'):
                        pattern = skeleton['pattern']
                        myMap['__validate__'] = indent + "if not re.match(\""+ pattern +"\"," + propertyName + "):\n"
                        myMap['__validate__'] += indent*2 + "sys.stderr.write(\"WARNING:\t'{0}' for field '"+ propertyName+"' does not match pattern '"+pattern+"'\".format(self."+propertyName+"))\n"
                        #m = re.match("^urn:jsonschema:(.+)$", classId)
                elif myMap['isAClass']:
                    if (skeleton.has_key('required')) and skeleton['required']:
                        myMap['__init__'] += indent + "self." + propertyName + " = " + className + "()\n"
                        myMap['__default__'] = propertyName + " = " + className + "()"
                        myMap['__clone__'] = indent + "obj." + propertyName + " = " + className + "(clone." + propertyName + ")\n"
                        myMap['__map__'] = indent + "if map.has_key('" + propertyName + "'):\n"
                        myMap['__map__'] += indent*2 + "obj." + propertyName + " = " + className + ".fromMap(map['" + propertyName + "'])\n"
                        myMap['__validate__'] = indent + "if not self."+ propertyName +" or self."+ propertyName +" == None :\n"
                        myMap['__validate__'] += indent*2 + "sys.stderr.write(\"ERROR: "+parentName+" - '"+propertyName+"' is required'\\n\")\n"
                        myMap['__validate__'] += indent + "else:\n"
                        myMap['__validate__'] += indent*2 + "self." + propertyName+".validate()\n"                          
                    else:
                        myMap['__init__'] += indent + "self." + propertyName + " = None\n"
                        myMap['__default__'] = indent + propertyName + " = None"
                        myMap['__clone__'] = indent + "if clone." + propertyName + ":\n"
                        myMap['__clone__'] += indent*2 + "obj." + propertyName + " = " + className + "(clone." + propertyName + ")\n"
                        myMap['__map__'] = indent + "if map.has_key('" + propertyName + "'):\n"
                        myMap['__map__'] += indent*2 + "obj." + propertyName + " = " + className + ".fromMap(map['" + propertyName + "'])\n"
            if myMap['isAClass']:
                '''
                 Generate the python class specification with:
                  1. a default initialisation method (init all the attributes by default)
                  2. a constructor will all the fields as arguments with default values
                  3. a deep-copy constructor (clone)
                  4. a map constructor (from json)
                  5. a validation method to validate against the JSON Schema
                '''
                classDefinition = ""
                if classId:
                    classDefinition += "# " + classId + "\n"
                classDefinition += "class " + className + "(object):\n"
                '''
                 1. default initialisation method
                '''
                arrayDefaultValues = []
                classDefinition += baseindent + "def initialise(self):\n"
                for attribute_key in myMap['attributes']:
                    classDefinition += myMap['attributes'][attribute_key]['__init__']
                    arrayDefaultValues.append(myMap['attributes'][attribute_key]['__default__'])
                '''
                 2. and another constructor again but with all attributes as arguments
                    with default values
                '''
                if (len(myMap['attributes'].keys())>0):
                    classDefinition += baseindent+"# Constructor using all fields with default values\n"
                    arguments = ", ".join(arrayDefaultValues)
                    classDefinition += baseindent + "def __init__(self, {0}):\n".format(arguments)
                    for attribute_key in myMap['attributes']:
                        classDefinition += myMap['attributes'][attribute_key]['__assign__']
                '''
                 3. and a deep copy one (clone) as class method
                '''
                classDefinition += baseindent + "@classmethod\n"
                classDefinition += baseindent + "def cloneObject(cls, clone):\n"
                classDefinition += baseindent*2 + "obj = cls()\n"
                for attribute_key in myMap['attributes']:
                    classDefinition += myMap['attributes'][attribute_key]['__clone__']
                classDefinition += baseindent*2 + "return obj\n"
                '''
                 4. and a map copy one (map) as class method
                    check that the parameter passed as an argument is a map
                    initialise all the fields first
                '''
                classDefinition += baseindent + "@classmethod\n"
                classDefinition += baseindent + "def fromMap(cls, map):\n"
                classDefinition += baseindent*2 + "obj = cls()\n"
                classDefinition += baseindent*2 + "if not isinstance(map, types.DictType):\n"
                classDefinition += baseindent*3
                classDefinition += "sys.stderr.write(\"ERROR: {0}".format(parentName)
                classDefinition +=" - DictType expected - {0} found\\n\".format(type(map)))\n"
                classDefinition += baseindent*3 + "return\n"
                for attribute_key in myMap['attributes']:
                    classDefinition += myMap['attributes'][attribute_key]['__map__']
                classDefinition += baseindent*2 + "return obj\n"
                '''
                 5. and a validate method
                '''
                classDefinition += baseindent + "def validate(self):\n"
                for attribute_key in myMap['attributes']:
                    if myMap['attributes'][attribute_key].has_key('__validate__'):
                        classDefinition += myMap['attributes'][attribute_key]['__validate__']
                classDefinition += baseindent*2 + "sys.stderr.flush()\n"
                '''
                 Finally store the class definition in the classes list
                '''
                myMap['classes'].extend(classDefinition)                        
        else:
            '''
             This field is a property of a class:
             1. generate the python code to initialise the variable in the default constructor
             2. generate the python code to initialise the variable in the clone/map constructor
             3. check the field is required or not
             4. validate the value of the field according to regex or format
            '''
            indent = baseindent*2
            myMap['__init__'] = indent + "\n" + indent + "# Name: " + propertyName + "\n"
            myMap['__init__'] += indent + "# Type: " + dataType + "\n"
            myMap['__assign__'] = indent + "self." + propertyName + " = " + propertyName + "\n"
            '''
             Add the description as a comment
            '''
            if (skeleton.has_key('description')):
                myMap['__init__'] += indent + "# Description: " + skeleton['description'] + "\n"
            '''
             Check if the property is required:
               1. if so, the value should be assigned from the deep-copy/map constructor
               2. the validation procedure must check the field exists
            '''
            if (skeleton.has_key('required') and skeleton['required']):
                #'{:%Y-%m-%d %H:%M:%S}'.format, gen
                #myMap['__init__'] += indent + '#Required: {%r}\n'.format %(skeleton['required']))
                myMap['__init__'] += indent + ('#Required: {%r}\n' % (skeleton['required'])) + "\n"
                myMap['__clone__'] = indent + "obj." + propertyName + " = clone." + propertyName + "\n"
                myMap['__map__'] = indent + "if map.has_key('" + propertyName + "'):\n"
                myMap['__map__'] += indent*2 + "obj." + propertyName + " = map['" + propertyName + "']\n"
                myMap['__validate__'] = indent + "if not self."+ propertyName +" or self."+ propertyName +" == None :\n"
                myMap['__validate__'] += indent*2 + "sys.stderr.write(\"ERROR: "+parentName+" - '"+propertyName+"' is required'\\n\")\n"                     
            else:
                myMap['__clone__'] = indent + "if clone." + propertyName + ":\n"
                myMap['__clone__'] += indent*2 + "obj." + propertyName + " = clone." + propertyName + "\n"
                myMap['__map__'] = indent + "if map.has_key('" + propertyName + "'):\n"
                myMap['__map__'] += indent*2 + "obj." + propertyName + " = map['" + propertyName + "']\n"
            '''
             VALIDATION STEP 1: check there is a regular expression rule to apply (for validation)
            '''
            if skeleton.has_key('pattern'):
                pattern = skeleton['pattern']
                myMap['__validate__'] = indent + "# Check regex: "+ pattern +" for validation\n"
                myMap['__validate__'] += indent + "if not re.match(\""+ pattern +"\", self." + propertyName + "):\n"
                myMap['__validate__'] += indent*2 + "sys.stderr.write(\"WARNING: "+parentName+" - "+propertyName+" '{0}' does not match pattern '"+pattern+"'\".format(self."+propertyName+"))\n"
            '''
             VALIDATION STEP 2: check format is correct
            '''
            if (skeleton.has_key('format')):
                # "format": "date-time", "format": "email"
                # we still need to validate those
                myMap['__init__'] += indent + "# String format: " + skeleton['format'] + "\n"
                if not myMap.has_key('__validate__'):
                    myMap['__validate__'] = ""
                if skeleton['format'] == "email":
                    myMap['__validate__'] += indent + "if self." + propertyName + " and not self." + propertyName + " == None and not re.match(\"[\\w.-]+@[\\w.-]+.\\w+\", self." + propertyName + "):\n"
                    myMap['__validate__'] += indent*2 + "sys.stderr.write(\"ERROR: "+parentName+" - "+propertyName+" '{0}' is not a valid email address\\n\".format(self."+propertyName+"))\n"
                elif skeleton['format'] == "date-time":
                    '''
                     This SHOULD be a date in ISO 8601 format of YYYY-MM-DDThh:mm:ssZ in UTC time.  This is the recommended form of date/timestamp
                     However, the ISO 8601 allows for fraction of a second like YYYY-MM-DDThh:mm:ss.sTZD (eg 1997-07-16T19:20:30.45+01:00)
                     So "2014-10-16T13:47:17.000+01:00" would be a valid datetime. 
                     Reference: http://www.w3.org/TR/NOTE-datetime
                    '''
                    myMap['__validate__'] += indent + "if self." + propertyName + " and not self." + propertyName + " == None:\n"
                    myMap['__validate__'] += indent*2 + "try:\n"
                    myMap['__validate__'] += indent*3 + "iso8601.parse_date(self."+propertyName+")\n"
                    myMap['__validate__'] += indent*2 + "except iso8601.iso8601.ParseError, e:\n"
                    myMap['__validate__'] += indent*3 + "sys.stderr.write(\"ERROR: "+parentName+" - "+propertyName+" '{0}' invalid ISO 8601 date (YYYY-MM-DDThh:mm:ss.sTZD expected)\\n\".format(self."+propertyName+"))\n"
            if dataType == 'string':
                '''
                 A string is initialised to None by default
                '''
                myMap['__init__'] += indent + "self." + propertyName + " = None\n"
                myMap['__default__'] = propertyName + " = None"
            elif dataType == 'boolean':
                '''
                 A boolean is initialised to False by default
                '''
                myMap['__init__'] += indent + "self." + propertyName + " = False" + "\n"
                myMap['__default__'] = propertyName + " = False"
            elif dataType == 'number':
                '''
                 A number is initialised to nought by default
                '''
                myMap['__init__'] += indent + "self." + propertyName + " = 0\n"
                myMap['__default__'] = propertyName + " = 0"
                '''
                 Constraints specific to numbers:
                  minimum, 
                  maximum, 
                  exclusiveMaximum, 
                  exclusiveMinimum
                '''
                constraint = []
                message = []
                if (skeleton.has_key('minimum')):
                    minimum = skeleton['minimum']
                    constraint.append("self.{0} > {1}".format(propertyName, minimum) if (skeleton.has_key('exclusiveMinimum')) else "self.{0} >= {1}".format(propertyName, minimum))
                    message.append("should be greater than {0}".format(minimum) if (skeleton.has_key('exclusiveMinimum')) else "should be greater than or equal to {0}".format(minimum))
                if (skeleton.has_key('maximum')):
                    maximum = skeleton['maximum']
                    constraint.append("self.{0} < {1}".format(propertyName, maximum) if (skeleton.has_key('exclusiveMaximum')) else "self.{0} <= {1}".format(propertyName, maximum))
                    message.append("should be lower than {0}".format(minimum) if (skeleton.has_key('exclusiveMaximum')) else "should be lower than or equal to {0}".format(maximum))
                if (len(constraint)>0):
                    if not myMap.has_key('__validate__'):
                        myMap['__validate__'] = ""
                    myMap['__validate__'] += indent + "if {0}:".format(" or ".join(constraint))
                    myMap['__validate__'] += indent*2 + "sys.stderr.write(\"ERROR: {0} - '{1}' {2}\\n\")\n".format(parentName, propertyName, " and ".join(message))                    
            elif dataType == 'array':
                '''
                 An array is created empty by default
                '''
                myMap['__init__'] += indent + "self." + propertyName + " = []\n"
                myMap['__default__'] = propertyName + " = []"
                '''
                 There are some constraints specific to arrays:
                   minItems
                '''
                if (skeleton.has_key('minItems')):
                    if not myMap.has_key('__validate__'):
                        myMap['__validate__'] = ""
                    myMap['__validate__'] += indent + "if self.{0} == None or len(self.{0}) <= {1}:\n".format(propertyName, skeleton['minItems'])
                    myMap['__validate__'] += indent*2 + "sys.stderr.write(\"ERROR: {0} - '{1}' array should have at least {2} elements\\n\")\n".format(parentName, propertyName, skeleton['minItems'])
                if (skeleton.has_key('maxItems')):
                    if not myMap.has_key('__validate__'):
                        myMap['__validate__'] = ""
                    myMap['__validate__'] += indent + "if self.{0} == None or len(self.{0}) >= {1}:\n".format(propertyName, skeleton['maxItems'])
                    myMap['__validate__'] += indent*2 + "sys.stderr.write(\"ERROR: {0} - '{1}' array should have at most {2} elements\\n\")\n".format(parentName, propertyName, skeleton['maxItems'])
                if (skeleton.has_key('uniqueItems')):
                    if not myMap.has_key('__validate__'):
                        myMap['__validate__'] = ""
                    myMap['__validate__'] += indent + "if self.{0} == None or len(set(self.{0})) != len(self.{0}):\n".format(propertyName)
                    myMap['__validate__'] += indent*2 + "sys.stderr.write(\"ERROR: {0} - '{1}' array have duplicated elements\\n\")\n".format(parentName, propertyName)               
               
    else:
        '''
         This data type is unknown
        '''
        print textindent + "Can't process type %s" %(type(skeleton))
    if bCreateFile:
        # dump
        #classfile.write('\n'.join(myMap['classes']))
        classfile.write('import re\nimport sys\nimport iso8601\nimport types\n')
        for c in myMap['classes']:
            classfile.write(c)
        classfile.close()
    return myMap
    
def generate_setup():
    setupString = "from setuptools import setup\n"
    setupString += "	setup(name='org.cttv.input.model',\n"
    setupString += "version='0.1',\n"
    setupString += "description='CTTV data model',\n"
    setupString += "url='http://github.com/CTTV',\n"
    setupString += "author='Gautier Koscielny',\n"
    setupString += "author_email='gautier.x.koscielny@gsk.com',\n"
    setupString += "license='Apache2',\n"
    setupString += "packages=['org.cttv.input.model'],\n"
    setupString += "zip_safe=False)\n"


# read directly from the URL
data = urlopen( options.json_schema_uri ).read()
decoded = json.loads(data)
generate_classes(decoded, True)
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

