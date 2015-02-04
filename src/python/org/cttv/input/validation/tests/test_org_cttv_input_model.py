from __future__ import absolute_import, print_function

import org.cttv.input.model as model

def setup_module(module):
    print ("") # this is to get a newline after the dots
    print ("setup_module before anything in this file")
 
def teardown_module(module):
    print ("teardown_module after everything in this file")
 
def my_setup_function():
    print ("my_setup_function")
 
def my_teardown_function():
    print ("my_teardown_function")
 
@with_setup(my_setup_function, my_teardown_function)
def test_evidenceString_exists():
    evidenceString = cttv.EvidenceString()
    assert not evidenceString == None
