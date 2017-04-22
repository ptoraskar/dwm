""" test_dwm_init """

import mongomock
from mock import patch, raises

from dwm import Dwm

# Setup mongomock db

DB = mongomock.MongoClient().db

# Initialization tests


def test_dwm_initialize():
    """ Test that Dwm class initializes with proper object type """
    dwm = Dwm(name='test', mongo=DB)
    assert isinstance(dwm, Dwm)


def test_dwm_init_name():
    """ test Dwm class sets name variable """
    dwm = Dwm(name='test', mongo=DB)
    assert dwm.name == 'test'


def test_dwm_init_mongo():
    """ test Dwm class sets MongoDB client """
    dwm = Dwm(name='test', mongo=DB)
    assert dwm.mongo == DB


def test_dwm_init_default_fields():
    """ test Dwm class initializes with default fields empty """
    dwm = Dwm(name='test', mongo=DB)
    assert dwm.fields == []


def test_dwm_init_default_udf():
    """ test Dwm class initializes with default fields empty """
    dwm = Dwm(name='test', mongo=DB)
    assert dwm.udfs == []

# Initialize with field settings


def test_dwm_init_fields():
    """ test Dwm class initializes with defined field set """
    fields = {
        'field1': {
            'lookup': ['genericLookup', 'genericRegex', 'fieldSpecificRegex',
                       'fieldSpecificLookup', 'normLookup', 'normIncludes'],
            'derive': [
                {
                    'type': 'deriveIncludes',
                    'fieldSet': ['field2'],
                    'options': []
                }
            ]
        }
    }

    dwm = Dwm(name='test', mongo=DB, fields=fields)
    assert dwm.fields == fields


@raises(ValueError)
def test_dwm_init_fields_badlookup():
    """ test Dwm class raises error with bad lookup type """
    fields = {
        'field1': {
            'lookup': ['genericLookup', 'genericRegex', 'fieldSpecificRegex',
                       'fieldSpecificLookup', 'normLookup', 'badlookup'],
            'derive': [
                {
                    'type': 'deriveIncludes',
                    'fieldSet': ['field2'],
                    'options': []
                }
            ]
        }
    }

    dwm = Dwm(name='test', mongo=DB, fields=fields)


@raises(ValueError)
def test_dwm_init_fields_badderive():
    """ test Dwm class raises error with bad derive type """
    fields = {
        'field1': {
            'lookup': ['genericLookup', 'genericRegex', 'fieldSpecificRegex',
                       'fieldSpecificLookup', 'normLookup', 'normIncludes'],
            'derive': [
                {
                    'type': 'badderive',
                    'fieldSet': ['field2'],
                    'options': []
                }
            ]
        }
    }

    dwm = Dwm(name='test', mongo=DB, fields=fields)


@raises(ValueError)
def test_dwm_init_fields_badopt():
    """ test Dwm class raises error with bad derive option type """
    fields = {
        'field1': {
            'lookup': ['genericLookup', 'genericRegex', 'fieldSpecificRegex',
                       'fieldSpecificLookup', 'normLookup', 'normIncludes'],
            'derive': [
                {
                    'type': 'deriveIncludes',
                    'fieldSet': ['field2'],
                    'options': ['badoption']
                }
            ]
        }
    }

    dwm = Dwm(name='test', mongo=DB, fields=fields)


# Initialize with User-Defined Functions

def udf_example_good(data, hist):
    """ example UDF function for testing; has expected parameters """
    return data, hist


def test_dwm_init_udf():
    """ test Dwm class initializes with defined UDFs """
    udf_set = {
        'beforeGenericValLookup': udf_example_good,
        'beforeGenericValRegex': udf_example_good,
        'beforeFieldSpecificLookup': udf_example_good,
        'beforeFieldSpecificRegex': udf_example_good,
        'beforeNormLookup': udf_example_good,
        'beforeNormRegex': udf_example_good,
        'beforeNormIncludes': udf_example_good,
        'beforeDerive': udf_example_good,
        'afterAll': udf_example_good
    }

    dwm = Dwm(name='test', mongo=DB, udfs=udf_set)
    assert dwm.udfs = udf_set


@raises(ValueError)
def test_dwm_init_udf_badpos():
    """ test Dwm class raises error with invalid position """

    udf_set = {
        'badposition': udf_example_good
    }

    dwm = Dwm(name='test', mongo=DB, udfs=udf_set)