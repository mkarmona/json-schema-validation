import sys
# the following dir contains the init file
sys.path.append('../../../../../../build')
import os
import org.cttv.input.model as cttv
import json
from json import JSONDecoder
from json import JSONEncoder
import logging
import logging.config
import yaml

def setup_logging(
    default_path='logging.ini', 
    default_level=logging.ERROR,
    env_key='LOG_CFG'
):
    """
     Setup logging configuration
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

# tested on IBD
# usage gunzip -c /home/gk680303/windows/scripts/cttv018_ibd_gwas_20141128_formatted.json.gz | python -c 'import sys, json; print json.load(sys.stdin)["country"]'

def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    
    python_raw = json.load(sys.stdin)

    validator = DataModelValidator()
    r = validator._validate(python_raw, logger)
    if r>0:
        logger.error("validation failed: {0} errors found while parsing the datasource".format(r))
        sys.exit(1)
    else:
        logger.info("validation passed")
        sys.exit(0)

def validate(python_raw, logger):
    nb_errors = 0
    if type(python_raw) is list:
        c = 0
        for currentItem in python_raw:
            logger.info("Entry Nb {0}".format(c))
            # debug mode
            evidenceString = cttv.EvidenceString.fromMap(currentItem)
            nb_errors = nb_errors + evidenceString.validate(logger)
            c +=1
    elif type(python_raw) is dict:
        evidenceString = cttv.EvidenceString.fromMap(python_raw)
        nb_errors = evidenceString.validate(logger)
    else:
        print "ERROR: impossible to parse the input stream\n"
    return nb_errors
#
# DataModel Validator class
#
class DataModelValidator(object):
    # Virtual Functions
    _validate = staticmethod(validate)

if __name__ == "__main__":
    main()