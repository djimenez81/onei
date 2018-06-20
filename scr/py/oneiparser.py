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
## ABOUT splitStream FUNCTION:
# As it is implemented right now, it works only if there is no errors in the
# stream. The function should check for certain simple errors. Some of them
# should be:
#
# 1. There are no missing or extra end statements.
# 2. There is no improper nesting, (No object can be nested inside another, etc)
# 3. Keywords, particularly those that are contained in DEFINERS, SCOPERS,
#    ELSERS, DECLARERS and the END_SING, are not used outside of context.



###############
###############
##           ##
##  IMPORTS  ##
##           ##
###############
###############
import pdb #; pdb.set_trace()
from oneilexer import *
from oneiconstants import *


#############
#############
##         ##
## METHODS ##
##         ##
#############
#############
def splitStream(stream):
    # This function makes a first pass to the stream received, trying to split
    # it into its main components.
    streamArray = []
    tempStream = OneiStream()
    stream.toBeginning()
    N = stream.length()
    k = 0
    scopeCount = 0
    scoping    = False
    initiating = True
    declaring  = False
    while k < N:
        k += 1
        tok = stream.next()
        tempStream.add(tok)
        content = tok.getContent()
        if initiating:
            initiating = False
            if content in DEFINERS:
                scoping = True
                scopeCount += 1
        elif scoping:
            if content in DECLARERS and not declaring:
                declaring = True
                scopeCount += 1
            elif content in DEFINERS:
                scopeCount += 1
            elif content in SCOPERS:
                scopeCount += 1
            elif content == END_SING:
                scopeCount -= 1
                if declaring:
                    declaring = False
                if scopeCount == 0:
                    streamArray.append(tempStream)
                    tempStream = OneiStream()
                    initiating = True
                    scoping = False
        else:
            if content == END_LINE_SYMBOL:
                streamArray.append(tempStream)
                tempStream = OneiStream()
                initiating = True
    return streamArray


#############
#############
##         ##
## CLASSES ##
##         ##
#############
#############




class OneiASTNode:
    # This class implements a node in the Abstract Syntax Tree (AST).

    ###########
    # CREATOR #
    ###########
    def __init__(self,nodeType=EMPTY_NODE):
#        self._children = {}
        self._leftChild  = None
        self._rightChild = None
        self._next       = None
        self._value      = None
        if nodeType in NODE_TYPES:
            self._nodeType = nodeType
        else:
            ## Here we should do something to catch errors
            pass

    #######################
    # GETTERS AND SETTERS #
    #######################
#     def getChildren(self):
#         return self._children

    def getLeftChild(self):
        return self._leftChild

    def getRightChild(self):
        return self._rightChild

    def getNext(self):
        return self._next

    def getValue(self):
        return self._value

    def getType(self):
        return self._nodeType

    ###########
    # METHODS #
    ###########
    def process(self,stream):
        if self._nodeType == ROOT_NODE:
            self._next       = None
            self._rightChild = None
            self._leftChild  = OneiASTNode()
            self._leftChild.process(stream)
        elif stream.length() == 0:
            # This should not occure. Here just in case
            print('I received an empty stream. YOU SHOULD NOT BE READING THIS.')
        elif stream.length() == 1:
            self._next     = None
            self._leftChild = None
            self._rightChild = None
            tok = stream.first()
            tempType = tok.getType()
            tempVal  = tok.getContent()
            if tempType == NAME:
                self._nodeType = ID_NODE
                self._value = tempVal
            elif tempType == NUMBER:
                if DOT_SYMBOL in tempVal or EXPONENT_SYMBOL in tempVal:
                    self._nodeType = FLOAT_NODE
                else:
                    self._nodeType = INT_NODE
                self._value = tempVal
            elif tempType == KEYWORD:
                if tempVal in BOOLEANS:
                    self._nodeType = BOOL_NODE
                    self._value = tempVal
            else:
                print('I am unsure what I received. YOU SHOULD NOT BE READING THIS')
        elif stream.isSimpleStatement():
            # Here we assume that the statement is properly implemented
            if stream.search(ASSIGNMENT_SYMBOL):
                self._nodeType = ASSIGNMENT_NODE
                stream.toBeginning()
                flag = True
                leftStream = OneiStream()
                rightStream = OneiStream()
                while flag:
                    tok = stream.next()
                    if tok.getContent() == ASSIGNMENT_SYMBOL:
                        flag = False
                    else:
                        leftStream.add(tok)
                flag = True
                while flag:
                    tok = stream.next()
                    if tok == None:
                        flag = False
                    elif tok.getContent() == END_LINE_SYMBOL:
                        flag = False
                    else:
                        rightStream.add(tok)
                self._leftChild = OneiASTNode()
                self._leftChild.process(leftStream)
                self._rightChild = OneiASTNode()
                self._rightChild.process(rightStream)


        else:
            print('This option has not yet been implemented')



class OneiAST:
    # This class implements an Abstract Syntax Tree (AST) for Onei.

    ##############
    # ATTRIBUTES #
    ##############
#    _imports      = []
#    _setup        = []
#    _objectList   = []
#    _functionList = []
#    _typeTable    = []
    _root = OneiASTNode(ROOT_NODE)
    _searchTable  = {}

    ###########
    # CREATOR #
    ###########
    def __init__(self, stream):
        self._root = OneiASTNode(ROOT_NODE)
        self._root.process(stream)

    #######################
    # GETTERS AND SETTERS #
    #######################
    def getRoot(self):
        return self._root

    ###########
    # METHODS #
    ###########



class OneiParser:
    # This class implements a parser for Onei.

    ##############
    # ATTRIBUTES #
    ##############
    _ASTList = []


    ###########
    # CREATOR #
    ###########
    def __init__(self):
        pass

    #######################
    # GETTERS AND SETTERS #
    #######################
    def getASTList(self):
        return self._ASTList

    ###########
    # METHODS #
    ###########
    def add(self,stream):
        # This method takes a stream and adds it to the list of sintax trees.
        tempAST = OneiAST(stream)
        # tempAST.add(stream)
        self._ASTList.append(tempAST)
