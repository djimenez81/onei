#!/usr/bin/python
# module oneiengine

# Copyright (c) 2018 Universidad de Costa Rica
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#   - Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#   - Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#   - Neither the name of the <organization> nor the names of its contributors
#     may be used to endorse or promote products derived from this software
#     without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL UNIVERSIDAD DE COSTA RICA BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Principal Investigator:
#         David Jimenez <david.jimenezlopez@ucr.ac.cr>
# Assistants:
#         Cristina Soto Rojas
#         Laureano Marin


# #############################################################################
# ##  THIS FILE SHOULD CONTAIN THE PARTS OF THE IMPLEMENTATION OF THE ENGINE ##
# ## (LEXER, PARSER, AST, BYTECODE COMPILER, BYTECODE INTERPRETER, BYTECODE  ##
# ## COMPILER) THAT IS BEING DEVELOPED AND TESTED.                           ##
# #############################################################################


####################
####################
####################
###              ###
###              ###
###   COMMENTS   ###
###              ###
###              ###
####################
####################
####################

# When it lexes something that ends with more than one delimiter, it adds an
# empty demiliter. For example, if one writes the following line
#
# for k in range(n):
#
# it is lexed as:
#
# <token type="KEYWORD" value="for" />
# <token type="NAME" value="k" />
# <token type="KEYWORD" value="in" />
# <token type="NAME" value="range" />
# <token type="DELIMITER" value="(" />
# <token type="NAME" value="n" />
# <token type="DELIMITER" value=")" />
# <token type="DELIMITER" value=":" />
# <token type="DELIMITER" value="" />
#
# Note the last token. It should not be there.
#


###############
###############
##           ##
##  IMPORTS  ##
##           ##
###############
###############
import pdb #; pdb.set_trace()
from os.path import basename, dirname
from oneiconstants import *


#############
#############
##         ##
## METHODS ##
##         ##
#############
#############


#############
#############
##         ##
## CLASSES ##
##         ##
#############
#############
class OneiToken:
    # This class implements a basic lexical token object. Mainly a container.
    #
    # EXAMPLE OF USE:
    #
    # token = OneiToken(theContent, theType)
    #

    ##############
    # ATTRIBUTES #
    ##############
    _content  = ''
    _type     = ''

    ###########
    # CREATOR #
    ###########
    def __init__(self, theContent, theType):
        self._content  = theContent
        self._type     = theType

    #######################
    # GETTERS AND SETTERS #
    #######################
    def getContent(self):
        # Standard getter. It returns the string containing the content of the
        # token.
        #
        # EXAMPLE OF USE:
        #
        # str = token.getContent()
        #
        return self._content

    def getType(self):
        # Standard getter. It returns the string containing the type of the
        # token.
        #
        # EXAMPLE OF USE:
        #
        # str = token.getType()
        #
        return self._type


class OneiStream:
    # This class implements the token stream of the lexer that will be passed
    # to the parser. It contains quite a bit of logic. Among other things, it
    # implements a lot of the logic necessary to recognize the content of
    # substreams to help at the time of parsing.
    #
    # EXAMPLE OF USE:
    #
    # stream = OneiStream()
    #

    ##############
    # ATTRIBUTES #
    ##############
    _stream = [] # List containing the tokens, in order, of the stream.
    _tokenN = 0  # Ammount of tokens presently contained in the stream.
    _nextP  = 0  # Current position on the stream.

    ###########
    # CREATOR #
    ###########
    def __init__(self):
        self._stream = []
        self._tokenN = 0
        self._nextP  = 0

    #######################
    # GETTERS AND SETTERS #
    #######################
    def getStream(self):
        # Standard getter. It returns the list containing the list of tokens of
        # the stream.
        #
        # EXAMPLE OF USE:
        #
        # listOfTokens = stream.getStream()
        #
        # NOTE: It might be a good idea to delete this method. It might not be
        #       the best idea to allow access to the inner workings of the
        #       container.
        #
        return self._stream

    def length(self):
        # This function returns the length of the stream, that is, the amount of
        # tokens in the stream at the present moment. It is implemented as a
        # standard getter, as the object keeps track of the number of tokens
        # that it contains.
        #
        # EXAMPLE OF USE:
        #
        # theLength = stream.length()
        return self._tokenN

    def position(self):
        # This function returns the current position on the stream. It is
        # implemented as a standard getter, as the object itself keeps track of
        # the position it is currently.
        #
        # EXAMPLE OF USE:
        #
        # pos = stream.position()
        #
        # NOTE: We should check if this is being used. I think it is not as
        #       necessary, and if it is not actively used, it would be advisable
        #       to remove it.
        #
        return self._nextP

    ###########
    # METHODS #
    ###########
    def add(self,token):
        # This method adds a token to the stream. It also updates the length of
        # the stream.
        #
        # EXAMPLE OF USE:
        #
        # stream.add(token)
        #
        self._stream.append(token)
        self._tokenN += 1


    def next(self):
        # This function returns the next token on the stream, and advances the
        # current position by one.
        #
        # EXAMPLE OF USE:
        #
        # token = stream.next()
        #
        if self._tokenN > self._nextP:
            token = self._stream[self._nextP]
            self._nextP += 1
            return token
        else:
            return None

    def previous(self):
        # This function returns the previous token on the stream, and moves the
        # current position one place back.
        #
        # EXAMPLE OF USE:
        #
        # token = stream.previous()
        #
        if self._nextP < 1:
            return None
        else:
            self._nextP -= 1
            token = self._stream[self._nextP]
            return token


    def final(self):
        # This function moves the current position to the end of the stream and
        # returns the last token on it.
        #
        # EXAMPLE OF USE:
        #
        # token = stream.final()
        #
        self._nextP = self._tokenN
        return self.previous()


    def toBeginning(self):
        # This method takes the pointer of the current position to the start of
        # the stream.
        #
        # EXAMPLE OF USE:
        #
        # stream.toBeginning()
        #
        self._nextP = 0


    def inPosition(self,k):
        # This function returns the token in a given position on the stream,
        # without modifying the current position. The index k indicates the
        # position of the token desired.
        #
        # EXAMPLE OF USE:
        #
        # token = stream.inPosition(k)
        #
        # NOTE: This function might not be necessary. If it is not used, I
        #       recommend to remove it.
        #
        if k >= self._tokenN:
            return None
        else:
            return self._stream[k]


    def first(self):
        # This function moves the current position to the beggining of the
        # stream and returns the first token on it.
        #
        # EXAMPLE OF USE:
        #
        # token = stream.first()
        #
        self._nextP = 0
        return self.next()


    def search(self,content):
        # This function returns a boolean, that is true if the stream contains
        # the content searched for, and returns false otherwise.
        #
        # EXAMPLE OF USE:
        #
        # isit = stream.search(content)
        #
        self.toBeginning()
        isit = False
        k = 0
        while (k < self._tokenN) and (not isit):
            isit = (content == self.next().getContent())
            k += 1
        return isit


    def isSimpleStatement(self):
        # This function returns a boolean, that is true if the stream is a
        # simple statement, and return false otherwise. A simple statement is,
        # basically, a piece of code that can be a line on the source, or part
        # of a lineself.
        #
        # EXAMPLE OF USE:
        #
        # isit = stream.isSimpleStatement()
        #
        self.toBeginning()
        isit = True
        i = 0
        while ( i < self._tokenN) and (isit):
            i += 1
            ltoken = self.next().getContent()
            isit = (ltoken not in ELEMENTS)
            if(';' == ltoken) and (i != self._tokenN):
                isit = False
        return isit


    def isControl(self):
        # This function returns a boolean, that is true if the piece of code is
        # a complete control statement, and false otherwise. A control statement
        # is a structure of if, for or while.
        #
        # EXAMPLE OF USE:
        #
        # isit = stream.isControl()
        #
        nivel = 0
        i = 0
        if(self.first().getContent() in CTRLELEMENTS):
            self.toBeginning()
            while(i < self._tokenN):
                ntoken = self.next().getContent()
                if(ntoken in CTRLELEMENTS):
                    nivel +=1
                if(ntoken == 'end'):
                    nivel -= 1
                i += 1
            if(nivel == 0) and (self.final().getContent() == 'end'):
                return True
            else:
                return False
        else:
            return  False


    def isDefinition(self):
        # This function returns a boolean, that is true if the stream is a
        # single definition and false otherwise. This might be an Onei object,
        # or it could be definition of variables (input, output or otherwise).
        #
        # EXAMPLE OF USE:
        #
        # isit = stream.isDefinition()
        #
        nivel = 0
        i = 0
        if self.first().getContent() in DEFELEMENTS:
            self.toBeginning()
            while (i < self._tokenN):
                ntoken = self.next().getContent()
                if (ntoken in DEFELEMENTS):
                    nivel += 1
                if (ntoken == 'end'):
                    nivel -= 1
                i += 1
            if (nivel == 0) and (self.final().getContent() == 'end'):
                return True
            else:
                return False
        elif self.first().getContent() in SIMPLEDEFELEMENTS:
            if self.final().getContent() == ';':
                return True
            else:
                return False
        else:
            self.toBeginning()
            isit = False
            i = 0
            while (i < self._tokenN) and (not isit):
                isit = (self.next().getContent() == '->') \
                        or (self.next().getContent() == '=')
            if self.final().getContent() == ';':
                return True
            else:
                return False

    def isFunctionCall(self):
        # This function returns a boolean, that is true if the stream is a
        # function call and false otherwise. This might be an Onei object,
        # or it could be definition of variables (input, output or otherwise).
        #
        # EXAMPLE OF USE:
        #
        # isit = stream.isDefinition()
        #
        if self.isSimpleStatement():
            parenCount = 0
            flag = True
            tok = self.final()
            isit = True
            if tok.getContent() == END_LINE_SYMBOL:
                tok = self.previous()
                if tok.getContent() != RPAREN_SYMBOL:
                    flag = False
                    isit = False
            elif tok.getContent() != RPAREN_SYMBOL:
                flag = False
                isit = False
            while flag:
                content = tok.getContent()
                if content == END_LINE_SYMBOL:
                    isit = False
                    flag = False
                elif content == RPAREN_SYMBOL:
                    parenCount += 1
                elif content == LPAREN_SYMBOL and parenCount > 0:
                    parenCount -= 1
                elif content == LPAREN_SYMBOL and parenCount == 0:
                    isit = False
                    flag = False
                elif parenCount == 0 and (content in OPERATORS or
                                          content in BIN_OPERATORS):
                    isit = False
                    flag = False
                if flag:
                    tok = self.previous()
                    if tok == None:
                        flag = False
            return isit
        else:
            return False



class OneiLexer:
    # This class implements the lexer of the language. It contains quite a bit
    # of logic. Among other things, it implements a lot of the logic necessary
    # to recognize the content of substreams to help at the time of parsing.
    #
    # EXAMPLE OF USE:
    #
    # lexer = OneiLexer()
    #

    ##############
    # ATTRIBUTES #
    ##############
    _numberOfLines = 0 # The number of lines contained on the file.
    _stream        = OneiStream() # stream is the final sequence of tokens.
    _lines         = []
    _currentState  = SPACE_READ # When the line has not been initiated, it is as
                                # if the last charater read had been a space.
    _tokenLine     = [] # This variable contains a variable that keeps count of
                        # what line a token is.
    _path          = ''
    _name          = ''

    ###########
    # CREATOR #
    ###########
    def __init__(self):
        self._numberOfLines = 0
        self._stream        = OneiStream()
        self._lines         = []
        self._currentState  = SPACE_READ
        self._tokenLine     = []
        _path          = ''
        _name          = ''

    #######################
    # GETTERS AND SETTERS #
    #######################
    def getLines(self):
        # Standard getter. It returns a list containing the strings of the lines
        # of code in the file being lexed.
        #
        # EXAMPLE OF USE:
        #
        # listOfLines = lexer.getLines()
        #
        return self._lines

    def getStream(self):
        # Standard getter. It returns the stream object inside the lexer.
        #
        # EXAMPLE OF USE:
        #
        # stream = lexer.getStream()
        #
        return self._stream

    def getTokenLine(self):
        # Standard getter. It returns a list that contains a list of the lines
        # and the specific token at the beginning.
        #
        # EXAMPLE OF USE:
        #
        # tokenLine = lexer.getTokenLine()
        #
        return self._tokenLine

    def getPath(self):
        # Standard getter. It returns a string with the path where the code
        # being lexed is stored.
        #
        # EXAMPLE OF USE:
        #
        # path = lexer.getPath()
        #
        return self._path

    def getName(self):
        # Standard getter. It returns a string with the name of the file
        # containing the code being lexed.
        #
        # EXAMPLE OF USE:
        #
        # path = lexer.getPath()
        #
        return self._name


    ###########
    # METHODS #
    ###########
    def tokenize(self, filename):
        # This method takes the file, and performes the tokenization, that is,
        # it realizes the basic lexical analysis. It takes a string filename
        # (relative or absolute path included).
        #
        # EXAMPLE OF USE:
        #
        # lexer.tokenize('path/file.onei')
        #
        self._path = dirname(filename)
        fullname = basename(filename)
        if '.' in fullname:
            idx = fullname.index('.')
            self._name = fullname[:idx]
        else:
            self._name = fullname
        theFile = open(filename)
        # There should be a way to check if it is a text file or not.
        for line in theFile:
            self.addLine(line)


    def addLine(self,line):
        # This method adds a line to the list of lines, and sends it to be
        # lexed. It takes as an argument a string containing a single line of
        # code.
        #
        # EXAMPLE OF USE:
        #
        # lexer.addLine(line)
        #
        self._numberOfLines += 1
        line = line.strip()
        if len(line) > 0:
            if line[0] != COMMENT_SYMBOL:
                self.splitLine(line)
                self._lines.append([self._numberOfLines, line])
                self._currentState = SPACE_READ
                self._tokenLine.append([self._numberOfLines, self._stream.length()])


    def splitLine(self,line):
        # This method separates each line on the pieces that will be tokenized.
        # It takes a single line of code as input. This method contains most of
        # the logic of the lexing.
        #
        # EXAMPLE OF USE:
        #
        # lexer.splitLine(line)
        #
        thisUnit = ''
        for char in line:
            # pdb.set_trace()
            if char == END_LINE_SYMBOL:
                if self._currentState != SPACE_READ and len(thisUnit) > 0:
                    if len(thisUnit) > 0:
                        if self._currentState == NAME and thisUnit in KEYWORDS:
                            self._stream.add(OneiToken(thisUnit,KEYWORD))
                        else:
                            self._stream.add(OneiToken(thisUnit, self._currentState))
                    self._currentState = SPACE_READ
                    thisUnit = ''
                self._stream.add(OneiToken(END_LINE_SYMBOL,END_LINE))
            elif char == COMMENT_SYMBOL and self._currentState != COMMENT_READ:
                if len(thisUnit) > 0:
                    self._stream.add(OneiToken(thisUnit, self._currentState))
                self._currentState = COMMENT_READ
            elif self._currentState == STRING_READ:
                if char == STRING_SYMBOL:
                    self._stream.add(OneiToken(thisUnit, self._currentState))
                    self._currentState = SPACE_READ
                    thisUnit = ''
                else:
                    thisUnit += char
            elif self._currentState == SPACE_READ:
                # If previous character read was a space
                if char == STRING_SYMBOL:
                    self._currentState = STRING_READ
                elif char.isalpha():
                    thisUnit += char
                    self._currentState = NAME
                elif char.isdigit():
                    thisUnit += char
                    self._currentState = NUMBER
                elif char == DOT_SYMBOL:
                    thisUnit += char
                    self._currentState = NUMBER
                    # After a space, only a number can start with a dot.
                elif char in DELIMITERS:
                    self._stream.add(OneiToken(char, DELIMITER))
                    self._currentState = SPACE_READ
                    thisUnit =''
                elif char in COMPARATOR_SYMBS:
                    thisUnit += char
                    self._currentState = OPERATOR
            elif char == SPACE_SYMBOL or char == TAB_SYMBOL:
                if len(thisUnit) > 0:
                    if self._currentState == NAME and thisUnit in KEYWORDS:
                        self._stream.add(OneiToken(thisUnit,KEYWORD))
                    else:
                        self._stream.add(OneiToken(thisUnit, self._currentState))
                thisUnit = ''
                self._currentState = SPACE_READ
            elif self._currentState == DOT_READ:
                # If previous character read was a dot
                if char == DOT_SYMBOL:
                    thisUnit += char
                    if thisUnit == CONTINUER_SYMBOL:
                        self._stream.add(OneiToken(thisUnit, DELIMITER))
                        self._currentState = SPACE_READ
                        thisUnit = ''
                elif char.isdigit():
                    thisUnit += char
                    self._currentState = NUMBER
                else:
                    self._stream.add(OneiToken(DOT_SYMBOL, DELIMITER))
                    thisUnit = ''
                    if char == COMMENT_SYMBOL:
                        self._currentState = COMMENT_READ
                    elif char == STRING_SYMBOL:
                        self._currentState = STRING_READ
                    elif char in DELIMITERS:
                        self._stream.add(OneiToken(char, DELIMITER))
                        self._currentState = SPACE_READ
                    elif char in COMPARATOR_SYMBS:
                        thisUnit += char
                        self._currentState = OPERATOR
                    elif char.isalpha():
                        thisUnit = char
                        self._currentState = NAME
                    else:
                        self._stream.add(OneiToken(char,UNKNOWN))
                        self._currentState = SPACE_READ
            elif self._currentState == OPERATOR:
                if char in COMPARATOR_SYMBS:
                    thisUnit += char
                    if thisUnit in OPERATORS:
                        self._stream.add(OneiToken(thisUnit,OPERATOR))
                    else:
                        self._stream.add(OneiToken(thisUnit, UNKNOWN))
                    self._currentState = SPACE_READ
                    thisUnit = ''
                else:
                    self._stream.add(OneiToken(thisUnit,OPERATOR))
                    thisUnit = ''
                    if char in BIN_OPERATORS:
                        self._stream.add(OneiToken(char,OPERATOR))
                        self._currentState = SPACE_READ
                    elif char in DELIMITERS:
                        self._stream.add(OneiToken(char,DELIMITER))
                        self._currentState = SPACE_READ
                    elif char == DOT_SYMBOL:
                        thisUnit += char
                        self._currentState = DOT_READ
                    elif char == COMMENT_SYMBOL:
                        self._currentState = COMMENT_READ
                    elif char == STRING_SYMBOL:
                        self._currentState = STRING_READ
                    else:
                        self._stream.add(OneiToken(char,UNKNOWN))
            elif self._currentState == NAME:
                # If we think it is writing a name.
                if char.isalpha() or char.isdigit() or char == UNDERSCORE:
                    thisUnit += char
                else:
                    if thisUnit in KEYWORDS:
                        self._stream.add(OneiToken(thisUnit,KEYWORD))
                    else:
                        self._stream.add(OneiToken(thisUnit,NAME))
                    thisUnit = ''
                    self._currentState = SPACE_READ
                    if char in COMPARATOR_SYMBS:
                        thisUnit += char
                        self._currentState = OPERATOR
                    elif char == DOT_SYMBOL:
                        thisUnit += char
                        self._currentState = DOT_READ
                    elif char in DELIMITERS:
                        self._stream.add(OneiToken(char, DELIMITER))
                        self._currentState = DELIMITER_READ
                    elif char in BIN_OPERATORS:
                        self._stream.add(OneiToken(char, OPERATOR))
                    elif char == COMMENT_SYMBOL:
                        self._currentState = COMMENT_READ
                    elif char == STRING_SYMBOL:
                        self._currentState = STRING_READ
            elif self._currentState == NUMBER:
                if char.isdigit() or char == DOT_SYMBOL \
                                       or char in EXPONENT_SYMBOL:
                    thisUnit += char
                elif char in BIN_OPERATORS and thisUnit[-1] == EXPONENT_SYMBOL:
                    thisUnit += char
                elif char.isalpha():
                    self._stream.add(OneiToken(thisUnit, NUMBER))
                    self._stream.add(OneiToken(char,UNKNOWN))
                    self._currentState = SPACE_READ
                    thisUnit = ''
                else:
                    self._stream.add(OneiToken(thisUnit, NUMBER))
                    self._currentState = SPACE_READ
                    thisUnit = ''
                    if char in COMPARATOR_SYMBS:
                        thisUnit += char
                        self._currentState = OPERATOR
                    elif char == DOT_SYMBOL:
                        thisUnit += char
                        self._currentState = DOT_READ
                    elif char in DELIMITERS:
                        self._stream.add(OneiToken(char,DELIMITER))
                        self._currentState = DELIMITER
                    elif char in BIN_OPERATORS:
                        self._stream.add(OneiToken(char,OPERATOR))
                    elif char == COMMENT_SYMBOL:
                        self._currentState = COMMENT_READ
                    elif char == STRING_SYMBOL:
                        self._currentState = STRING_READ
            elif self._currentState == DELIMITER_READ:
                if char == DOT_SYMBOL:
                    self._stream.add(OneiToken(DOT_SYMBOL, DELIMITER))
                    self._currentState = NAME
                else:
                    self._currentState = SPACE_READ
                    if char == STRING_SYMBOL:
                        self._currentState = STRING_READ
                    elif char.isalpha():
                        thisUnit += char
                        self._currentState = NAME
                    elif char.isdigit():
                        thisUnit += char
                        self._currentState = NUMBER
                    elif char == DOT_SYMBOL:
                        # thisUnit += char
                        self._currentState = NAME
                        # After a space, only a number can start with a dot.
                    elif char in DELIMITERS:
                        self._stream.add(OneiToken(char, DELIMITER))
                        self._currentState = DELIMITER_READ
                        # self._currentState = SPACE_READ
                        thisUnit =''
                    elif char in COMPARATOR_SYMBS:
                        thisUnit += char
                        self._currentState = OPERATOR

        if self._currentState != SPACE_READ:
            # After finish reading, it is likely that the last word was not
            # entered in the split array.
            if thisUnit in KEYWORDS:
                self._stream.add(OneiToken(thisUnit, KEYWORD))
            elif self._currentState != DELIMITER_READ:
                self._stream.add(OneiToken(thisUnit, self._currentState))
            # More lines might be splitted in the future, so, state must be left
            # in the appropriate state.
            self._currentState = SPACE_READ
