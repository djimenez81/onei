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
from oneilexer     import *
from oneiparser    import *
from oneiconstants import *


#############
#############
##         ##
## METHODS ##
##         ##
#############
#############


###################
###################
###################
###             ###
###             ###
###   CLASSES   ###
###             ###
###             ###
###################
###################
###################

#############
#############
##         ##
##  CLASS  ##
##         ##
#############
#############
class OneiASTNode:
    # This class implements a node in the Abstract Syntax Tree (AST). It is not
    # simply a container, and the parsing itself in a large messure happens on
    # this class.
    #
    # EXAMPLE OF USE:
    #
    # node = OneiASTNode()
    # node = OneiASTNode(NODE_TYPE)
    #

    ###########
    # CREATOR #
    ###########
    def __init__(self, nodeType = EMPTY_NODE):
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

    ############
    # FUNCTION #
    ############
    def getLeftChild(self):
        # Standard getter. It returns the left child node.
        #
        # EXAMPLE OF USE:
        #
        # left_child_node = node.getLeftChild()
        #
        return self._leftChild

    ############
    # FUNCTION #
    ############
    def getRightChild(self):
        # Standard getter. It returns the right child node.
        #
        # EXAMPLE OF USE:
        #
        # right_child_node = node.getRightChild()
        #
        return self._rightChild

    ############
    # FUNCTION #
    ############
    def getNext(self):
        # Standard getter. It returns the next node.
        #
        # EXAMPLE OF USE:
        #
        # next_node = node.getNext()
        #
        return self._next

    ############
    # FUNCTION #
    ############
    def getValue(self):
        # Standard getter. It returns a string with the value of the node.
        #
        # EXAMPLE OF USE:
        #
        # value_string = node.getValue()
        #
        # NOTE: So far, this function makes no type checking.
        #
        return self._value

    ############
    # FUNCTION #
    ############
    def getType(self):
        # Standard getter. It returns a string with the specification of the
        # type of the node.
        #
        # EXAMPLE OF USE:
        #
        # type_string = node.getType()
        #
        # NOTE: So far, this function makes no type checking.
        #
        return self._nodeType

    ######################## #####
    #############################
    ##                         ##
    ##  FUNCTIONS AND METHODS  ##
    ##                         ##
    #############################
    #############################

    ##########
    # METHOD #
    ##########
    def process(self,stream):
        # This method implements a lot of the logic of the parsing. It receives
        # a stream, and if it can be directly parsed, it does, if not, it
        # divides such stream into substreams and sends it back to itself.
        #
        # EXAMPLE OF USE:
        #
        # node.process(stream)
        #
        # NOTE: This function is in the process of being written. It is relevant
        #       at this point to have a priority of operations to take as a base
        #       of work.
        #        - Assignment ('=')
        #        - Logical predicate (and, or, xor, not)
        #        - Comparison ('==', '!=', '>', etc)
        #        - First order operation ('+', '-', include signed statements)
        #        - Second order operation ('*', '/')
        #        - Exponentials ('^')
        #        - Subfuncion call (like in 'object.fun1(arg).fun2(arg1,arg2)')
        #        - Function call
        #
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
            elif tempType == KEYWORD and tempVal in BOOLEANS:
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
    # This class implements an Abstract Syntax Tree (AST) for Onei. Thus far,
    # most of the logic is in the node, and not in this class.
    #
    # EXAMPLE OF USE:
    #
    # ast = OneiAST(stream)
    #
    # NOTE: Thus far this is a container. It has absoltuely no logic, and has no
    #       tools to modify the contents once these have been initialized.
    #

    ##############
    # ATTRIBUTES #
    ##############
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
        # Standard getter. It returns the root node of the syntax tree.
        #
        # EXAMPLE OF USE:
        #
        # ast.getRoot()
        #
        return self._root

    ###########
    # METHODS #
    ###########



class OneiParser:
    # This class is the parser. At this point is just slightly more than a
    # container.
    #
    # EXAMPLE OF USE:
    #
    # parser = OneiParser()
    #

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

    ############
    # FUNCTION #
    ############
    def getASTList(self):
        # Standard getter. It returns a list of abstract syntax tree objects.
        #
        # EXAMPLE OF USE:
        #
        # ast_list = parser.getASTList()
        #
        return self._ASTList

    #############################
    #############################
    ##                         ##
    ##  FUNCTIONS AND METHODS  ##
    ##                         ##
    #############################
    #############################

    ##########
    # METHOD #
    ##########
    def add(self,stream):
        # This method takes a stream and adds it to the list of sintax trees.
        #
        # EXAMPLE OF USE:
        #
        # parser.add(stream)
        #
        tempAST = OneiAST(stream)
        # tempAST.add(stream)
        self._ASTList.append(tempAST)
