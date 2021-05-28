import re
from dateutil.parser import parse

def cellType(cell):
    #Data Types for Sheets: String, Whole Number, Decimal Number, Booleans (str, int, float, bool)

    #Catch all for boolean values
    if(cell == "true" or cell == "false" or cell == "yes" or cell == "no"):
        return 'bool'

    #Date is not a python data type, but must be checked so there aren't any false positives for integer checks
    if parse(cell, fuzzy=False):
        return 'date'

    #If cells contains a letter, it will always be a string
    if re.search('[a-zA-Z]', cell):
        return 'str'
    elif re.search('\d', cell):
        if floatCheck(cell):
            return 'float'
        else:
            return 'int'

def floatCheck(cell):
    decimalCount = 0
    for character in cell:
        if character == ".":
            decimalCount += 1
    if decimalCount == 1:
        return True
    else:
        return False
