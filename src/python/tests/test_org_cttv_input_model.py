import sys
# the following dir contains the init file
sys.path.append('.')

import copy
import pickle

import pytest

import org.cttv.input.model as cttv

def test_evidenceString_exists():
    evidenceString = cttv.EvidenceString()
    assert not evidenceString == None

#def test_evidenceString_dummy():
#    evidenceString = cttv.EvidenceString()
#    assert 1 == 2

def foo():
  pass
    