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


######################
######################
##                  ##
## GLOBAL CONSTANTS ##
##                  ##
######################
######################
DEFINERS  = ['agent',   'environment',  'exchange', 'function', 'io',
            'item',     'message',      'patch',    'rule',     'setup',
            'table']

SCOPERS   = ['for', 'if','while']

ELSERS    = ['elseif', 'else']

DECLARERS = ['attributes','input', 'output','variables']

KEYWORDY = ['and',      'array',    'boolean',  'character',    'dictionary',
            'extends',  'false',    'float',    'import',       'in',
            'integer',  'list',     'not',      'or',           'pass',
            'self',     'string',   'true',     'xor']

END_SING   = 'end'
COLON      = ':'

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
        if k == N - 1 and tempStream.length() > 0:
            # We should verify if this last conditional is ever reached twice.
            streamArray.append(tempStream)
    return streamArray


#############
#############
##         ##
## CLASSES ##
##         ##
#############
#############
# class OneiASTNode:
    # This class implements a node in the Abstract Syntax Tree (AST).

    ##############
    # ATTRIBUTES #
    ##############

    ###########
    # CREATOR #
    ###########
#     def __init__(self):
#         pass

    #######################
    # GETTERS AND SETTERS #
    #######################

    ###########
    # METHODS #
    ###########





class OneiAST:
    # This class implements a whatever

    ##############
    # ATTRIBUTES #
    ##############

    ###########
    # CREATOR #
    ###########
    def __init__(self):
        pass

    #######################
    # GETTERS AND SETTERS #
    #######################

    ###########
    # METHODS #
    ###########



class OneiParser:
    # This class implements a whatever

    ##############
    # ATTRIBUTES #
    ##############
    # _imports = []


    ###########
    # CREATOR #
    ###########
    def __init__(self):
        pass

    #######################
    # GETTERS AND SETTERS #
    #######################
    # def setImports(self,imports):
    #     self._imports = imports

    # def getImports(self):
    #     return self._imports

    ###########
    # METHODS #
    ###########
