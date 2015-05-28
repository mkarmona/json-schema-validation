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
import ConfigParser
import io

basepackagepath = "cttv/model"
packageClassNames = {}
packageClassDefinitions = {}
packagePythonMapping = {}

requirements = '''
nose>=1.3.4
tox>=1.7.0
wheel>=0.22.0
iso8601>=0.1.10
'''

manifest = '''
recursive-include cttv *.py
include README.rst LICENSE tox.ini setup.py *requirements.txt
'''

tox = '''
[tox]
envlist = py27

[testenv]
deps=-r{toxinidir}/requirements.txt
changedir={toxinidir}/cttv/model/tests
commands=nosetests
#deps= -rrequirements.txt
#commands=py.test --verbose cttv/model/test_cttv_model.py
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
    name="cttv.model",
    version="1.2",
    description=long_description.split("\\n")[0],
    long_description=long_description,
    author="Gautier Koscielny",
    author_email="gautierk@targetvalidation.org",
    url="https://github.com/CTTV/json_schema",
    #packages=find_packages('.'),
    #package_dir = {'': '.'},
    #namespace_packages = ["cttv", "cttv.model"],
    packages=[ LIST_PACKAGES ],
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

licence_header = '''
Copyright 2014-2015 EMBL - European Bioinformatics Institute, Wellcome 
Trust Sanger Institute and GlaxoSmithKline

This software was developed as part of the Centre for Therapeutic 
Target Validation (CTTV)  project. For more information please see:

	http://targetvalidation.org

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

authorship = '''
__author__ = "Gautier Koscielny"
__copyright__ = "Copyright 2014-2015, The Centre for Therapeutic Target Validation (CTTV)"
__credits__ = ["Gautier Koscielny", "Samiul Hasan"]
__license__ = "Apache 2.0"
__version__ = "1.2"
__maintainer__ = "Gautier Koscielny"
__email__ = "gautierk@targetvalidation.org"
__status__ = "Production"
'''

def get_class_properties_from_ref(ref, textindent, innerClass = None, uri = None):
    '''
     urn:jsonschema:cttv:input:model:EvidenceProperties
     https://github.com/CTTV/json_schema/blob/master/src/base.json
     => 
    '''
    classProperties = {}
    print textindent + "Find class for reference " + ref
    
    local_match = re.match("^#/(.+)$", ref)
    if local_match:
        print textindent + "Correct and point to full URI " + ref
        ref = uri + ref
        
    
    #https://raw.githubusercontent.com/CTTV/json_schema/master/src/evidence/base.json#base_evidence/properties/association_score
    uri_match = re.match("^https://raw\.githubusercontent\.com/CTTV/json_schema/master/src/(.+)\.json#*(.*)$", ref)
    json_match = re.match("^(https://raw\.githubusercontent\.com/CTTV/json_schema/master/src/.+\.json).*$", ref)
    #local_match = re.match("^#/(.+)$", ref)
    
    '''
     if we found a package from github
    '''
    if uri_match:
        '''
         if this class was never recorded
        '''
        if not ref in packageClassNames:
            print textindent + ";".join(uri_match.groups())
            uriclasspath = uri_match.groups()[0]
            # get python package for this json file
            jsonFile = json_match.groups()[0]
            data = urlopen( jsonFile ).read()
            jsonclass = json.loads(data)
            className = None
            raw = None
            
            if innerClass:
                p = re.compile(r'/')
                raw = p.split(uriclasspath)
                className = raw[-1].title() + innerClass.title()
                print textindent + "inner class '" + className + "' found"
            elif len(uri_match.groups()[1]) > 0:
                subschema = uri_match.groups()[1]
                print textindent + "Found subschema " + subschema
                definition_match = re.match("^(.*)/definitions/(.+)$", subschema)
                raw = subschema.split("/")
                className = raw[-1].title()
                # base_evidence/definitions/single_lit_reference
            else:
                # split path and className
                p = re.compile(r'/')
                raw = p.split(uriclasspath)
                className = raw[-1].title()
       
            print textindent + "IsClass: " + className
            # retrieve the package name for this class
            dirpath = packagePythonMapping[jsonFile]
            baselevels = len(basepackagepath.split("/"))
            print textindent + dirpath
            classProperties['dirPath'] = dirpath

            #if 'id' in jsonclass and 'type' in jsonclass['properties']:
            #    classProperties['class'] = jsonclass['properties']['type'][0]
            #else:
            classProperties['class'] = className
            p = re.compile(r'/')
            raw = p.split(dirpath)
            classProperties['package'] = '.'.join(raw)
            if len(raw) > baselevels:
                classProperties['import_as'] = "_".join(raw[baselevels:len(raw)])
            classProperties['classpath'] = '.'.join(raw) + '.' + className
            print textindent + "classpath: " + classProperties['classpath']
            packageClassNames[ref] = classProperties
            
        else:
            classProperties = packageClassNames[ref]
            print textindent + "IsClass: " + classProperties['class']
            print textindent + "IsPackage: " + classProperties['package']
            print textindent + "IsImportedAs: " + classProperties['import_as'] 
            
#    elif local_match:
#        localref = local_match.groups()[0]
#        definitions_match = re.match("^definitions/(.+)$", localref)
#        if definitions_match:
#            fullclasspath = definitions_match.groups()[0]
#        else:
#            fullclasspath = localref
#        p = re.compile(r'/')
#        raw = p.split(fullclasspath)
#        dirpath = None
#        if len(raw) > 1:
#            dirpath = '/'.join(raw[:len(raw)-1])
#            print textindent + dirpath
#        print textindent + raw[-1]
#        classProperties['package'] = dirpath
#        classProperties['class'] = raw[-1].title()
#        print("LOCAL MATCH " + fullclasspath)
    else:
        print(ref + "didn't match pattern :(")
        sys.exit(1)

    return classProperties
    
def generate_classes(skeleton, propertyName=None, parentName=None, package=None, required=False, uri=None, depth=0):
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
        if parentName:
            print textindent + "propertyName:\t" + propertyName + " (" + parentName + ")"
        else:
            print textindent + "propertyName:\t" + propertyName

    print textindent + 'Keys:\t\t' + ','.join(skeleton.keys())
    referencedSchema = None
    referencedClassProperties = None
    '''
     If the data type is an object
     we will define a class with a proper name
    '''
    className = None
    generateClassDefinition = False
    
    if type(skeleton) is dict:
    
        print textindent + "Parsing data structure"
        
        if '$ref' in skeleton:
            '''
             This is a reference to another module
             It's still a class but processing the class
             happens separately
            '''
            dataType = 'object' # $ref
            generateClassDefinition = False
            referencedSchema = skeleton['$ref']
            referencedClassProperties = get_class_properties_from_ref(referencedSchema, textindent, uri = uri)
            if package == referencedClassProperties['package']:
                className = referencedClassProperties['class']
            else:
                className = referencedClassProperties['import_as'] + "." + referencedClassProperties['class']

        elif 'allOf' in skeleton:
            dataType = skeleton['type']
            generateClassDefinition = True
            print textindent + "DataType: %s" %(dataType)
            parentURI = skeleton['allOf'][0]
            referencedSchema = parentURI['$ref']
            referencedClassProperties = get_class_properties_from_ref(referencedSchema, textindent, uri = uri)
                
        elif 'type' in skeleton:
            if type(skeleton['type']) is list:
                print textindent + "DataType: %s" %(','.join(skeleton['type']))
                # horrible hack
                dataType = skeleton['type'][0]
                sys.exit(1)
            else:
                dataType = skeleton['type']
                print textindent + "DataType: %s" %(dataType)
            
        if referencedSchema:
            '''
             The reference may come from another package. In this case, we need to import
             the relevant package in the ini file of the current package for the current class
            '''
            importStatement = referencedClassProperties['package']
            if referencedClassProperties['import_as'] and parentName:
                importStatement = referencedClassProperties['package'] + " as " + referencedClassProperties['import_as']
            if not (referencedClassProperties['package'] == package or importStatement in packageClassDefinitions[package]['imports']):
                packageClassDefinitions[package]['imports'].append(importStatement)
            
        '''
         The current structure represents an object
        '''
        if dataType == 'object':
        
            '''
             defines the multiple inherited classes
             and the oneOf declaration when an attribute must be one of 
             a set of subschemas
            '''
            superClasses = []
            oneOfClasses = []
            
            if 'allOf' in skeleton:
                '''
                 it's an extension of another schema definition
                 we have to assume it's always the first item
                '''
                generateClassDefinition = True
                parentURI = skeleton['allOf'][0]
                parentClassProperties = get_class_properties_from_ref(parentURI['$ref'], textindent, uri = uri)
                superClasses.append(parentClassProperties)
                print textindent + "SuperClass:\t" + parentClassProperties['package']

            elif 'oneOf' in skeleton:
                '''
                 the type of the attribute will be one of the classes, so
                 will need to cast to one of the class in turn but we
                 won't generate a class definition.
                '''
                #superClasses.append('object')
                generateClassDefinition = False
                for parentRef in skeleton['oneOf']:
                    oneOfClassProperties = get_class_properties_from_ref(parentRef['$ref'], textindent, uri = uri)
                    oneOfClasses.append(oneOfClassProperties)
                    print textindent + "PolymorphClass:\t" + oneOfClassProperties['package']
                    '''
                     The reference may come from another package. In this case, we need to import
                     the relevant package in the ini file of the current package for the current class
                    '''
                    importStatement = oneOfClassProperties['package']
                    if oneOfClassProperties['import_as'] and parentName:
                        importStatement = oneOfClassProperties['package'] + " as " + oneOfClassProperties['import_as']
                    if not (oneOfClassProperties['package'] == package or importStatement in packageClassDefinitions[package]['imports']):
                        packageClassDefinitions[package]['imports'].append(importStatement)
                    
            elif 'properties' in skeleton:
                '''
                 inner class
                '''
                generateClassDefinition = True
            elif 'additionalProperties' in skeleton:
                print("additionalProperties for attribute %s" %(propertyName))
            else:
                print textindent + "SuperClass:\tobject"
                            
            '''
             If we are at the root of the schema
             We create a fully fledged class
            '''
            if generateClassDefinition == True:
            #if depth == 0 and uri:
                if 'version' in skeleton:
                    schemaVersion = skeleton['version']
                '''
                create a python class with the same namespace and same identifier
                '''
                myMap['isAClass'] = True
                
                '''
                 generate a class identifier based on the URI
                '''
                classProperties = None
                if depth == 0:
                    classProperties = get_class_properties_from_ref(uri, textindent, uri = uri)
                    classId = uri
                else:
                    classProperties = get_class_properties_from_ref(uri + "#" + propertyName, textindent, innerClass = propertyName, uri = uri)
                    classId = uri + " inner class:("+propertyName+")"
                
                print textindent + "URI:\t" + uri
                className = classProperties['class']
                #if 'properties' in skeleton and 'type' in skeleton['properties']:
                #    myMap['class'] = skeleton['properties']['type']['enum'][0]
                #else:
                myMap['class'] = classProperties['class']
                myMap['package'] = classProperties['package']
                print textindent + "ClassName:\t" + myMap['class']
                
                packageClassDefinitions[package]['classes'].append(className)
                packageClassDefinitions[package][className] = {}
                packageClassDefinitions[package][className]['imports'] = []
              
                '''
                 The reference may come from another package. In this case, we need to import
                 the relevant package in the ini file of the current package for the current class
                '''
                if referencedClassProperties:
                    importStatement = referencedClassProperties['package']
                    if referencedClassProperties['import_as']:
                        importStatement = referencedClassProperties['package'] + " as " + referencedClassProperties['import_as']
                    if not (referencedClassProperties['package'] == package or importStatement in packageClassDefinitions[package][className]['imports']):
                        packageClassDefinitions[package][className]['imports'].append(importStatement)
                       
                '''
                 if there are definitions, treat them as inner classes. 
                 However, we will expose them as the same level as the class declaring it
                '''
                if 'definitions' in skeleton:
                    print textindent + "Parse extra definitions at depth {0}".format(depth)
                    for definition_key in skeleton['definitions']:
                        definitionMap = generate_classes(skeleton['definitions'][definition_key], parentName=definition_key, package=package, depth=depth, uri=uri + skeleton['id'] + "/definitions/" + definition_key)
                
            '''
             If the object contains properties, parse each of the properties and 
             create classes as necessary. 
             If a class inherits from another cttv class, we have to make sure
             we will init the properties properly. 
             We don't have to parse them at this point, but when we generate 
             the class definition, we have to add them in the constructors 
             and call the superclass for validation, cloning or validation
            '''
            classAttributes = {}

            if 'allOf' in skeleton and len(skeleton['allOf']) > 1 and 'properties' in skeleton['allOf'][1]:
                classAttributes = skeleton['allOf'][1]['properties']
                if ('type' in classAttributes):
                    print json.dumps(classAttributes)
                    #sys.exit(1)
            elif 'properties' in skeleton:
                '''
                 'type' can be a property of the class 
                '''
                classAttributes = skeleton['properties']
            
            '''
             Check the one that are required
            '''
            requiredArray = []
            if 'required' in skeleton:
                requiredArray = skeleton['required']
                #print "...".join(requiredArray)
            
            pName = parentName
            if className:
                pName = className

            for attribute_key in classAttributes:
                '''
                 skip references to other schemas
                 don't parse the type of the class either
                '''
                if not attribute_key in ['import_remote_schemas', 'allOf']:
                    childMap = generate_classes(classAttributes[attribute_key], propertyName=attribute_key, parentName=pName, package=package, required=(attribute_key in requiredArray), depth=depth+1, uri=uri)
                    myMap['attributes'][attribute_key] = childMap
                    '''
                     extends the classes definition with the one from this map
                    '''
                    #myMap['classes'].extend(childMap['classes'])

            '''
             Now let's specify the class declaration, all the constructors and methods
            '''
            indent = "  "*2
            if propertyName:
                myMap['__assign__'] = indent + "self." + propertyName + " = " + propertyName + "\n"
                myMap['__init__'] = indent + "\"\"\"\n"
                myMap['__init__'] += indent + "Name: " + propertyName + "\n"
                myMap['__init__'] += indent + "\"\"\"\n"
                '''
                describes properties not accounted for by the "properties" or "patternProperties" keywords
                If this value is not specified (or is boolean true, then additional properties can contain anything
                now generate the python code
                The additionalProperties keyword is used to control the handling of extra stuff, that is, properties whose names
                are not listed in the properties keyword. By default any additional properties are allowed
                We create a validation for properties                  
                '''
                if ('oneOf' in skeleton):
                    validateClause = []
                    for oneOfClass in oneOfClasses:
                        validateClause.append(" isinstance(self.{0}, {1}.{2})".format(propertyName,oneOfClass['import_as'], oneOfClass['class']))
                    if required:
                        #myMap['__init__'] += indent + "if " + propertyName + " is None:\n" + indent*2 + "self." + propertyName + " = {}\n" + indent + "else:\n" + indent*2 + "self." + propertyName + " = "+ propertyName + "\n"
                        myMap['__init__'] += indent + "self." + propertyName + " = " + propertyName + "\n"                        
                        myMap['__default__'] = propertyName + " = None"
                        myMap['__clone__'] = indent + "obj." + propertyName + " = clone." + propertyName + "\n"
                        myMap['__map__'] = indent + "obj." + propertyName + " = map['" + propertyName + "']\n"
                        myMap['__validate__'] = indent + "if not self."+ propertyName +" or self."+ propertyName +" == None:\n"
                        myMap['__validate__'] += indent*2 + "logger.error(\""+parentName+" - '"+propertyName+"' is required\")\n"
                        myMap['__validate__'] += indent*2 + "error = error + 1\n"
                        myMap['__validate__'] += indent + "elif not("+" or".join(validateClause)+"):\n"
                        myMap['__validate__'] += indent*2 + "logger.error(\""+parentName+" - '"+propertyName+"' incorrect type\")\n"
                        myMap['__validate__'] += indent*2 + "error = error + 1\n"
                        myMap['__validate__'] += indent + "else:\n"
                        myMap['__validate__'] += indent*2 + propertyName + "_error = self." + propertyName +".validate(logger)\n"
                        myMap['__validate__'] += indent*2 + "error = error + "+ propertyName + "_error\n"
                    else:
                        print textindent + "init not required oneOf {0}\n".format(propertyName)
                        myMap['__init__'] += indent + "self." + propertyName + " = " + propertyName + "\n"
                        myMap['__default__'] = propertyName + " = None"
                        myMap['__clone__'] = indent + "if clone." + propertyName + ":\n"
                        myMap['__clone__'] += indent*2 + "obj." + propertyName + " = clone." + propertyName + "\n"
                        myMap['__map__'] = indent + "if  '" + propertyName + "' in map:\n"
                        myMap['__map__'] += indent*2 + "obj." + propertyName + " = map['" + propertyName + "']\n"   
                        myMap['__validate__'] = indent + "if self."+ propertyName + ":\n" 
                        myMap['__validate__'] = indent*2 + "if not ("+" or".join(validateClause)+"):\n"
                        myMap['__validate__'] += indent*3 + "logger.error(\""+parentName+" - '"+propertyName+"' incorrect type\")\n"
                        myMap['__validate__'] += indent*3 + "error = error + 1\n"
                        myMap['__validate__'] += indent*2 + "else:\n"
                        myMap['__validate__'] += indent*3 + propertyName + "_error = self." + propertyName +".validate(logger)\n"
                        myMap['__validate__'] += indent*3 + "error = error + "+ propertyName + "_error\n"
                elif myMap['isAClass'] or '$ref' in skeleton:
                    if required:
                        #myMap['__init__'] += indent + "if " + propertyName + " is None:\n" + indent*2 + "self." + propertyName + " = " + className + "()\n" + indent + "else:\n" + indent*2 + "self." + propertyName + " = "+ propertyName + "\n"
                        myMap['__init__'] += indent + "self." + propertyName + " = "+ propertyName + "\n"
                        myMap['__default__'] = propertyName + " = None"
                        myMap['__clone__'] = indent + "obj." + propertyName + " = " + className + ".cloneObject(clone." + propertyName + ")\n"
                        myMap['__map__'] = indent + "if  '" + propertyName + "' in map:\n"
                        myMap['__map__'] += indent*2 + "obj." + propertyName + " = " + className + ".fromMap(map['" + propertyName + "'])\n"
                        myMap['__validate__'] = indent + "if not self."+ propertyName +" or self."+ propertyName +" == None :\n"
                        myMap['__validate__'] += indent*2 + "logger.error(\""+parentName+" - '"+propertyName+"' is required\")\n"
                        myMap['__validate__'] += indent*2 + "error = error + 1\n"
                        myMap['__validate__'] += indent + "elif not isinstance(self.{0}, {1}):\n".format(propertyName, className)
                        myMap['__validate__'] += indent*2 + "logger.error(\""+className+" class instance expected for attribute - '"+propertyName+"'\")\n"
                        myMap['__validate__'] += indent*2 + "error = error + 1\n"
                        myMap['__validate__'] += indent + "else:\n"
                        myMap['__validate__'] += indent*2 + propertyName + "_error = self." + propertyName +".validate(logger)\n"
                        myMap['__validate__'] += indent*2 + "error = error + "+ propertyName + "_error\n"
                    else:
                        myMap['__init__'] += indent + "self." + propertyName + " = "+ propertyName + "\n"
                        myMap['__default__'] = indent + propertyName + " = None"
                        myMap['__clone__'] = indent + "if clone." + propertyName + ":\n"
                        myMap['__clone__'] += indent*2 + "obj." + propertyName + " = " + className + ".cloneObject(clone." + propertyName + ")\n"
                        myMap['__map__'] = indent + "if  '" + propertyName + "' in map:\n"
                        myMap['__map__'] += indent*2 + "obj." + propertyName + " = " + className + ".fromMap(map['" + propertyName + "'])\n"
                        myMap['__validate__'] = indent + "if self."+ propertyName +":\n"
                        myMap['__validate__'] += indent*2 + "if not isinstance(self.{0}, {1}):\n".format(propertyName, className)
                        myMap['__validate__'] += indent*3 + "logger.error(\""+className+" class instance expected for attribute - '"+propertyName+"'\")\n"
                        myMap['__validate__'] += indent*3 + "error = error + 1\n"
                        myMap['__validate__'] += indent*2 + "else:\n"                        
                        myMap['__validate__'] += indent*3 + propertyName + "_error = self." + propertyName +".validate(logger)\n"
                        myMap['__validate__'] += indent*3 + "error = error + "+ propertyName + "_error\n"

                    myMap['__serialize__'] = indent + "if not self." + propertyName +" is None: classDict['"+propertyName+"'] = self." + propertyName +".serialize()\n"

                elif ('additionalProperties' in skeleton):
                    '''
                     The additionalProperties keyword is used to control the handling of extra stuff, that is, properties whose names
                     are not listed in the properties keyword. By default any additional properties are allowed.
                     The additionalProperties keyword may be either a boolean or an object. If additionalProperties is a boolean
                     and set to False, no additional properties will be allowed.
                    '''
                    additionalProperties = skeleton['additionalProperties']
                    print textindent + "additionalProperties found - check if it's a dictionary\n"
                    print textindent + "additionalProperties found - required {0}\n".format(required)
                    
                    if type(additionalProperties) is dict:                
                        if required:
                            myMap['__init__'] += indent + "if " + propertyName + " is None:\n" + indent*2 + "self." + propertyName + " = {}\n" + indent + "else:\n" + indent*2 + "self." + propertyName + " = "+ propertyName + "\n"
                            myMap['__default__'] = propertyName + " = None"
                            myMap['__clone__'] = indent + "obj." + propertyName + " = clone." + propertyName + "\n"
                            myMap['__map__'] = indent + "obj." + propertyName + " = map['" + propertyName + "']\n"
                            myMap['__validate__'] = indent + "if not self."+ propertyName +" or self."+ propertyName +" == None :\n"
                            myMap['__validate__'] += indent*2 + "logger.error(\""+parentName+" - '"+propertyName+"' is required\")\n"
                            myMap['__validate__'] += indent*2 + "error = error + 1\n"
                            myMap['__validate__'] += indent + "elif not isinstance(self.{0}, dict):\n".format(propertyName)
                            myMap['__validate__'] += indent*2 + "logger.error(\"dictionary expected for attribute - '"+propertyName+"'\")\n"
                            myMap['__validate__'] += indent*2 + "error = error + 1\n"
                        else:
                            print textindent +  "well init this {0}\n".format(propertyName)
                            
                            myMap['__init__'] += indent + "self." + propertyName + " = " + propertyName + "\n"
                            myMap['__default__'] = propertyName + " = None"
                            myMap['__clone__'] = indent + "if clone." + propertyName + ":\n"
                            myMap['__clone__'] += indent*2 + "obj." + propertyName + " = clone." + propertyName + "\n"
                            myMap['__map__'] = indent + "if  '" + propertyName + "' in map:\n"
                            myMap['__map__'] += indent*2 + "obj." + propertyName + " = map['" + propertyName + "']\n"
                            myMap['__validate__'] = indent + "if self.{0} and not isinstance(self.{0}, dict):\n".format(propertyName)
                            myMap['__validate__'] += indent*2 + "logger.error(\"dictionary expected for attribute - '"+propertyName+"'\")\n"
                            myMap['__validate__'] += indent*2 + "error = error + 1\n"                            
                        myMap['__serialize__'] = indent + "if not self." + propertyName +" is None: classDict['"+propertyName+"'] = self." + propertyName +"\n"
                        if 'pattern' in skeleton:
                            pattern = skeleton['pattern']
                            myMap['__validate__'] = indent + "if self." + propertyName + " and not re.match('"+ pattern +"', self." + propertyName + "):\n"
                            myMap['__validate__'] += indent*2 + "logger.error(\" - "+propertyName+" '\"+self."+propertyName+"+\"' does not match pattern '"+pattern+"'\")\n"
                            myMap['__validate__'] += indent*2 + "logger.warn(json.dumps(self.{0}, sort_keys=True, indent=2))\n".format(propertyName)
                    elif type(additionalProperties) is bool and additionalProperties == False:
                        print textident + "TODO: No additionalProperties for this class"
                        
                    #sys.exit(1)
                else:
                    print(textindent + "Unknown condition to generate class template")
                    sys.exit(1)
                    
            if myMap['isAClass']:
                            
                '''
                 Generate the python class specification with:
                  0. declaration of the class with the superclass
                  1. collect the default initialisation for fields (init all the attributes by default)
                     if the class inherits from a cttv class, we need to pass all the attributes and callable
                     the constructor for the fields that belongs to the superclass
                  2. a constructor will all the fields as arguments with default values
                  3. a deep-copy constructor (clone)
                  4. a map constructor (from json)
                  5. a validation method to validate against the JSON Schema
                  6. add any other methods
                  7. get dictionary of non empty object
                  8. JSON SERIALIZER 
                '''
                
                '''
                 Declare class name and inherited classes
                '''
                classDefinition = ""
                if classId:
                    classDefinition += "\"\"\"\n" 
                    classDefinition += classId + "\n"
                    classDefinition += "\"\"\"\n"
                    
                if (len(superClasses) == 0):
                    classDefinition += "class " + className + "(object):\n"
                else:
                    superClassPaths = []
                    for parentClassProperty in superClasses:
                        print textindent + parentClassProperty['classpath']
                        if parentClassProperty['package'] == package:
                            superClassPaths.append(parentClassProperty['class'])
                        else:
                            superClassPaths.append(parentClassProperty['import_as'] + "." + parentClassProperty['class'])
                        classDefinition += "class " + className + "("+",".join(superClassPaths)+"):\n"
                
                '''
                 get attributes from superclass
                '''
                superArrayDefaultValues = []
                superClassMap = None
                parentClassProperty = None
                superClassAttributes = None
                if (len(superClasses) > 0):
                    parentClassProperty = superClasses[0]
                    print "Super class: {0} {1}".format(parentClassProperty['package'],parentClassProperty['class'])
                    superClassMap = packageClassDefinitions[parentClassProperty['package']][parentClassProperty['class']]['specs']
                    print textindent + "{0}".format(",".join(superClassMap.keys()))
                    superArrayDefaultValues = superClassMap['arrayDefaultValues']
                    
                '''
                 1. default initialisation for fields
                    from current class but not 
                    from superclass
                '''
                arrayDefaultValues = []
                for attribute_key in myMap['attributes']:
                    #classDefinition += myMap['attributes'][attribute_key]['__init__']
                    if not superClassMap or attribute_key not in superClassMap['attributes'].keys():
                        print textindent + "Prepare default value for " + attribute_key
                        arrayDefaultValues.append(myMap['attributes'][attribute_key]['__default__'])
                    else:
                        print textindent + "Superclass attribute " + attribute_key
                myMap['arrayDefaultValues'] = arrayDefaultValues
                

                    
                '''
                 2. and another constructor again but with all attributes as arguments
                    with default values. If an attribute is defined twice, we need
                    to initialise the superclass attribute but not inherited one
                '''
                if (len(myMap['attributes'].keys())>0 or (superClassMap and len(superClassMap['attributes'].keys())>0)):
                    argsDefaultValuesArray = arrayDefaultValues
                    classDefinition += baseindent+"\"\"\"\n"
                    classDefinition += baseindent +"Constructor using all fields with default values\n"
                    classDefinition += baseindent+ "Arguments:\n"
                    if (len(myMap['attributes'].keys())>0):
                        classDefinition += baseindent+ ":param "
                        classDefinition += "\n{0}:param ".format(baseindent).join(arrayDefaultValues) + "\n"
                    if (superClassMap and len(superClassMap['attributes'].keys())>0):
                        classDefinition += baseindent+ ":param "
                        classDefinition += "\n{0}:param ".format(baseindent).join(superArrayDefaultValues) + "\n"                        
                        argsDefaultValuesArray.extend(superArrayDefaultValues)
                    classDefinition += baseindent+ "\"\"\"\n"
                    arguments = ", ".join(argsDefaultValuesArray)
                    classDefinition += baseindent + "def __init__(self, {0}):\n".format(arguments)
                    '''
                     call super constructor
                    '''
                    if (superClassMap and len(superClassMap['attributes'].keys())>0):
                        classDefinition += baseindent*2 + "\"\"\"\n"
                        classDefinition += baseindent*2 + "Call super constructor\n"
                        classDefinition += baseindent*2 + "BaseClassName.__init__(self, args)\n"
                        classDefinition += baseindent*2 + "\"\"\"\n"
                        #super(Derived, self).func()
                        #classDefinition += baseindent*2 +  "super({0}, self).__init__({1})\n".format(myMap['class'], ",".join(superClassMap['attributes'].keys()))
                        initArguments = []
                        for attribute_key in superClassMap['attributes']:
                            initArguments.append(attribute_key + " = " + attribute_key)
                        classDefinition += baseindent*2 +  "super({0}, self).__init__({1})\n".format(myMap['class'], ",".join(initArguments))
                        #if parentClassProperty['package'] == package:
                        #    classDefinition += baseindent*2 +  "super({0}, self).__init__({1})\n".format(parentClassProperty['class'], ",".join(initArguments))
                        #else:
                        #    classDefinition += baseindent*2 +  "super({0}, self).__init__({1})\n".format(parentClassProperty['import_as'] + "." + parentClassProperty['class'], ",".join(initArguments))
                    for attribute_key in myMap['attributes']:
                        classDefinition += myMap['attributes'][attribute_key]['__init__']

                '''
                 3. and a deep copy one (clone) as class method
                '''
                classDefinition += baseindent + "\n"
                classDefinition += baseindent + "@classmethod\n"
                classDefinition += baseindent + "def cloneObject(cls, clone):\n"
                
                if superClassMap:
                    classDefinition += baseindent*2 +  "# super will return an instance of the subtype\n"
                    classDefinition += baseindent*2 +  "obj = super({0}, cls).cloneObject(clone)\n".format(myMap['class'])
                else:
                    classDefinition += baseindent*2 + "obj = cls()\n"
                for attribute_key in myMap['attributes']:
                    classDefinition += myMap['attributes'][attribute_key]['__clone__']
                classDefinition += baseindent*2 + "return obj\n"
                '''
                 4. and a map copy one (map) as class method
                    check that the parameter passed as an argument is a map
                    initialise all the fields first
                '''
                classDefinition += baseindent + "\n"                
                classDefinition += baseindent + "@classmethod\n"
                classDefinition += baseindent + "def fromMap(cls, map):\n"
                if (superClassMap and len(superClassMap['attributes'].keys())>0):
                    # take the keys from the parent class as well
                    attrs = list(myMap['attributes'].keys())
                    attrs.extend(list(superClassMap['attributes'].keys()))
                    classDefinition += baseindent*2 + "cls_keys = ['"+"','".join(list(attrs))+"']\n"
                else:
                    classDefinition += baseindent*2 + "cls_keys = ['"+"','".join(list(myMap['attributes']))+"']\n"
                if superClassMap:
                    classDefinition += baseindent*2 +  "obj = super({0}, cls).fromMap(map)\n".format(myMap['class'])
                else:
                    classDefinition += baseindent*2 + "obj = cls()\n"                    
                classDefinition += baseindent*2 + "if not isinstance(map, types.DictType):\n"
                classDefinition += baseindent*3
                classDefinition += "logger.error(\"{0}".format(myMap['class'])
                classDefinition +=" - DictType expected - {0} found\\n\".format(type(map)))\n"
                classDefinition += baseindent*3 + "return\n"
                for attribute_key in myMap['attributes']:
                    classDefinition += myMap['attributes'][attribute_key]['__map__']
                if superClassMap:
                    classDefinition += baseindent*2 + "for key in map:\n"
                    classDefinition += baseindent*3 + "if not key in cls_keys:\n"
                    classDefinition += baseindent*4 + "logger.error(\"{0}".format(myMap['class'])
                    classDefinition +=" - invalid field - {0} found\".format(key))\n"
                classDefinition += baseindent*2 + "return obj\n"
                
                '''
                 5. and a validate method
                '''
                classDefinition += baseindent + "\n"
                classDefinition += baseindent + "def validate(self, logger):\n"
                classDefinition += baseindent*2 + "\"\"\"\n"
                classDefinition += baseindent*2 + "Validate class {0}\n".format(className)
                classDefinition += baseindent*2 + ":returns: number of errors found during validation\n"
                classDefinition += baseindent*2 + "\"\"\"\n"
                #classDefinition += baseindent*2 + "logger.error(\"Validating class {0}\")\n".format(className)
                classDefinition += baseindent*2 + "error = 0\n"
                if superClassMap:
                    classDefinition += baseindent*2 + "# cumulate errors from super class\n"
                    classDefinition += baseindent*2 +  "error = error + super({0}, self).validate(logger)\n".format(myMap['class'])
                    '''
                     Add all required attribute from superclass
                    '''
                    for attribute_key in superClassMap['attributes']:
                        if attribute_key in requiredArray:
                            classDefinition += baseindent*2 + "if self." + attribute_key + " == None:\n"
                            classDefinition += baseindent*3 + "logger.error(\""+className+" - '"+attribute_key+"' is required\")\n"
                            classDefinition += baseindent*3 + "error = error + 1\n"
                for attribute_key in myMap['attributes']:
                    if '__validate__' in myMap['attributes'][attribute_key]:
                        classDefinition += myMap['attributes'][attribute_key]['__validate__']
                    else:
                        print "WARNING: " + attribute_key + " has no validation predicate"
                        sys.exit(1)

                
                #classDefinition += baseindent*2 + "sys.stderr.flush()\n"
                classDefinition += baseindent*2 + "return error\n"
                
                '''
                 6. Add other methods if any
                '''
                for attribute_key in myMap['attributes']:
                    if myMap['attributes'][attribute_key].has_key('__methods__'):
                        classDefinition += myMap['attributes'][attribute_key]['__methods__']
                '''
                 7. Get dictionary of non empty fields including superclass fields
                '''
                classDefinition += baseindent + "\n"
                classDefinition += baseindent + "def serialize(self):\n"
                if superClassMap:
                    classDefinition += baseindent*2 + "classDict = super({0}, self).serialize()\n".format(myMap['class'])
                else:
                    classDefinition += baseindent*2 + "classDict = {}\n"
                for attribute_key in myMap['attributes']:
                    if myMap['attributes'][attribute_key].has_key('__serialize__'):
                        classDefinition += myMap['attributes'][attribute_key]['__serialize__']
                classDefinition += baseindent*2 + "return classDict\n"
                '''
                 8. Serialisation in JSON
                '''
                classDefinition += baseindent + "\n"
                classDefinition += baseindent + "def to_JSON(self, indentation=4):\n"
                #classDefinition += baseindent*2 + "return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, check_circular=False, indent=4)\n"
                classDefinition += baseindent*2 + "return json.dumps(self, default=lambda o: o.serialize(), sort_keys=True, check_circular=False, indent=indentation)\n"
                
                '''
                 Finally store the class definition in the classes directory
                '''
                packageClassDefinitions[package][myMap['class']]['specs'] = myMap
                packageClassDefinitions[package][myMap['class']]['classDefinition'] = classDefinition
                
                #myMap['classes'].extend(classDefinition)
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
            myMap['__init__'] = indent + "\n" + indent + "\"\"\"\n"
            myMap['__init__'] += indent + "Name: " + propertyName + "\n"
            myMap['__init__'] += indent + "Type: " + dataType + "\n"
            myMap['__assign__'] = indent + "self." + propertyName + " = " + propertyName + "\n"
            myMap['__methods__'] = ""
            
            '''
             Add the description as a comment
            '''
            if (skeleton.has_key('description')):
                myMap['__init__'] += indent + "Description: " + skeleton['description'] + "\n"
            
            '''
             Check if the property is required:
               1. if so, the value should be assigned from the deep-copy/map constructor
               2. the validation procedure must check the field exists
            '''
            if required:
                #'{:%Y-%m-%d %H:%M:%S}'.format, gen
                #myMap['__init__'] += indent + '#Required: {%r}\n'.format %(skeleton['required']))
                myMap['__init__'] += indent + ('Required: {%r}' % (required)) + "\n"
                myMap['__map__'] = indent + "if  '" + propertyName + "' in map:\n"
                myMap['__map__'] += indent*2 + "obj." + propertyName + " = map['" + propertyName + "']\n"
                myMap['__validate__'] = indent + "if not self."+ propertyName +" or self."+ propertyName +" == None :\n"
                myMap['__validate__'] += indent*2 + "logger.error(\""+parentName+" - '"+propertyName+"' is required\")\n"
                myMap['__validate__'] += indent*2 + "error = error + 1\n"
                
            else:
                myMap['__map__'] = indent + "if  '" + propertyName + "' in map:\n"
                myMap['__map__'] += indent*2 + "obj." + propertyName + " = map['" + propertyName + "']\n"
            
            myMap['__serialize__'] = indent + "if not self." + propertyName +" is None: classDict['"+propertyName+"'] = self." + propertyName +"\n"
            '''
             VALIDATION STEP 1: check there is a regular expression rule to apply (for validation)
            '''
            if 'pattern' in skeleton:
                pattern = skeleton['pattern']
                myMap['__validate__'] = indent + "\"\"\" Check regex: "+ pattern +" for validation\"\"\"\n"
                myMap['__validate__'] += indent + "if self." + propertyName + " and not re.match('"+ pattern +"', self." + propertyName + "):\n"
                myMap['__validate__'] += indent*2 + "logger.error(\""+parentName+" - "+propertyName+" '\"+self."+propertyName+"+\"' does not match pattern '"+pattern+"'\")\n"
                myMap['__validate__'] += indent*2 + "logger.warn(json.dumps(self.{0}, sort_keys=True, indent=2))\n".format(propertyName)
            '''
             VALIDATION STEP 2: check format is correct
            '''
            if ('format' in skeleton):
                # "format": "date-time", "format": "email"
                # we still need to validate those
                myMap['__init__'] += indent + "String format: " + skeleton['format'] + "\n"
                if not myMap.has_key('__validate__'):
                    myMap['__validate__'] = ""
                if skeleton['format'] == "email":
                    myMap['__validate__'] += indent + "if self." + propertyName + " and not self." + propertyName + " == None and not re.match('[\\w.-]+@[\\w.-]+.\\w+', self." + propertyName + "):\n"
                    myMap['__validate__'] += indent*2 + "logger.error(\""+parentName+" - "+propertyName+" '{0}' is not a valid email address\".format(self."+propertyName+"))\n"
                    myMap['__validate__'] += indent*2 + "logger.error(self.to_JSON)\n"
                    myMap['__validate__'] += indent*2 + "error = error + 1\n"
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
                    myMap['__validate__'] += indent*3 + "logger.error(\""+parentName+" - "+propertyName+" '{0}' invalid ISO 8601 date (YYYY-MM-DDThh:mm:ss.sTZD expected)\".format(self."+propertyName+"))\n"
                    myMap['__validate__'] += indent*3 + "logger.error(self.to_JSON())\n"
                    myMap['__validate__'] += indent*3 + "error = error+1\n"

                    '''
                    Add method to convert to an ISODate
                    '''
                    myMap['__methods__'] += baseindent + "def " + propertyName + "to_isoformat(self):\n" + indent + "iso8601.parse_date(self."+propertyName+").isoformat()\n"
                    
            if 'enum' in skeleton:
                '''
                 The enum keyword is used to restrict a value to a fixed set of values. 
                 It must be an array with at least one element, where each element is unique
                '''
                if not myMap.has_key('__validate__'):
                    myMap['__validate__'] = ""                
                enumArray = None
                if dataType == 'string':
                    enumArray = "'" + "','".join(skeleton['enum']) + "'"
                else:
                    enumArray = ",".join(skeleton['enum'])
                myMap['__validate__'] += indent + "if self." + propertyName + " and not self." + propertyName + " == None and not self." + propertyName + " in [" + enumArray + "]:\n"
                myMap['__validate__'] += indent*2 + "logger.error(\""+parentName+" - '"+propertyName+"' value is restricted to the fixed set of values " + enumArray + "\")\n"
                myMap['__validate__'] += indent*2 + "error = error + 1\n"
                
            #if '$ref' in skeleton:
            #    '''
            #     This is the reference to an object of a different type 
            #    '''
            #    if not myMap.has_key('__validate__'):
            #        myMap['__validate__'] = ""               
            #    myMap['__validate__'] += indent + propertyName + "_error = self." + propertyName +".validate(logger)\n"
            #    myMap['__validate__'] += indent + "error = error + "+ propertyName + "_error\n"   
                
            myMap['__init__'] += indent + "\"\"\"\n"
            
            if 'oneOf' in skeleton:
                '''
                '''
                print("oneOf - DO SOMETHING!!!!")
                sys.exit(1)
                
            if dataType == '$ref':
                '''
                 This is a reference to another schema
                 A dictionary will contain the name of the class
                 if not it will get it by parsing the file.
                 check if required or not
                '''
                myMap['__init__'] += indent + "self." + propertyName + " = " + propertyName + "\n"
                myMap['__clone__'] = indent + "if clone." + propertyName + ":\n"
                myMap['__clone__'] += indent*2 + "obj." + propertyName + " = clone." + propertyName + "\n"
                myMap['__default__'] = propertyName + " = None"
                print "Why are we here?"
                sys.exit(1)
                
            elif dataType == 'string':
                '''
                 A string is initialised to None by default
                '''
                myMap['__init__'] += indent + "self." + propertyName + " = " + propertyName + "\n"
                myMap['__clone__'] = indent + "if clone." + propertyName + ":\n"
                myMap['__clone__'] += indent*2 + "obj." + propertyName + " = clone." + propertyName + "\n"
                myMap['__default__'] = propertyName + " = None"
                # Check type
                if not myMap.has_key('__validate__'):
                    myMap['__validate__'] = ""
                myMap['__validate__'] += indent + "if self." + propertyName + " and not isinstance(self." + propertyName + ", basestring):\n"
                myMap['__validate__'] += indent*2 + "logger.error(\""+parentName+" - '"+propertyName+"' type should be a string\")\n"
                myMap['__validate__'] += indent*2 + "error = error + 1\n"    
                
                
            elif dataType == 'boolean':
                '''
                 A boolean is initialised to False by default
                '''
                myMap['__init__'] += indent + "self." + propertyName + " = " + propertyName + "\n"
                myMap['__clone__'] = indent + "if clone." + propertyName + ":\n"
                myMap['__clone__'] += indent*2 + "obj." + propertyName + " = clone." + propertyName + "\n"
                myMap['__default__'] = propertyName + " = False"
                if not myMap.has_key('__validate__'):
                    myMap['__validate__'] = ""
                myMap['__validate__'] += indent + "if self." + propertyName + " and not type(self." + propertyName + ") is bool:\n"
                myMap['__validate__'] += indent*2 + "logger.error(\""+parentName+" - '"+propertyName+"' type should be a boolean\")\n"
                myMap['__validate__'] += indent*2 + "error = error + 1\n"
                
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
                    myMap['__validate__'] += indent + "if {0}:\n".format(" or ".join(constraint))
                    myMap['__validate__'] += indent*2 + "logger.error(\"{0} - '{1}': {2} {3}\".format(self.{1}))\n".format(parentName, propertyName, "{0}", " and ".join(message))
                    myMap['__validate__'] += indent*2 + "logger.error(self.to_JSON())\n"
                    myMap['__validate__'] += indent*2 + "error = error+1\n"
                    
            elif dataType == 'array':
                '''
                 An array is created empty by default
                '''
                myMap['__init__'] += indent + "if " + propertyName + " is None:\n" + indent*2 + "self." + propertyName + " = []\n" + indent + "else:\n" + indent*2 + "self." + propertyName + " = "+ propertyName + "\n"
                myMap['__default__'] = propertyName + " = None"
                myMap['__clone__'] = indent + "if clone." + propertyName + ":\n"
                myMap['__clone__'] += indent*2 + "obj." + propertyName + " = []; obj." + propertyName +".extend(clone." + propertyName + ")\n"
                
                print "KEYS:{0}\n".format( ",".join(skeleton.keys()))
                
                if 'items' in skeleton:
                    items = skeleton['items']
                    
                    '''
                    Items of an array can contain definition of objects
                    So, for every attribute within this array, we have to 
                    create a class if it's not a primitive type
                    '''
                    
                    itemType = None
                    
                    if items['type'] == "string":
                        ''' can be string or unicode'''
                        itemType = "basestring"
                    elif items['type'] == "number":
                        itemType = "(int, long, float, complex)"
                    elif items['type'] == "object" and '$ref' in items:
                        '''
                         is it a local or remote reference to an existing class?
                        '''
                        print textindent + "ITEM REF: {0}\n".format(items['$ref'])
                        referencedClassProperties = get_class_properties_from_ref(items['$ref'], textindent, uri = uri)
                        if package == referencedClassProperties['package']:
                            itemType = referencedClassProperties['class']
                        else:
                            importStatement = referencedClassProperties['package'] + " as " + referencedClassProperties['import_as']
                            if not (importStatement in packageClassDefinitions[package]['imports']):
                                packageClassDefinitions[package]['imports'].append(importStatement)                        
                            itemType = referencedClassProperties['import_as'] + "." + referencedClassProperties['class']
                        #itemType = classProperties['class']

                    elif items['type'] == "object" and 'id' in items:
                        print "Creating type for child of property " + propertyName + "\n"
                        sys.exit(1)
                        childMap = generate_classes(skeleton['items'], package=package, depth=depth+1)
                        if childMap['isAClass']:
                            itemType = childMap['class']
                        myMap['classes'].extend(childMap['classes'])                     
                    #myMap['attributes'][attribute_key] = childMap
                    # extends the classes definition with the one from this map
                
                    '''
                     There are some constraints specific to arrays:
                       type                     
                       minItems
                       maxItems
                       uniqueItems
                    '''
                    if not myMap.has_key('__validate__'):
                        myMap['__validate__'] = ""
                    '''
                    The empty array is always valid but the items should be of the specified type
                    '''
                    myMap['__validate__'] += indent + "if not self.{0} == None and len(self.{0}) > 0 and not all(isinstance(n, {1}) for n in self.{0}):\n".format(propertyName, itemType)
                    myMap['__validate__'] += indent*2 + "logger.error(\"{0} - '{1}' array should have elements of type '{2}'\")\n".format(parentName, propertyName, itemType)
                    myMap['__validate__'] += indent*2 + "error = error+1\n"
                        
                    if ('minItems' in items):
                        
                        myMap['__validate__'] += indent + "if self.{0} and len(self.{0}) < {1}:\n".format(propertyName, items['minItems'])
                        myMap['__validate__'] += indent*2 + "logger.error(\"{0} - '{1}' array should have at least {2} elements\")\n".format(parentName, propertyName, items['minItems'])
                        myMap['__validate__'] += indent*2 + "error = error + 1\n"
                    if ('maxItems' in items):
                        myMap['__validate__'] += indent + "if self.{0} and len(self.{0}) > {1}:\n".format(propertyName, items['maxItems'])
                        myMap['__validate__'] += indent*2 + "logger.error(\"{0} - '{1}' array should have at most {2} elements\")\n".format(parentName, propertyName, items['maxItems'])
                        myMap['__validate__'] += indent*2 + "error = error + 1\n"
                    if ('uniqueItems' in items):
                        myMap['__validate__'] += indent + "if self.{0} and len(set(self.{0})) != len(self.{0}):\n".format(propertyName)
                        myMap['__validate__'] += indent*2 + "logger.error(\"{0} - '{1}' array have duplicated elements\")\n".format(parentName, propertyName)
                        myMap['__validate__'] += indent*2 + "error = error + 1\n"
                    
                
    else:
        '''
         This data type is unknown
        '''
        print textindent + "Can't process type %s" %(type(skeleton))
        sys.exit(1)

    return myMap

def write_package_files(exportDirectory, dirpath, isAModule=False):
                
    index = 0
    raw = dirpath.split("/")
    package = ".".join(raw)
    print "Write python package " + package
    subdirs = dirpath
    if isAModule:
        subdirs = "/".join(raw[0:len(raw)-1])
    '''
     create directories recursively
    '''
    if not os.path.exists(exportDirectory + "/" + subdirs):
        os.makedirs(exportDirectory + "/" + subdirs)
    '''
     create an init file recursively too (use the raw variable)
    '''

    
    for i in range(1, len(raw)-1):
        print "Create" + "/".join(raw[index:i])
        '''
        __init__.py
          
        A project’s source tree must include the namespace packages’ __init__.py files 
        (and the __init__.py of any parent packages)
        These __init__.py files must contain the line:
        __import__('pkg_resources').declare_namespace(__name__)
        '''
        initFilename = exportDirectory + "/" + "/".join(raw[index:i]) + "/__init__.py"
        if not os.path.isfile(initFilename):
            initFile = open(initFilename, 'w')
            initFile.write('#package ' + ".".join(raw[index:i]) + "\n")
            #classfile.write("__import__('pkg_resources').declare_namespace(__name__)")
            initFile.write(authorship + "\n")
            initFile.write("from pkgutil import extend_path\n")
            initFile.write("__path__ = extend_path(__path__, __name__)")
            initFile.close()
    
    fileName = "__init__.py"
    upperBound = len(raw)
    
    if isAModule:
        fileName = raw[-1]+".py"
        upperBound = len(raw)-1
        
    '''
     create a file there and keep the file handler open
     while exporting all the classes
    '''
    initFile = open(exportDirectory + "/" + "/".join(raw[0:upperBound]) + "/" + fileName, 'w')
    
    '''
     Add licence header
    '''
    initFile.write("'''")
    initFile.write(licence_header)
    initFile.write("'''\n")
    
    '''
     add imports
    '''
    print "Add the following import statements to the package: " + ";".join(packageClassDefinitions[package]['imports'])
    initFile.write("\n".join(map(lambda x: "import " + x, packageClassDefinitions[package]['imports'])))
    initFile.write("\n")
    
    '''
     add author information
    '''
    initFile.write(authorship + "\n")
    
    '''
     add logger for validation
    '''
    initFile.write("logger = logging.getLogger(__name__)\n")
        
    print "export following classes: " + ",".join(packageClassDefinitions[package]['classes'])
    for className in packageClassDefinitions[package]['classes']:
        print "export class " + className
        #classFileHandler = open(exportDirectory + "/" + dirpath + "/" + className+ ".py", 'w')
        print "Add the following import statements to the package: " + ";".join(packageClassDefinitions[package][className]['imports'])
        initFile.write("\n".join(map(lambda x: "import " + x, packageClassDefinitions[package][className]['imports'])))
        initFile.write("\n")        
        initFile.write(packageClassDefinitions[package][className]['classDefinition'])
 
    initFile.flush()
    initFile.close()

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
    _write_package_files = staticmethod(write_package_files)
    _get_class_properties_from_ref = staticmethod(get_class_properties_from_ref)
    # Attributes
    

def main():

    parser = optparse.OptionParser()
    parser.add_option('-d', '--directory', default='../../../../../../build', dest='exportDirectory')
    parser.add_option('-c', '--config', default='../../../../../../schema/json-1.2.ini', dest='json_schema_ini_file')
    #parser.add_option('-u', '--uri', default='https://raw.githubusercontent.com/CTTV/json_schema/master/src/base.json', dest='json_schema_uri')

    options, args = parser.parse_args()

    pattern = re.compile('^urn:jsonschema:(.+)$')
    classfile = 0
    testDirectory = 'tests'

    if not os.path.exists(options.exportDirectory):
        os.makedirs(options.exportDirectory)

    # Load the configuration file
    with open(options.json_schema_ini_file) as f:
        dependencies_config = f.read()
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.readfp(io.BytesIO(dependencies_config))

    dependencies = {}
    # List all dependencies and assign correct python package mapping
    print("List all dependencies")
    for package in config.sections():
        print("Package: %s" % package)
        for jsonclass in config.options(package):
            print("x %s:::%s:::%s" % (jsonclass, config.get(package, jsonclass), str(type(jsonclass))))
            dependencies[config.get(package, jsonclass)] = None
            packagePythonMapping[config.get(package, jsonclass)] = package

    # Print some contents
    #print("\nPrint some schema URI")
    #print(config.get('bioentity', 'drug'))

    '''
     remove existing directory structure containing 
     the python package
    '''
    pdir = basepackagepath.split("/")
    if os.path.exists(options.exportDirectory + "/" + pdir[0]):
        shutil.rmtree(options.exportDirectory + "/" + pdir[0])
    
    generator = DataModelGenerator()
    
    pythonPackages = []
    pythonDirs = []
    # OK, let's iterate over all packages and classes in Turn
    for package in config.sections():
        print("Package: %s" % package)
        s = package.split("/")
        pythonPackage = ".".join(s)
        pythonDir = "\"" + ".".join(s[0:len(s)-1]) + "\""
        if not pythonDir in pythonDirs:
            pythonDirs.append(pythonDir)
        pythonPackages.append("\"" + pythonPackage + "\"")
        
        '''
         initialisation of the package in the package registry
         including default imports
        '''
        packageClassDefinitions[pythonPackage] = {}
        packageClassDefinitions[pythonPackage]['classes'] = []
        packageClassDefinitions[pythonPackage]['imports'] = ["re", "sys", "iso8601", "types", "json", "logging"]    
        
        '''
         parse each file in turn
        '''
        
        for jsonclass in config.options(package):
            uri = config.get(package, jsonclass)
            print("parsing class %s with URI %s" % (jsonclass, uri))
            # read directly from the URL in the dependencies dictionary
            data = urlopen( uri ).read()
            decoded = json.loads(data)
            generator._generate_classes(decoded, package=pythonPackage, uri=uri)
            
        '''
         finally, write the class definitions in the correct order
        '''
        generator._write_package_files(options.exportDirectory, package, len(config.options(package))>0)
            
    generator._generate_file(options.exportDirectory, license, "LICENSE")
    generator._generate_file(options.exportDirectory, readme, "README.rst")
    
    generator._generate_file(options.exportDirectory, setup.replace("LIST_PACKAGES", ",".join(pythonDirs)), "setup.py")
    generator._generate_file(options.exportDirectory, tox, "tox.ini")
    generator._generate_file(options.exportDirectory, requirements, "requirements.txt")
    generator._generate_file(options.exportDirectory, manifest, "MANIFEST.in")
    shutil.copy2(testDirectory +'/test_org_cttv_input_model.py', options.exportDirectory + "/cttv/model/test_cttv_model.py")
    print 'The package has been generated in ', options.exportDirectory
    # exit here
    sys.exit()
    
if __name__ == "__main__":
    main()
