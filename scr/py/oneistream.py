#!/usr/bin/python
# module oneistream

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


###############
###############
##           ##
##  IMPORTS  ##
##           ##
###############
###############
import pdb #; pdb.set_trace()
from oneiconstants import *


#############
#############
##         ##
## CLASSES ##
##         ##
#############
#############
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


    # We need to implement:
    #  - isAssignment
    #  - isFormula
    #     -- a+b-c*d
    #     -- a==b or a>b
    #  - isImport

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

    def isAssignment(self):
        # This function returns a boolean, it is true if the stream is an
        # assignment an false otherwise. Assigmente is : ID = expression
        #
        #EXAMPLE OF USE:
        #
        #isit = stream.isAssignment()
        #
        self.toBeginning()
        isit = True
        i = 0;
        ltoken1 = self.next().getType()
        ltoken2 = self.next().getContent()
        if((ltoken1 == 'NAME') and  (ltoken2 == '=') ):
            isit = True
            number = True
            operator = False
            while (i < (self._tokenN -3)) and (isit):
                type = self.next().getType()
                if(((type == 'NUMBER')or(type == 'NAME'))and (number)):
                    isit = True
                    number = False
                    operator = True
                elif((type == 'OPERATOR')and(operator)):
                    isit = True
                    number = True
                    opereator = False
                else:
                    isit = False
                i += 1
        else:
            isit = False

        return isit


    def isImport(self):
        # This function returns a boolean, it is true if the stream is an
        # import an false otherwise. Import is :
        #       Import: FROM ID IMPORT importList NL
        #               | IMPORT importList NL
        # And importlist:
        #       importlist:  ID ',' importList
        #                   | ID ';'
        #
        # EXAMPLE OF USE:
        #
        # isit = stream.isAssignment()
        #
        self.toBeginning()
        isit = True
        i = 0;
        ltoken1 = self.next().getContent()
        if (ltoken1 == 'FROM'):
            ltoken2 = self.next().getType()
            ltoken3 = self.next().getContent()
            if ((ltoken2 == 'NAME') and (ltoken3 == 'IMPORT')):
                isit = True
                id = True
                delimiter  = False
                while (i < (self._tokenN - 3)) and (isit):
                    type = self.next().getType()
                    if ((type == 'NAME') and (id)):
                        isit = True
                        id = False
                        delimiter = True
                    elif ((type == 'DELIMITER') and (delimiter)):
                        isit = True
                        id = True
                        delimiter = False
                    else:
                        isit = False
                    i += 1
            else:
                isit = False
        elif (ltoken1 == 'IMPORT'):
            isit = True
            id = True
            delimiter = False
            while (i < (self._tokenN - 1)) and (isit):
                type = self.next().getType()
                if ((type == 'NAME') and (id)):
                    isit = True
                    id = False
                    delimiter = True
                elif ((type == 'DELIMITER') and (delimiter)):
                    isit = True
                    id = True
                    delimiter = False
                else:
                    isit = False
                i += 1
        else:
            isit  = False
        return isit


    def isFormula(self):
        # This function returns a boolean, it is true if the stream is an
        # import an false otherwise. Formula is :
        #       -- a+b-c*d
        #       -- a==b or a>b
        # EXAMPLE OF USE:
        #
        # isit = stream.isFormula()
        #
        #
        self.toBeginning()
        isit = True
        i = 0;
        ltoken1 = self.next().getType()
        if ((ltoken1 == 'NUMBER')or(ltoken1 == 'NAME')):
            if(3 == self._tokenN):
                content = self.next().getContent()
                type = self.next().getType
                if(((content in OPERATORS)or (content in BIN_OPERATORS))) and ((type == 'NAME')or(type == 'NUMBER')):
                    isit = True
            else:
                isit = True
                operand = False
                operator = True
                while (i < (self._tokenN -1)) and (isit):
                    nextToken = self.next()
                    type = nextToken.getType()
                    content = nextToken.getContent()
                    if (((type == 'NAME')or(type == 'NUMBER')) and (operand)):
                        isit = True
                        operand = False
                        operator = True
                    elif ((content in  BIN_OPERATORS) and (operator)):
                        isit = True
                        operand = True
                        operator = False
                    else:
                        isit = False
                    i += 1
                if(operand):
                    isit = False
        else:
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
