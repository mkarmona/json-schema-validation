import sys
# the following dir contains the init file
sys.path.append('../../../../../../build')

import org.cttv.input.model as cttv
import json
from json import JSONDecoder
from json import JSONEncoder
  
# tested on IBD
# usage gunzip -c /home/gk680303/windows/scripts/cttv018_ibd_gwas_20141128_formatted.json.gz | python -c 'import sys, json; print json.load(sys.stdin)["country"]'

def main():
    python_raw = json.load(sys.stdin)

    validator = DataModelValidator()
    r = validator._validate(python_raw)
    sys.exit(r)

def validate(python_raw):
    result = 0
    if type(python_raw) is list:
        c = 0
        for currentItem in python_raw:
            print "Entry Nb {0}\n".format(c)
            # debug mode
            evidenceString = cttv.EvidenceString.fromMap(currentItem)
            r = evidenceString.validate()
            if r == False:
                result = 1
            c +=1
    elif type(python_raw) is dict:
        evidenceString = cttv.EvidenceString.fromMap(python_raw)
        evidenceString.validate()
    else:
        print "ERROR: impossible to parse the input stream\n"
    return 0
#
# DataModel Validator class
#
class DataModelValidator(object):
    # Virtual Functions
    _validate = staticmethod(validate)

if __name__ == "__main__":
    main()