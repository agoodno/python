from sqlobject import *
import re

useQuotedIdentifiers = False

class MixedCaseUnderscoreANSIStyle(Style):
    """
    This style create all names in ANSI standard upper-case with underscores
    """

    def pythonAttrToDBColumn(self, attr):
        return mixedToUpper(attr)

    def dbColumnToPythonAttr(self, col):
        return upperToMixed(col)

    def pythonClassToDBTable(self, className):
        return mixedToUpper(className)

    def dbTableToPythonClass(self, table):
        return table[0].upper() + upperToMixed(table[1:])

    def pythonClassToDBTableReference(self, className):
        print "*" + className + "*"
        return self.tableReference(self.pythonClassToDBTable(className))

    def tableReference(self, table):
        return maybeQuoteStr("ID")


############################################################
## Text utilities
############################################################
_mixedToUpperRE = re.compile(r'[a-zA-Z]+')
def mixedToUpper(name):
    """
        Given 'product', will return 'PRODUCT'
        Given 'productId', will return 'PRODUCT_ID'
        Given 'productName', will return 'PRODUCT_NAME'
    """
    def mixedToUpperSub(match):
        upperWithUnderscoresStr = match.group(0)[0]
        for matchChar in match.group(0)[1:]:
            if (matchChar == matchChar.upper()):
                upperWithUnderscoresStr += '_%s' % matchChar
            else:
                upperWithUnderscoresStr += matchChar
        return maybeQuoteStr(upperWithUnderscoresStr.upper())
    
    #print "name=%s" % name
    if name.endswith('ID'):
        return mixedToUpper(name[:-2]) + "_ID"

    trans = _mixedToUpperRE.sub(mixedToUpperSub, name)
    #if trans.startswith('_'):
    #    trans = trans[1:]
    #print "dbname=%s" % trans
    #print "classname=%s" % upperToMixed(trans)
    return trans

_upperToMixedRE = re.compile('_.')
def upperToMixed(name):
    """
        Given 'PRODUCT', will return 'product'
        Given 'PRODUCT_ID', will return 'productId'
        Given 'PRODUCT_NAME', will return 'productName'
    """
    return _upperToMixedRE.sub(lambda m: m.group(0)[1].upper(), name.lower())

def maybeQuoteStr(unquotedStr):
    if useQuotedIdentifiers:
        return "\"" + unquotedStr + "\""
    return unquotedStr

