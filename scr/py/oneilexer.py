#!/usr/bin/python
# module oneilexer

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
from oneistream import *


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
