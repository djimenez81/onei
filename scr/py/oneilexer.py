#!/usr/bin/python
# module oneiengine

# Copyright (c) 2017 Universidad de Costa Rica
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
        return self._content

    def getType(self):
        return self._type


class OneiStream:
    # This class implements the token stream of the lexer that will be passed
    # to the parser. Mainly a container with a little bit of behavior.

    ##############
    # ATTRIBUTES #
    ##############
    _stream = []
    _tokenN = 0
    _nextP  = 0

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
        return self._stream

    def length(self):
        return self._tokenN

    ###########
    # METHODS #
    ###########
    def add(self,token):
        self._stream.append(token)
        self._tokenN += 1

    def next(self):
        if self._tokenN > self._nextP:
            token = self._stream[self._nextP]
            self._nextP += 1
            return token
        else:
            return None

    def previous(self):
        if self._nextP < 2:
            return None
        else:
            token = self._stream[self._nextP-2]
            self._nextP -= 1
            return token

    def final(self):
        return self._stream[-1]

    def position(self):
        return self._nextP

    def toBeginning(self):
        self._nextP = 0

    def first(self):
        self._nextP = 0
        return self.next()

    def search(self,content):
        self.toBeginning()
        isit = False
        k = 0
        while (k < self._tokenN) and (not isit):
            isit = (content == self.next().getContent())
            k += 1
        return isit


    def isSimpleStatement(self):
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

    def isFunctionCall(self):
        # pdb.set_trace()
        if self.isSimpleStatement():
            parenCount = 0
            if self.first().getType() == NAME:
                flag = True
                dotExpected = True
                while flag:
                    tok = self.next()
                    if tok == None:
                        return False
                    elif dotExpected and tok.getContent() == DOT_SYMBOL:
                        dotExpected = False
                    elif dotExpected and tok.getContent() == LPAREN_SYMBOL:
                        flag = False
                        parenCount += 1
                    elif not dotExpected and tok.getType() == NAME:
                        dotExpected = True
                    else:
                        return False
                tok = self.next()
                flag = (tok != None)
                while flag:
                    if tok.getContent() == LPAREN_SYMBOL:
                        parenCount += 1
                    elif tok.getContent() == RPAREN_SYMBOL:
                        parenCount -= 1
                    if parenCount == 0:
                        flag = False
                    else:
                        tok = self.next()
                        flag = (tok != None)
                delta = self.length() - self.position()
                if parenCount > 0:
                    return False
                elif  delta > 1:
                    return False
                elif delta == 1 and self.next().getContent() == END_LINE_SYMBOL:
                    return True
                elif delta == 0:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False


class OneiLexer:
    # This class implements a lexer for the Onei language.

    ##############
    # ATTRIBUTES #
    ##############
    _numberOfLines = 0
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
        return self._lines

    def getStream(self):
        return self._stream

    def getTokenLine(self):
        return self._tokenLine

    def getPath(self):
        return self._path

    def getName(self):
        return self._name


    ###########
    # METHODS #
    ###########
    def tokenize(self, filename):
        # This method takes the file, and performes the tokenization, that is,
        # it realizes the basic lexical analysis.
        # We first get the path and names of the module.
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
        # This method adds a line to the list of lines.
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
        thisUnit = ''
        for char in line:
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
                        self._currentState == COMMENT_READ
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
                    self._currentState == SPACE_READ
                    thisUnit = ''
                else:
                    self._stream.add(OneiToken(thisUnit, NUMBER))
                    self._currentState == SPACE_READ
                    thisUnit = ''
                    if char in COMPARATOR_SYMBS:
                        thisUnit += char
                        self._currentState = OPERATOR
                    elif char == DOT_SYMBOL:
                        thisUnit += char
                        self._currentState = DOT_READ
                    elif char in DELIMITERS:
                        self._stream.add(OneiToken(char,DELIMITER))
                    elif char in BIN_OPERATORS:
                        self._stream.add(OneiToken(char,OPERATOR))
                    elif char == COMMENT_SYMBOL:
                        self._currentState = COMMENT_READ
                    elif char == STRING_SYMBOL:
                        self._currentState = STRING_READ
        if self._currentState != SPACE_READ:
            # After finish reading, it is likely that the last word was not
            # entered in the split array.
            if thisUnit in KEYWORDS:
                self._stream.add(OneiToken(thisUnit, KEYWORD))
            else:
                self._stream.add(OneiToken(thisUnit, self._currentState))
            # More lines might be splitted in the future, so, state must be left
            # in the appropriate state.
            self._currentState = SPACE_READ
