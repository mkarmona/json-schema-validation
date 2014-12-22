import sys
# the following dir contains the init file
sys.path.append('../../build')

import org.cttv.input.model as cttv
import json
from json import JSONDecoder
from json import JSONEncoder
  
# tested on IBD
# usage gunzip -c /home/gk680303/windows/scripts/cttv018_ibd_gwas_20141128_formatted.json.gz | python -c 'import sys, json; print json.load(sys.stdin)["country"]'

python_raw = json.load(sys.stdin)

c = 0
for currentItem in python_raw:
    print "Entry Nb {0}\n".format(c)
    evidenceString = cttv.EvidenceString.fromMap(currentItem)
    evidenceString.validate()
    c +=1
