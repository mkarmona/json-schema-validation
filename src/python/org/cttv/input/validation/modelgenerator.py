"""
.. module:: useful_1
   :platform: Unix, Windows
   :synopsis: This script generates the CTTV package for JSON Schema validation

.. moduleauthor:: Gautier Koscielny <gautier.x.koscielny@gsk.com>

"""

from urllib2 import *
from pprint import pprint
#import python_jsonschema_objects as pjs
import json 
import copy
import sys
import re
import shutil
import optparse
import shutil

requirements = '''
nose>=1.3.4
tox>=1.7.0
wheel>=0.22.0
iso8601>=0.1.10
'''

manifest = '''
recursive-include org *.py
include README.rst LICENSE tox.ini setup.py *requirements.txt
'''

tox = '''
[tox]
envlist = py27

[testenv]
deps=-r{toxinidir}/requirements.txt
changedir={toxinidir}/org/cttv/input/model/tests
commands=nosetests
#deps= -rrequirements.txt
#commands=py.test --verbose org/cttv/input/model/test_org_cttv_input_model.py
setenv =
    LC_ALL=C
'''

setup = '''
import os

try:
    from setuptools import setup
except ImportError:
    from distutils import setup

long_description = open(os.path.join(os.path.dirname(__file__), "README.rst")).read()

setup(
    name="org.cttv.input.model",
    version="0.1.1",
    description=long_description.split("\\n")[0],
    long_description=long_description,
    author="Gautier Koscielny",
    author_email="gautier.x.koscielny@gsk.com",
    url="https://github.com/CTTV",
    #packages=find_packages('.'),
    #package_dir = {'': '.'},
    #namespace_packages = ["org", "org.cttv", "org.cttv.input"],    
    packages=["org.cttv.input.model"],
    license="Apache2",
    classifiers=[
        "License :: Apache 2",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
)

'''

readme = '''
Simple module to validate, compare and generate CTTV evidence strings

'''

license = '''

                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.

      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.

      "Legal Entity" shall mean the union of the acting entity and all
      other entities that control, are controlled by, or are under common
      control with that entity. For the purposes of this definition,
      "control" means (i) the power, direct or indirect, to cause the
      direction or management of such entity, whether by contract or
      otherwise, or (ii) ownership of fifty percent (50%) or more of the
      outstanding shares, or (iii) beneficial ownership of such entity.

      "You" (or "Your") shall mean an individual or Legal Entity
      exercising permissions granted by this License.

      "Source" form shall mean the preferred form for making modifications,
      including but not limited to software source code, documentation
      source, and configuration files.

      "Object" form shall mean any form resulting from mechanical
      transformation or translation of a Source form, including but
      not limited to compiled object code, generated documentation,
      and conversions to other media types.

      "Work" shall mean the work of authorship, whether in Source or
      Object form, made available under the License, as indicated by a
      copyright notice that is included in or attached to the work
      (an example is provided in the Appendix below).

      "Derivative Works" shall mean any work, whether in Source or Object
      form, that is based on (or derived from) the Work and for which the
      editorial revisions, annotations, elaborations, or other modifications
      represent, as a whole, an original work of authorship. For the purposes
      of this License, Derivative Works shall not include works that remain
      separable from, or merely link (or bind by name) to the interfaces of,
      the Work and Derivative Works thereof.

      "Contribution" shall mean any work of authorship, including
      the original version of the Work and any modifications or additions
      to that Work or Derivative Works thereof, that is intentionally
      submitted to Licensor for inclusion in the Work by the copyright owner
      or by an individual or Legal Entity authorized to submit on behalf of
      the copyright owner. For the purposes of this definition, "submitted"
      means any form of electronic, verbal, or written communication sent
      to the Licensor or its representatives, including but not limited to
      communication on electronic mailing lists, source code control systems,
      and issue tracking systems that are managed by, or on behalf of, the
      Licensor for the purpose of discussing and improving the Work, but
      excluding communication that is conspicuously marked or otherwise
      designated in writing by the copyright owner as "Not a Contribution."

      "Contributor" shall mean Licensor and any individual or Legal Entity
      on behalf of whom a Contribution has been received by Licensor and
      subsequently incorporated within the Work.

   2. Grant of Copyright License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      copyright license to reproduce, prepare Derivative Works of,
      publicly display, publicly perform, sublicense, and distribute the
      Work and such Derivative Works in Source or Object form.

   3. Grant of Patent License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      (except as stated in this section) patent license to make, have made,
      use, offer to sell, sell, import, and otherwise transfer the Work,
      where such license applies only to those patent claims licensable
      by such Contributor that are necessarily infringed by their
      Contribution(s) alone or by combination of their Contribution(s)
      with the Work to which such Contribution(s) was submitted. If You
      institute patent litigation against any entity (including a
      cross-claim or counterclaim in a lawsuit) alleging that the Work
      or a Contribution incorporated within the Work constitutes direct
      or contributory patent infringement, then any patent licenses
      granted to You under this License for that Work shall terminate
      as of the date such litigation is filed.

   4. Redistribution. You may reproduce and distribute copies of the
      Work or Derivative Works thereof in any medium, with or without
      modifications, and in Source or Object form, provided that You
      meet the following conditions:

      (a) You must give any other recipients of the Work or
          Derivative Works a copy of this License; and

      (b) You must cause any modified files to carry prominent notices
          stating that You changed the files; and

      (c) You must retain, in the Source form of any Derivative Works
          that You distribute, all copyright, patent, trademark, and
          attribution notices from the Source form of the Work,
          excluding those notices that do not pertain to any part of
          the Derivative Works; and

      (d) If the Work includes a "NOTICE" text file as part of its
          distribution, then any Derivative Works that You distribute must
          include a readable copy of the attribution notices contained
          within such NOTICE file, excluding those notices that do not
          pertain to any part of the Derivative Works, in at least one
          of the following places: within a NOTICE text file distributed
          as part of the Derivative Works; within the Source form or
          documentation, if provided along with the Derivative Works; or,
          within a display generated by the Derivative Works, if and
          wherever such third-party notices normally appear. The contents
          of the NOTICE file are for informational purposes only and
          do not modify the License. You may add Your own attribution
          notices within Derivative Works that You distribute, alongside
          or as an addendum to the NOTICE text from the Work, provided
          that such additional attribution notices cannot be construed
          as modifying the License.

      You may add Your own copyright statement to Your modifications and
      may provide additional or different license terms and conditions
      for use, reproduction, or distribution of Your modifications, or
      for any such Derivative Works as a whole, provided Your use,
      reproduction, and distribution of the Work otherwise complies with
      the conditions stated in this License.

   5. Submission of Contributions. Unless You explicitly state otherwise,
      any Contribution intentionally submitted for inclusion in the Work
      by You to the Licensor shall be under the terms and conditions of
      this License, without any additional terms or conditions.
      Notwithstanding the above, nothing herein shall supersede or modify
      the terms of any separate license agreement you may have executed
      with Licensor regarding such Contributions.

   6. Trademarks. This License does not grant permission to use the trade
      names, trademarks, service marks, or product names of the Licensor,
      except as required for reasonable and customary use in describing the
      origin of the Work and reproducing the content of the NOTICE file.

   7. Disclaimer of Warranty. Unless required by applicable law or
      agreed to in writing, Licensor provides the Work (and each
      Contributor provides its Contributions) on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
      implied, including, without limitation, any warranties or conditions
      of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
      PARTICULAR PURPOSE. You are solely responsible for determining the
      appropriateness of using or redistributing the Work and assume any
      risks associated with Your exercise of permissions under this License.

   8. Limitation of Liability. In no event and under no legal theory,
      whether in tort (including negligence), contract, or otherwise,
      unless required by applicable law (such as deliberate and grossly
      negligent acts) or agreed to in writing, shall any Contributor be
      liable to You for damages, including any direct, indirect, special,
      incidental, or consequential damages of any character arising as a
      result of this License or out of the use or inability to use the
      Work (including but not limited to damages for loss of goodwill,
      work stoppage, computer failure or malfunction, or any and all
      other commercial damages or losses), even if such Contributor
      has been advised of the possibility of such damages.

   9. Accepting Warranty or Additional Liability. While redistributing
      the Work or Derivative Works thereof, You may choose to offer,
      and charge a fee for, acceptance of support, warranty, indemnity,
      or other liability obligations and/or rights consistent with this
      License. However, in accepting such obligations, You may act only
      on Your own behalf and on Your sole responsibility, not on behalf
      of any other Contributor, and only if You agree to indemnify,
      defend, and hold each Contributor harmless for any liability
      incurred by, or claims asserted against, such Contributor by reason
      of your accepting any such warranty or additional liability.

   END OF TERMS AND CONDITIONS

   APPENDIX: How to apply the Apache License to your work.

      To apply the Apache License to your work, attach the following
      boilerplate notice, with the fields enclosed by brackets "[]"
      replaced with your own identifying information. (Don't include
      the brackets!)  The text should be enclosed in the appropriate
      comment syntax for the file format. We also recommend that a
      file or class name and description of purpose be included on the
      same "printed page" as the copyright notice for easier
      identification within third-party archives.

   Copyright (c) 2014 - 2015 CTTV

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''

def generate_classes(exportDirectory, skeleton, bCreateFile, propertyName=None, parentName=None, depth=0):
    '''
     This method generates all the python classes representing evidence string concepts
     as defined in the JSON Schema definition.
     It creates simple constructor, deep-copy constructors, validation methods to check
     if required fields are defined, in the correct format (date, email) or following a
     specific pattern rule (identifiers, etc.)
    '''
    schemaVersion = None
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
            if depth == 0 and 'version' in skeleton:
                schemaVersion = skeleton['version']
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
                        if os.path.exists(exportDirectory + "/" + raw[0]):
                            shutil.rmtree(exportDirectory + "/" + raw[0])
                        # create directory recursively
                        if not os.path.exists(exportDirectory + "/" + dirpath):
                            os.makedirs(exportDirectory + "/" + dirpath)
                        # create an init file recursively too (use the raw variable)
                        index = 0
                        for i in range(1, len(raw)-1):
                            '''
                            __init__.py
                              
                            A project’s source tree must include the namespace packages’ __init__.py files 
                            (and the __init__.py of any parent packages)
                            These __init__.py files must contain the line:
                            __import__('pkg_resources').declare_namespace(__name__)
                            '''
                            classfile = open(exportDirectory + "/" + "/".join(raw[index:i]) + "/__init__.py", 'w')
                            classfile.write('#package ' + ".".join(raw[index:i]) + "\n")
                            #classfile.write("__import__('pkg_resources').declare_namespace(__name__)")
                            classfile.write("from pkgutil import extend_path\n")
                            classfile.write("__path__ = extend_path(__path__, __name__)")
                            classfile.close()
                        # Finally create a file there and keep the file handler open
                        classfile = open(exportDirectory + "/" + dirpath + "/__init__.py", 'w')
            if (skeleton.has_key('properties')):
                for attribute_key in skeleton['properties']:
                    childMap = generate_classes(exportDirectory, skeleton['properties'][attribute_key], False, attribute_key, className, depth+1)
                    myMap['attributes'][attribute_key] = childMap
                    # extends the classes definition with the one from this map
                    myMap['classes'].extend(childMap['classes'])
            elif (className == 'AssociationScore'):
                # this is a hack since the JSON Schema is not consistent
                for attribute_key in ['probability', 'pvalue']:
                    childMap = generate_classes(exportDirectory, skeleton[attribute_key], False, attribute_key, className, depth+1)
                    myMap['attributes'][attribute_key] = childMap
                    # extends the classes definition with the one from this map
                    myMap['classes'].extend(childMap['classes'])
            elif (className == 'EvidenceProperties'):
                '''
                 this is a hack since the JSON Schema is not consistent in the way
                 concepts are defined.
                '''
                for attribute_key in ['experiment_specific', 'evidence_chain']:
                    childMap = generate_classes(exportDirectory, skeleton[attribute_key], False, attribute_key, className, depth+1)
                    myMap['attributes'][attribute_key] = childMap
                    # extends the classes definition with the one from this map
                    myMap['classes'].extend(childMap['classes'])
            elif (className == 'ProbabilityScore' or className == 'PValueScore'):
                # this is a hack since the JSON Schema is not consistent
                for attribute_key in ['value', 'method']:
                    childMap = generate_classes(exportDirectory, skeleton[attribute_key], False, attribute_key, className, depth+1)
                    myMap['attributes'][attribute_key] = childMap
                    # extends the classes definition with the one from this map
                    myMap['classes'].extend(childMap['classes'])
            indent = "  "*2
            if propertyName:
                myMap['__init__'] = indent + "\n" + indent + "# Name: " + propertyName + "\n"
                myMap['__assign__'] = indent + "self." + propertyName + " = " + propertyName + "\n"
                '''
                 describes properties not accounted for by the "properties" or "patternProperties" keywords
                 If this value is not specified (or is boolean true, then additional properties can contain anything
                 now generate the python code
                '''
                if (skeleton.has_key('additionalProperties')):
                    if (skeleton.has_key('required')) and skeleton['required']:
                        myMap['__init__'] += indent + "if " + propertyName + " is None:\n" + indent*2 + "self." + propertyName + " = {}\n" + indent + "else:\n" + indent*2 + "self." + propertyName + " = "+ propertyName + "\n"
                        myMap['__default__'] = propertyName + " = None"
                        myMap['__clone__'] = indent + "obj." + propertyName + " = clone." + propertyName + "\n"
                        myMap['__map__'] = indent + "obj." + propertyName + " = map['" + propertyName + "']\n"
                    else:
                        myMap['__init__'] += indent + "self." + propertyName + " = " + propertyName + "\n"
                        myMap['__default__'] = propertyName + " = None"
                        myMap['__clone__'] = indent + "if clone." + propertyName + ":\n"
                        myMap['__clone__'] += indent*2 + "obj." + propertyName + " = clone." + propertyName + "\n"
                        myMap['__map__'] = indent + "if map.has_key('" + propertyName + "'):\n"
                        myMap['__map__'] += indent*2 + "obj." + propertyName + " = map['" + propertyName + "']\n"
                    myMap['__serialize__'] = indent + "if not self." + propertyName +" is None: classDict['"+propertyName+"'] = self." + propertyName +"\n"
                    if skeleton.has_key('pattern'):
                        pattern = skeleton['pattern']
                        myMap['__validate__'] = indent + "if not re.match(\""+ pattern +"\"," + propertyName + "):\n"
                        myMap['__validate__'] += indent*2 + "sys.stderr.write(\"WARNING:\t'{0}' for field '"+ propertyName+"' does not match pattern '"+pattern+"'\".format(self."+propertyName+"))\n"
                        #m = re.match("^urn:jsonschema:(.+)$", classId)
                elif myMap['isAClass']:
                    if (skeleton.has_key('required')) and skeleton['required']:
                        myMap['__init__'] += indent + "if " + propertyName + " is None:\n" + indent*2 + "self." + propertyName + " = " + className + "()\n" + indent + "else:\n" + indent*2 + "self." + propertyName + " = "+ propertyName + "\n"
                        myMap['__default__'] = propertyName + " = None"
                        myMap['__clone__'] = indent + "obj." + propertyName + " = " + className + ".cloneObject(clone." + propertyName + ")\n"
                        myMap['__map__'] = indent + "if map.has_key('" + propertyName + "'):\n"
                        myMap['__map__'] += indent*2 + "obj." + propertyName + " = " + className + ".fromMap(map['" + propertyName + "'])\n"
                        myMap['__validate__'] = indent + "if not self."+ propertyName +" or self."+ propertyName +" == None :\n"
                        myMap['__validate__'] += indent*2 + "sys.stderr.write(\"ERROR: "+parentName+" - '"+propertyName+"' is required'\\n\")\n"
                        myMap['__validate__'] += indent*2 + "error = True"
                        myMap['__validate__'] += indent + "else:\n"
                        myMap['__validate__'] += indent*2 + "self." + propertyName+".validate()\n"            
                    else:
                        myMap['__init__'] += indent + "self." + propertyName + " = None\n"
                        myMap['__default__'] = indent + propertyName + " = None"
                        myMap['__clone__'] = indent + "if clone." + propertyName + ":\n"
                        myMap['__clone__'] += indent*2 + "obj." + propertyName + " = " + className + ".cloneObject(clone." + propertyName + ")\n"
                        myMap['__map__'] = indent + "if map.has_key('" + propertyName + "'):\n"
                        myMap['__map__'] += indent*2 + "obj." + propertyName + " = " + className + ".fromMap(map['" + propertyName + "'])\n"
                    myMap['__serialize__'] = indent + "if not self." + propertyName +" is None: classDict['"+propertyName+"'] = self." + propertyName +".serialize()\n"
                    
            if myMap['isAClass']:
                '''
                 Generate the python class specification with:
                  1. collect the default initialisation for fields (init all the attributes by default)
                  2. a constructor will all the fields as arguments with default values
                  3. a deep-copy constructor (clone)
                  4. a map constructor (from json)
                  5. a validation method to validate against the JSON Schema
                  6. add any other methods
                  7. get dictionary of non empty object
                  8. JSON SERIALIZER 
                '''
                classDefinition = ""
                if classId:
                    classDefinition += "# " + classId + "\n"
                classDefinition += "class " + className + "(object):\n"
                '''
                 1. default initialisation for fields
                '''
                arrayDefaultValues = []
                #classDefinition += baseindent + "def initialise(self):\n"
                for attribute_key in myMap['attributes']:
                    #classDefinition += myMap['attributes'][attribute_key]['__init__']
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
                        classDefinition += myMap['attributes'][attribute_key]['__init__']
                        #classDefinition += myMap['attributes'][attribute_key]['__assign__']
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
                classDefinition += baseindent*2 + "error = False\n"
                for attribute_key in myMap['attributes']:
                    if myMap['attributes'][attribute_key].has_key('__validate__'):
                        classDefinition += myMap['attributes'][attribute_key]['__validate__']
                classDefinition += baseindent*2 + "sys.stderr.flush()\n"
                classDefinition += baseindent*2 + "return error\n"
                '''
                 6. Add other methods if any
                '''
                for attribute_key in myMap['attributes']:
                    if myMap['attributes'][attribute_key].has_key('__methods__'):
                        classDefinition += myMap['attributes'][attribute_key]['__methods__']
                '''
                 7. Get dictionary of non empty fields
                '''
                classDefinition += baseindent + "def serialize(self):\n" + baseindent*2 + "classDict = {}\n"
                for attribute_key in myMap['attributes']:
                    if myMap['attributes'][attribute_key].has_key('__serialize__'):
                        classDefinition += myMap['attributes'][attribute_key]['__serialize__']
                classDefinition += baseindent*2 + "return classDict\n"        
                '''
                 8. Serialisation in JSON
                '''
                classDefinition += baseindent + "def to_JSON(self):\n"
                #classDefinition += baseindent*2 + "return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, check_circular=False, indent=4)\n"
                classDefinition += baseindent*2 + "return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=4)\n"
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
             5. generate extra methods
            '''
            indent = baseindent*2
            myMap['__init__'] = indent + "\n" + indent + "# Name: " + propertyName + "\n"
            myMap['__init__'] += indent + "# Type: " + dataType + "\n"
            myMap['__assign__'] = indent + "self." + propertyName + " = " + propertyName + "\n"
            myMap['__methods__'] = ""
            
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
                myMap['__map__'] = indent + "if map.has_key('" + propertyName + "'):\n"
                myMap['__map__'] += indent*2 + "obj." + propertyName + " = map['" + propertyName + "']\n"
                myMap['__validate__'] = indent + "if not self."+ propertyName +" or self."+ propertyName +" == None :\n"
                myMap['__validate__'] += indent*2 + "sys.stderr.write(\"ERROR: "+parentName+" - '"+propertyName+"' is required'\\n\")\n"
                myMap['__validate__'] += indent*2 + "error = True"
                
            else:
                myMap['__map__'] = indent + "if map.has_key('" + propertyName + "'):\n"
                myMap['__map__'] += indent*2 + "obj." + propertyName + " = map['" + propertyName + "']\n"
            
            myMap['__serialize__'] = indent + "if not self." + propertyName +" is None: classDict['"+propertyName+"'] = self." + propertyName +"\n"
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
                    myMap['__validate__'] += indent*2 + "error = True"
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
                    myMap['__validate__'] += indent*2 + "error = True"

                    '''
                    Add method to convert to an ISODate
                    '''
                    myMap['__methods__'] += baseindent + "def " + propertyName + "to_isoformat(self):\n" + indent + "iso8601.parse_date(self."+propertyName+").isoformat()\n"
            if dataType == 'string':
                '''
                 A string is initialised to None by default
                '''
                myMap['__init__'] += indent + "self." + propertyName + " = " + propertyName + "\n"
                myMap['__clone__'] = indent + "if clone." + propertyName + ":\n"
                myMap['__clone__'] += indent*2 + "obj." + propertyName + " = clone." + propertyName + "\n"
                myMap['__default__'] = propertyName + " = None"
            elif dataType == 'boolean':
                '''
                 A boolean is initialised to False by default
                '''
                myMap['__init__'] += indent + "self." + propertyName + " = " + propertyName + "\n"
                myMap['__clone__'] = indent + "if clone." + propertyName + ":\n"
                myMap['__clone__'] += indent*2 + "obj." + propertyName + " = clone." + propertyName + "\n"
                myMap['__default__'] = propertyName + " = False"
            elif dataType == 'number':
                '''
                 A number is initialised to nought by default
                '''
                myMap['__init__'] += indent + "self." + propertyName + " = " + propertyName + "\n"
                myMap['__clone__'] = indent + "if clone." + propertyName + ":\n"
                myMap['__clone__'] += indent*2 + "obj." + propertyName + " = clone." + propertyName + "\n"
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
                    constraint.append("self.{0} <= {1}".format(propertyName, minimum) if (skeleton.has_key('exclusiveMinimum')) else "self.{0} < {1}".format(propertyName, minimum))
                    message.append("should be greater than {0}".format(minimum) if (skeleton.has_key('exclusiveMinimum')) else "should be greater than or equal to {0}".format(minimum))
                if (skeleton.has_key('maximum')):
                    maximum = skeleton['maximum']
                    constraint.append("self.{0} >= {1}".format(propertyName, maximum) if (skeleton.has_key('exclusiveMaximum')) else "self.{0} > {1}".format(propertyName, maximum))
                    message.append("should be lower than {0}".format(minimum) if (skeleton.has_key('exclusiveMaximum')) else "should be lower than or equal to {0}".format(maximum))
                if (len(constraint)>0):
                    if not myMap.has_key('__validate__'):
                        myMap['__validate__'] = ""
                    myMap['__validate__'] += indent + "if {0}:".format(" or ".join(constraint))
                    myMap['__validate__'] += indent*2 + "sys.stderr.write(\"ERROR: {0} - '{1}': {2} {3}\\n\".format(self.{1}))\n".format(parentName, propertyName, "{0}", " and ".join(message))  
                    myMap['__validate__'] += indent*2 + "error = True"
                    
            elif dataType == 'array':
                '''
                 An array is created empty by default
                '''
                myMap['__init__'] += indent + "if " + propertyName + " is None:\n" + indent*2 + "self." + propertyName + " = []\n" + indent + "else:\n" + indent*2 + "self." + propertyName + " = "+ propertyName + "\n"
                myMap['__default__'] = propertyName + " = None"
                myMap['__clone__'] = indent + "if clone." + propertyName + ":\n"
                myMap['__clone__'] += indent*2 + "obj." + propertyName + " = []; obj." + propertyName +".extend(clone." + propertyName + ")\n"           
                '''
                 There are some constraints specific to arrays:
                   minItems
                '''
                if (skeleton.has_key('minItems')):
                    if not myMap.has_key('__validate__'):
                        myMap['__validate__'] = ""
                    myMap['__validate__'] += indent + "if self.{0} == None or len(self.{0}) < {1}:\n".format(propertyName, skeleton['minItems'])
                    myMap['__validate__'] += indent*2 + "sys.stderr.write(\"ERROR: {0} - '{1}' array should have at least {2} elements\\n\")\n".format(parentName, propertyName, skeleton['minItems'])
                    myMap['__validate__'] += indent*2 + "error = True"
                if (skeleton.has_key('maxItems')):
                    if not myMap.has_key('__validate__'):
                        myMap['__validate__'] = ""
                    myMap['__validate__'] += indent + "if self.{0} == None or len(self.{0}) > {1}:\n".format(propertyName, skeleton['maxItems'])
                    myMap['__validate__'] += indent*2 + "sys.stderr.write(\"ERROR: {0} - '{1}' array should have at most {2} elements\\n\")\n".format(parentName, propertyName, skeleton['maxItems'])
                    myMap['__validate__'] += indent*2 + "error = True"
                if (skeleton.has_key('uniqueItems')):
                    if not myMap.has_key('__validate__'):
                        myMap['__validate__'] = ""
                    myMap['__validate__'] += indent + "if self.{0} != None and len(set(self.{0})) != len(self.{0}):\n".format(propertyName)
                    myMap['__validate__'] += indent*2 + "sys.stderr.write(\"ERROR: {0} - '{1}' array have duplicated elements\\n\")\n".format(parentName, propertyName)               
                    myMap['__validate__'] += indent*2 + "error = True"
    else:
        '''
         This data type is unknown
        '''
        print textindent + "Can't process type %s" %(type(skeleton))
    if bCreateFile:
        # dump
        #classfile.write('\n'.join(myMap['classes']))
        classfile.write('import re\nimport sys\nimport iso8601\nimport types\nimport json\nimport logging\n')
        for c in myMap['classes']:
            classfile.write(c)
        classfile.close()
    return myMap
    
def generate_file(exportDirectory, contents, filename):
    moduleFile = open(exportDirectory + "/" + filename, 'w')
    moduleFile.write(contents)
    moduleFile.close()
 
#
# Package Generator class
#
class DataModelGenerator(object):
    # Virtual Functions
    _generate_file = staticmethod(generate_file)
    _generate_classes = staticmethod(generate_classes)

def main():

    parser = optparse.OptionParser()
    parser.add_option('-d', '--directory', default='../../../../../../build', dest='exportDirectory')
    parser.add_option('-u', '--uri', default='https://raw.githubusercontent.com/CTTV/input_data_format/master/json_schema/evidence_string_schema.json', dest='json_schema_uri')

    options, args = parser.parse_args()

    pattern = re.compile('^urn:jsonschema:(.+)$')
    classfile = 0
    testDirectory = 'tests'

    if not os.path.exists(options.exportDirectory):
        os.makedirs(options.exportDirectory)

    generator = DataModelGenerator()
    # read directly from the URL
    data = urlopen( options.json_schema_uri ).read()
    decoded = json.loads(data)
    generator._generate_classes(options.exportDirectory, decoded, True)
    generate_file(options.exportDirectory, license, "LICENSE")
    generator._generate_file(options.exportDirectory, readme, "README.rst")
    generator._generate_file(options.exportDirectory, setup, "setup.py")
    generator._generate_file(options.exportDirectory, tox, "tox.ini")
    generator._generate_file(options.exportDirectory, requirements, "requirements.txt")
    generator._generate_file(options.exportDirectory, manifest, "MANIFEST.in")
    shutil.copy2(testDirectory +'/test_org_cttv_input_model.py', options.exportDirectory + "/org/cttv/input/model/test_org_cttv_input_model.py")
    print 'The package has been generated in ', options.exportDirectory
    # exit here
    sys.exit()
    
if __name__ == "__main__":
    main()
