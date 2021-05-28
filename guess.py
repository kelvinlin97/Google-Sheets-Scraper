import re

def cellType(cell):
    if cell in ('', None):
        return 'blank'
    #Data Types for Sheets: String, Whole Number, Decimal Number, Booleans, Dates, Money (str, int, float, bool, date, money)

    #Catch all for boolean values
    if(cell == "true" or cell == "false" or cell == "yes" or cell == "no"):
        return 'bool'

    #TODO: Match more date formats
    if re.match(r'\d{4}-\d{2}-\d{2}', cell):
        return 'date'

    #If cells contains a letter, it will always be a string
    if re.search('[a-zA-Z]', cell):
        return 'str'
    elif re.search('\d', cell):
        if re.search(r"\$[^\]]+", cell):
            return 'money'
        elif floatCheck(cell):
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

