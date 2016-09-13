from .cleaning import DataLookup, RegexLookup, DeriveDataLookup, DeriveDataCopyValue, DeriveDataRegex
from datetime import datetime


def lookupAll(data, configFields, lookupType, db, histObj={}):
    """
    Return a record after having cleaning rules of specified type applied to all fields in the config

    :param dict data: single record (dictionary) to which cleaning rules should be applied
    :param dict configFields: "fields" object from DWM config (see DataDictionary)
    :param string lookupType: Type of lookup to perform/MongoDB collection name. One of 'genericLookup', 'fieldSpecificLookup', 'normLookup', 'genericRegex', 'fieldSpecificRegex', 'normRegex'
    :param MongoClient db: MongoClient instance connected to MongoDB
    :param dict histObj: History object to which changes should be appended
    """

    for field in data.keys():

        if field in configFields.keys() and data[field]!='':

            if lookupType in configFields[field]["lookup"]:

                if lookupType in ['genericLookup', 'fieldSpecificLookup', 'normLookup']:

                    fieldValNew, histObj = DataLookup(fieldVal=data[field], db=db, lookupType=lookupType, fieldName=field, histObj=histObj)

                elif lookupType in ['genericRegex', 'fieldSpecificRegex', 'normRegex']:

                    fieldValNew, histObj = RegexLookup(fieldVal=data[field], db=db, fieldName=field, lookupType=lookupType, histObj=histObj)

                data[field] = fieldValNew

    return data, histObj


def DeriveDataLookupAll(data, configFields, db, histObj={}):
    """
    Return a record after performing derive rules for all fields, based on config

    :param dict data: single record (dictionary) to which cleaning rules should be applied
    :param dict configFields: "fields" object from DWM config (see DataDictionary)
    :param MongoClient db: MongoClient instance connected to MongoDB
    :param dict histObj: History object to which changes should be appended
    """

    for field in data.keys():

        if field in configFields.keys():

            fieldVal = data[field]

            fieldValNew = fieldVal

            for deriveSet in configFields[field]['derive'].keys():

                deriveSetConfig = configFields[field]['derive'][deriveSet]

                if set.issubset(set(deriveSetConfig['fieldSet']), data.keys()):

                    deriveInput = {}

                    for val in deriveSetConfig['fieldSet']:
                        deriveInput[val] = data[val]

                    if deriveSetConfig['type']=='deriveValue':

                        fieldValNew, histObj = DeriveDataLookup(fieldName=field, db=db, deriveInput=deriveInput, overwrite=deriveSetConfig['overwrite'], fieldVal=fieldVal, histObj=histObj, blankIfNoMatch=deriveSetConfig['blankIfNoMatch'])
                    elif deriveSetConfig['type']=='copyValue':

                        fieldValNew, histObj = DeriveDataCopyValue(fieldName=field, deriveInput=deriveInput, overwrite=deriveSetConfig['overwrite'], fieldVal=fieldVal, histObj=histObj)

                    elif deriveSetConfig['type']=='deriveRegex':

                        fieldValNew, histObj = DeriveDataRegex(fieldName=field, db=db, deriveInput=deriveInput, overwrite=deriveSetConfig['overwrite'], fieldVal=fieldVal, histObj=histObj, blankIfNoMatch=deriveSetConfig['blankIfNoMatch'])


                if fieldValNew!=fieldVal:

                    data[field] = fieldValNew

                    break

    return data, histObj
