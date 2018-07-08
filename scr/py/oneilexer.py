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
#
#
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
    # This class implements a basic lexical token object. For all purposes, it
    # is simply a container of the tipe and content of the token in the stream.
    # The container is, for the most part, static, in the sense that there is no
    # setters, and thus, after creation, there is no tool to change those
    # values.
    #
    # EXAMPLE OF USE:
    #
    # token = OneiToken('function',KEYWORD)
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

    ############
    # FUNCTION #
    ############
    def getContent(self):
        # Self explanatory. This funtion returns the string of content of the
        # token.
        #
        # EXAMPLE OF USE:
        #
        # content_string = token.getContent()
        #
        return self._content

    ############
    # FUNCTION #
    ############
    def getType(self):
        # Self explanatory. This funtion returns the string of type of the
        # token.
        #
        # EXAMPLE OF USE:
        #
        # type_string = token.getType()
        #
        return self._type


class OneiStream:
    # This class implements the token stream of the lexer that will be passed
    # to the parser. It implements tools to traverse the stream, and to check
    # if the string corresponds to different pieces of code.
    #
    # EXAMPLE OF USE:
    #
    # token = OneiStream()
    #

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

    ############
    # FUNCTION #
    ############
    def getStream(self):
        # This method is a standard getter, and returns the list that contains
        # all the tokens.
        #
        # EXAMPLE OF USE:
        #
        # stream_token_list = token.getStream()
        #
        # NOTE: Thus far we have not used this function, and it should be
        #       considered for eliminations.
        #
        return self._stream


    ############
    # FUNCTION #
    ############
    def length(self):
        # This function returns a non negative integer that corresponds to the
        # number of tokens contained in the stream.
        #
        # EXAMPLE OF USE:
        #
        # length_number = token.length()
        #
        return self._tokenN


    ############
    # FUNCTION #
    ############
    def position(self):
        # This function returns a non negative integer that corresponds to the
        # current position while traversing the stream.
        #
        # EXAMPLE OF USE:
        #
        # position_number = token.position()
        #
        return self._nextP-1

    #############################
    #############################
    ##                         ##
    ##  METHODS AND FUNCTIONS  ##
    ##                         ##
    #############################
    #############################

    ##########
    # METHOD #
    ##########
    def add(self,token):
        # This method takes a token object as the last element of the stream.
        #
        # EXAMPLE OF USE:
        #
        # steam.add(token)
        #
        # NOTE: There is no implementation for type checking. This means that
        #       currently, the user could add any object or variable to the
        #       stream. Careful use should suggest that only tokens are used,
        #       but it should be considered to implement such check.
        #
        self._stream.append(token)
        self._tokenN += 1


    ############
    # FUNCTION #
    ############
    def next(self):
        # This function moves the current position in the stream to one position
        # ahead, and returns the token object at that position. If the current
        # position is already at the end of the stream, it returns a None
        # object.
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


    ############
    # FUNCTION #
    ############
    def previous(self):
        # This function moves the current position in the stream to one position
        # behind, and returns the token object at that position. If the current
        # position is already at the beginning of the stream, it returns a None
        # object.
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

    ############
    # FUNCTION #
    ############
    def final(self):
        # This function moves the current position to the end of the stream,
        # and returns the token object at that position.
        #
        # EXAMPLE OF USE:
        #
        # token = stream.final()
        #
        self._nextP = self._tokenN
        return self.previous()

    ############
    # FUNCTION #
    ############
    def position(self):
        # This function returns the non negative integer denoting the position
        # currently held within the stream.
        #
        # EXAMPLE OF USE:
        #
        # current_position_number = stream.position()
        #
        return self._nextP

    ##########
    # METHOD #
    ##########
    def toBeginning(self):
        # This method forces the current position to go to the beginning of the
        # stream.
        #
        # EXAMPLE OF USE:
        #
        # stream.toBeginning()
        #
        # NOTE: It should be asked if this method is actually necessary, as most
        #       of its uses could be instead performed by the function 'first'.
        #       Still, it has already been used in a few places on the code, so,
        #       probably it will stay, at least until some major review comes.
        #
        self._nextP = 0


    ############
    # FUNCTION #
    ############
    def inPosition(self,k):
        # This function recieves a non negative integer k, and returns the k-th
        # token in the stream (there is a 0-th elemenet). If k is negative or k
        # exceeds the number of elements in the stream, then it returns a None.
        # This function does not affect the current position.
        #
        # EXAMPLE OF USE:
        #
        # token = stream.inPosition(k)
        #
        # NOTE: This function seems to have not yet been used, and it is not
        #       necessarily consistent with the behavior of the other functions
        #       and methods. Then, one could consider to remove it.
        #
        if k >= self._tokenN or k < 0:
            return None
        else:
            return self._stream[k]

    ############
    # FUNCTION #
    ############
    def first(self):
        # This function moves the current position to the first element of the
        # stream, returns such element, and moves the current position to the
        # next position.
        #
        # EXAMPLE OF USE:
        #
        # token = stream.first()
        #
        self._nextP = 0
        return self.next()

    ############
    # FUNCTION #
    ############
    def search(self,content):
        # This function takes a string 'content' as an argument and searches the
        # tokens of the stream to check whether or not there is one that has
        # such content. It should be noted that this function returns only a
        # boolean, and not the index or indices of the positions where the
        # content appears, if it does.
        #
        # EXAMPLE OF USE:
        #
        # boolean_answer = stream.search(content)
        #
        self.toBeginning()
        isit = False
        k = 0
        while (k < self._tokenN) and (not isit):
            isit = (content == self.next().getContent())
            k += 1
        return isit


    ############
    # FUNCTION #
    ############
    def isSimpleStatement(self):
        # This function goes over the stream, and checks if it corresponds to a
        # simple statement, and returns a boolean with the anser. This is used
        # mostly when parsing.
        #
        # EXAMPLE OF USE:
        #
        # boolean_answer = stream.isSimpleStatement()
        #
        self.toBeginning()
        isit = True
        i = 0
        while ( i < self._tokenN) and (isit):
            i += 1
            ltoken = self.next().getContent()
            isit = (ltoken not in ELEMENTS)
            if(ltoken == END_LINE_SYMBOL) and (i != self._tokenN):
                isit = False
        return isit

    ############
    # FUNCTION #
    ############
    def isControl(self):
        # This function goes over the stream, and checks if it corresponds to a
        # a control statement, that is, an if, for or while. This function
        # returns a boolean with the anser. This is used mostly when parsing.
        #
        # EXAMPLE OF USE:
        #
        # boolean_answer = stream.isControl()
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

    ############
    # FUNCTION #
    ############
    def isDefinition(self):
        # This function goes over the stream, and checks if it corresponds to a
        # a definition statement, that is, it is defining a function, or another
        # type of object. This function returns a boolean with the anser. This
        # is used mostly when parsing.
        #
        # EXAMPLE OF USE:
        #
        # boolean_answer = stream.isDefinition()
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
                isit = (self.next().getContent() == '->') or (self.next().getContent() == '=')
            if self.final().getContent() == ';':
                return True
            else:
                return False

    ############
    # FUNCTION #
    ############
    def isFunctionCall(self):
        # This function goes over the stream, and checks if it corresponds to a
        # a function call. This function returns a boolean with the anser. This
        # is used mostly when parsing.
        #
        # EXAMPLE OF USE:
        #
        # boolean_answer = stream.isFunctionCall()
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


    ############
    # FUNCTION #
    ############
    def isOperation(self):
        # This function reviews the stream and determines if it corresponds to
        # an operation. An operation is anything that has two parts and an
        # operand in the middle. For example:
        #
        # x * (y + 1)
        #
        # This function returns True if it considers the stream is an operation,
        # and False otherwise.
        #
        # EXAMPLE OF USE:
        #
        # stream.isOperation()
        #
        # NOTE: This method has not been implemented.
        #
        pass



class OneiLexer:
    # This class implements the lexer object for the Onei language. This class
    # contains a lot of behavior. The main function that is going to be used is
    # 'tokenize', but most of the logic is on 'splitLine'. It should be noted
    # that it contains quite a few getters, but no setter. Content should be
    # set through behavior.
    #
    # EXAMPLE OF USE:
    #
    # lexer = OneiLexer()
    #


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
        self._path          = ''
        self._name          = ''

    #######################
    # GETTERS AND SETTERS #
    #######################

    ############
    # FUNCTION #
    ############
    def getLines(self):
        # This function returns the list of lines. The lines come from the text
        # file read.
        #
        # EXAMPLE OF USE:
        #
        # line_list = lexer.getLines()
        #
        return self._lines

    ############
    # FUNCTION #
    ############
    def getStream(self):
        # This function returns the stream object inside the lexer.
        #
        # EXAMPLE OF USE:
        #
        # stream = lexer.getStream()
        #
        return self._stream

    ############
    # FUNCTION #
    ############
    def getTokenLine(self):
        # This function returns the list of token of lines. This is a list of
        # pairs that indicates the number of the token that corresponds to the
        # beginning of the line in question.
        #
        # EXAMPLE OF USE:
        #
        # token_line_list = lexer.getLines()
        #
        return self._tokenLine

    ############
    # FUNCTION #
    ############
    def getPath(self):
        # This function returns the path where the file that was used to
        # generate this lexer object.
        #
        # EXAMPLE OF USE:
        #
        # path_string = lexer.getPath()
        #
        # NOTE: This has not been yet used a lot. But it should, as soon we will
        #       be generating parsing of multiple files.
        #
        return self._path

    ############
    # FUNCTION #
    ############
    def getName(self):
        # This function returns the name of the file that was used to generate
        # this lexer object.
        #
        # EXAMPLE OF USE:
        #
        # name_string = lexer.getName()
        #
        # NOTE: This has not been yet used a lot. But it should, as soon we will
        #       be generating parsing of multiple files.
        #
        return self._name


    ############################
    ############################
    ##                        ##
    ##  METHODS AND FUNCTIONS ##
    ##                        ##
    ############################
    ############################


    ##########
    # METHOD #
    ##########
    def tokenize(self, filename):
        # This method takes the file, and performes the tokenization, that is,
        # it realizes the basic lexical analysis. This method does not have that
        # much logic. It splits the file in lines, and passes everything to
        # addLine.
        #
        # EXAMPLE OF USE:
        #
        # lexer.tokenize('file.onei')
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


    ##########
    # METHOD #
    ##########
    def addLine(self,line):
        # This method takes a line of text from an onei file, makes a simple
        # preprocessing and sends it to the method 'splitLine'. It also keeps
        # track of the line numbering.
        #
        # EXAMPLE OF USE:
        #
        # lexer.addLine(line_string)
        #
        self._numberOfLines += 1
        line = line.strip()
        if len(line) > 0:
            if line[0] != COMMENT_SYMBOL:
                self.splitLine(line)
                self._lines.append([self._numberOfLines, line])
                self._currentState = SPACE_READ
                self._tokenLine.append([self._numberOfLines, self._stream.length()])


    ##########
    # METHOD #
    ##########
    def splitLine(self,line):
        # This method contains most of the logic of the lexer. It takes a string
        # and checks it iteratively character by character, looking for token
        # boundaries, and interpreting each token as it comes, and adding it to
        # the stream.
        #
        # EXAMPLE OF USE:
        #
        # lexer.splitLine(line_string)
        #
        thisUnit = ''
        for char in line:
            if char == END_LINE_SYMBOL:
                # It first check if it is at the end of the line.
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
                # Second it checks if a comment is starting, or if it is already
                # reading a comment.
                if len(thisUnit) > 0:
                    self._stream.add(OneiToken(thisUnit, self._currentState))
                self._currentState = COMMENT_READ
            elif self._currentState == STRING_READ:
                # Checks if it is reading a string variable.
                if char == STRING_SYMBOL:
                    self._stream.add(OneiToken(thisUnit, self._currentState))
                    self._currentState = SPACE_READ
                    thisUnit = ''
                else:
                    thisUnit += char
            elif self._currentState == SPACE_READ:
                # If previous character read was a space.
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
                # Checks for spaces or tabs.
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
