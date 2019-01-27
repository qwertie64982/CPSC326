#
# Author: Maxwell Sherman
# Course: CPSC 326, Spring 2019
# Assignment: 2
# Description:
#   Lexer class, to be used in hw2.py
#------------------------------------------

import mypl_token as token
import mypl_error as error

class Lexer(object):
    def __init__(self, input_stream):
        self.line = 1
        self.column = 0
        self.input_stream = input_stream
    
    def __peek(self):
        pos = self.input_stream.tell()
        symbol = self.input_stream.read(1)
        self.input_stream.seek(pos)
        return symbol
    
    def __read(self):
        return self.input_stream.read(1)
    
    def next_token(self):
        peekValue = self.__peek() # for efficiency purposes
        
        if peekValue == "":
            return token.Token(token.EOS, "", self.line, self.column)
        elif peekValue.isdigit():
            curr_lexeme = self.__read()
            isFloat = False
            while self.__peek().isdigit() or self.__peek() == ".":
                if self.__peek() == "." and not isFloat:
                    # check if first part is intval
                    if (curr_lexeme[0] == "0" and len(curr_lexeme) == 1) or curr_lexeme[0] != "0" and len(curr_lexeme) > 1:
                        isFloat = True
                    else:
                        raise error.MyPLError("float starts with 0", self.line, self.column)
                elif self.__peek() == "." and isFloat:
                    raise error.MyPLError("two decimal points in one number", self.line, self.column)
                # safe zone from here down
                curr_lexeme += self.read()
            if isFloat:
                return token.Token(token.FLOATVAL, float(curr_lexeme), self.line, self.column)
            else:
                return token.Token(token.INTVAL, int(curr_lexeme), self.line, self.column)
                
        elif peekValue.isalpha():
            curr_lexeme = self.__read()
            isDefinitelyID = False
            while self.__peek().isalpha() or self.__peek().isdigit() or self.__peek() == "_":
                if self.__peek().isdigit() or self.__peek() == "_":
                    isDefinitelyID = True
                curr_lexeme += self.__read()
            
            if isDefinitelyID:
                return token.Token(token.ID, curr_lexeme, self.line, self.column)
            elif curr_lexeme == "bool":
                return token.Token(token.BOOLTYPE, curr_lexeme, self.line, self.column)
            elif curr_lexeme == "int":
                return token.Token(token.INTTYPE, curr_lexeme, self.line, self.column)
            elif curr_lexeme == "float":
                return token.Token(token.FLOATTYPE, curr_lexeme, self.line, self.column)
            elif curr_lexeme == "str":
                return token.Token(token.STRINGTYPE, curr_lexeme, self.line, self.column)
            elif curr_lexeme == "struct":
                return token.Token(token.STRUCTTYPE, curr_lexeme, self.line, self.column)
            elif curr_lexeme == "and":
                return token.Token(token.AND, curr_lexeme, self.line, self.column)
            elif curr_lexeme == "or":
                return token.Token(token.OR, curr_lexeme, self.line, self.column)
            elif curr_lexeme == "not":
                return token.Token(token.NOT, curr_lexeme, self.line, self.column)
            elif curr_lexeme == "while":
                return token.Token(token.WHILE, curr_lexeme, self.line, self.column)
            elif curr_lexeme == "do":
                return token.Token(token.DO, curr_lexeme, self.line, self.column)
            elif curr_lexeme == "if":
                return token.Token(token.IF, curr_lexeme, self.line, self.column)
            elif curr_lexeme == "then":
                return token.Token(token.THEN, curr_lexeme, self.line, self.column)
            elif curr_lexeme == "else":
                return token.Token(token.ELSE, curr_lexeme, self.line, self.column)
            elif curr_lexeme == "elif":
                return token.Token(token.ELIF, curr_lexeme, self.line, self.column)
            elif curr_lexeme == "end":
                return token.Token(token.END, curr_lexeme, self.line, self.column)
            elif curr_lexeme == "fun":
                return token.Token(token.FUN, curr_lexeme, self.line, self.column)
            elif curr_lexeme == "var":
                return token.Token(token.VAR, curr_lexeme, self.line, self.column)
            elif curr_lexeme == "set":
                return token.Token(token.SET, curr_lexeme, self.line, self.column)
            elif curr_lexeme == "return":
                return token.Token(token.RETURN, curr_lexeme, self.line, self.column)
            elif curr_lexeme == "new":
                return token.Token(token.NEW, curr_lexeme, self.line, self.column)
            elif curr_lexeme == "nil":
                return token.Token(token.NIL, curr_lexeme, self.line, self.column)
            elif curr_lexeme == "true" or curr_lexeme == "false":
                return token.Token(token.BOOLVAL, curr_lexeme, self.line, self.column)
            else:
                return token.Token(token.ID, curr_lexeme, self.line, self.column)
        elif peekValue.isspace():
            self.__read()
            return self.next_token()
        elif peekValue == ";":
            self.__read()
            return token.Token(token.SEMICOLON, ";", self.line, self.column)
        elif peekValue == '"':
            curr_lexeme = ""
            self.__read() # throw out first quotation marks
            while self.__peek() != '"' and self.__peek() != "\n":
                curr_lexeme += self.__read()
            if self.__peek() == '"':
                self.__read()
                return token.Token(token.STRINGVAL, curr_lexeme, self.line, self.column)
            elif self.__peek() == "\n":
                raise error.MyPLError("unexpected newline in string", self.line, self.column)
            else:
                raise error.MyPLError("something strange happened", self.line, self.column)
        elif peekValue == "=":
            self.__read()
            if self.__peek() == "=":
                self.__read()
                return token.Token(token.EQUAL, "==", self.line, self.column)
            else:
                return token.Token(token.ASSIGN, "=", self.line, self.column)
        elif peekValue == ",":
            self.__read() # reading here instead of in the return so that line and column update properly
            return token.Token(token.COMMA, ",", self.line, self.column)
        elif peekValue == ":":
            self.__read()
            return token.Token(token.COLON, ":", self.line, self.column)
        elif peekValue == "/":
            self.__read()
            return token.Token(token.DIVIDE, "/", self.line, self.column)
        elif peekValue == ".":
            self.__read()
            return token.Token(token.DOT, ".", self.line, self.column)
        elif peekValue == ">":
            self.__read()
            if self.__peek() == "=":
                self.__read()
                return token.Token(token.GREATER_THAN_EQUAL, ">=", self.line, self.column)
            else:
                return token.Token(token.GREATER_THAN, ">", self.line, self.column)
        elif peekValue == "<":
            self.__read()
            if self.__peek() == "=":
                self.__read()
                return token.Token(token.LESS_THAN_EQUAL, "<=", self.line, self.column)
            else:
                return token.Token(token.LESS_THAN, "<", self.line, self.column)
        elif peekValue == "!":
            self.__read()
            if self.__peek() == "=":
                self.__read()
                return token.Token(token.NOT_EQUAL, "!=", self.line, self.column)
            else:
                raise error.MyPLError("unexpected character '!'", self.line, self.column)
        elif peekValue == "(":
            self.__read()
            return token.Token(token.LPAREN, "(", self.line, self.column)
        elif peekValue == ")":
            self.__read()
            return token.Token(token.RPAREN, ")", self.line, self.column)
        elif peekValue == "-":
            self.__read()
            return token.Token(token.MINUS, "-", self.line, self.column)
        elif peekValue == "+":
            self.__read()
            return token.Token(token.PLUS, "+", self.line, self.column)
