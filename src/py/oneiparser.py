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


###############
###############
##           ##
##  IMPORTS  ##
##           ##
###############
###############
import pdb #; pdb.set_trace()
from oneilexer import OneiLexer


########################
########################
########################
###                  ###
###                  ###
###      PARSER      ###
###                  ###
###                  ###
########################
########################
########################


######################
######################
##                  ##
## GLOBAL CONSTANTS ##
##                  ##
######################
######################
DEFINERS  = ['agent',   'environment',  'exchange', 'function', 'io',   
            'item',     'message',      'patch',    'rule',     'table']

SCOPERS   = ['for', 'if','while']

DECLARERS = ['attributes','input', 'output','variables'] 

KEYWORDY = ['and', 'array', 'boolean', 'character', 'dictionary', 'else', 
            'elseif', 'extends', 'false', 'float', 'import', 'in',  
            'integer', 'list', 'not', 'or', 'pass', 'self', 'string', 'true', 
            'xor']

END_SING   = 'end'
SEMI_COLON = ';'
COLON      = ':'




#############
#############
##         ##
## METHODS ##
##         ##
#############
#############
# def splitStream(stream):
#     pass


#############
#############
##         ##
## CLASSES ##
##         ##
#############
#############
class OneiASTNode:
    # This class implements a whatever

    ##############
    # ATTRIBUTES #
    ##############
    _nodeType  = ''
    _nodeValue = ''
    _children  = []

    ###########
    # CREATOR #
    ###########
    def __init__(self):
        pass

    #######################
    # GETTERS AND SETTERS #
    #######################
    def setNodeType(self,nodeType):
        self._nodeType = nodeType
    
    def getNodeType(self):
        return self._nodeType
    
    
    def setChildren(self,children):
        self._children = children
    
    
    def getChildren(self):
        return self._children
    
    def setValue(self,value):
        self._nodeValue = value
    
    def getValue(self):
        return self._nodeValue

    ###########
    # METHODS #
    ###########





class OneiAST:
    # This class implements a whatever

    ##############
    # ATTRIBUTES #
    ##############
    _root = OneiASTNode()

    ###########
    # CREATOR #
    ###########
    def __init__(self):
        pass

    #######################
    # GETTERS AND SETTERS #
    #######################
    def getRoot(self):
        return self._root
    
    def setRoot(self,root):
        self._root = root

    ###########
    # METHODS #
    ###########


'''

class OneiParser:
    # This class implements a whatever

    ##############
    # ATTRIBUTES #
    ##############
    _imports = []
    

    ###########
    # CREATOR #
    ###########
    def __init__(self):
        pass

    #######################
    # GETTERS AND SETTERS #
    #######################
    def setImports(self,imports):
        self._imports = imports
    
    def getImports(self):
        return self._imports

    ###########
    # METHODS #
    ###########
    def parse(self,stream):
        tokenTotal = len(stream)
        
        
        
        pass


'''

