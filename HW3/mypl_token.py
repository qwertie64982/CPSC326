# Author: Maxwell Sherman
# Course: CPSC 326, Spring 2019
# Assignment: 3
# Description:
#   Token class, to be used in hw3.py
#------------------------------------------

# tokentype constants
ASSIGN  = "ASSIGN"
COMMA   = "COMMA"
COLON   = "COLON"
DIVIDE  = "DIVIDE"
DOT     = "DOT"
EQUAL   = "EQUAL"
GREATER_THAN        = "GREATER_THAN"
GREATER_THAN_EQUAL  = "GREATER_THAN_EQUAL"
LESS_THAN           = "LESS_THAN"
LESS_THAN_EQUAL     = "LESS_THAN_EQUAL"
NOT_EQUAL   = "NOT_EQUAL"
LPAREN      = "LPAREN"
RPAREN      = "RPAREN"
MINUS       = "MINUS"
MODULO      = "MODULO"
MULTIPLY    = "MULTIPLY"
PLUS        = "PLUS"
SEMICOLON   = "SEMICOLON"
BOOLTYPE    = "BOOLTYPE"
INTTYPE     = "INTTYPE"
FLOATTYPE   = "FLOATYPE"
STRINGTYPE  = "STRINGTYPE"
STRUCTTYPE  = "STRUCTTYPE"
AND     = "AND"
OR      = "OR"
NOT     = "NOT"
WHILE   = "WHILE"
DO      = "DO"
IF      = "IF"
THEN    = "THEN"
ELSE    = "ELSE"
ELIF    = "ELIF"
END     = "END"
FUN     = "FUN"
VAR     = "VAR"
SET     = "SET"
RETURN  = "RETURN"
NEW     = "NEW"
NIL     = "NIL"
EOS     = "EOS"
BOOLVAL     = "BOOLVAL"
INTVAL      = "INTVAL"
FLOATVAL    = "FLOATVAL"
STRINGVAL   = "STRINGVAL"
ID          = "ID"

class Token(object):
    # init method
    def __init__(self, tokentype, lexeme, line, column):
        self.tokentype = tokentype
        self.lexeme = lexeme
        self.line = line
        self.column = column
    
    # str method
    def __str__(self):
        return self.tokentype + " '" + str(self.lexeme) + "' " + str(self.line) + ":" + str(self.column)
