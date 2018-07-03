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
# DISCLAIMED. IN NO EVENT SHALL UNIVERSIDAD DE COSTA RICA, DAVID JIMENEZ, OR ANY
# OF THE AUTHORS OF THIS SOFTWARE, BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Principal Investigator:
#         David Jimenez <david.jimenezlopez@ucr.ac.cr>
# Assistants:
#         Cristina Soto Rojas

# #############################################################################
# ##  THIS FILE CONTAINS THE CONSTANTS NEEDED ON THE IMPLEMENTATION OF THE   ##
# ##  ONEI LEXER, PARSER, AST, BYTECODE COMPILER, BYTECODE INTERPRETER AND   ##
# ##  BYTECODE THAT IS BEING DEVELOPED AND TESTED.                           ##
# #############################################################################


######################
######################
##                  ##
## GLOBAL CONSTANTS ##
##                  ##
######################
######################
ELEMENTS = ['agent',  'environment', 'exchange', 'function', 'io',
            'item',   'message',     'patch',    'rule',     'setup',
            'table',  'for',         'if',       'while',    'elseif',
            'else',   'attributes',  'input',    'output',   'variables',
            'end',  ':']

CTRLELEMENTS = ['for', 'if','while']


DEFELEMENTS = ['function', 'agent',     'environment', 'attributes',
               'input',    'output',    'variables',   'array',
               'boolean',  'character', 'dictionary',  'integer',
               'list',     'float',     'string',      '=',
               '<-',       'item',      'message',     'patch',
               'rule',     'setup',     'table',       'io',
               'exchange']

###############
# STATE FLAGS #
###############
COMMENT_READ   = 'COMMENT'   #
SPACE_READ     = 'SPACE'     #
STRING_READ    = 'STRING'    #
DOT_READ       = 'DOT'       #
DELIMITER_READ = 'DELIMITER' #


######################
# SPECIAL CHARACTERS #
######################
OPERATORS        = ['<-', '=', '==', '!=', '<', '>', '<=', '>=']
DELIMITERS       = ':.,([{}])@'
END_LINE_SYMBOL  = ';'
CONTINUER_SYMBOL = '...'
COMMENT_SYMBOL   = '#'
STRING_SYMBOL    = '\"'
DOT_SYMBOL       = '.'
BIN_OPERATORS    = '+-*/^'
COMPARATOR_SYMBS = '<>-=!'
SPACE_SYMBOL     = ' '
TAB_SYMBOL       = '\t'
EXPONENT_SYMBOL  = 'e'
UNDERSCORE       = '_'
LPAREN_SYMBOL    = '('
RPAREN_SYMBOL    = ')'



#########
# TYPES #
#########
OPERATOR  = 'OPERATOR'
DELIMITER = 'DELIMITER'
UNKNOWN   = 'UNKNOWN'
KEYWORD   = 'KEYWORD'
NAME      = 'NAME'
NUMBER    = 'NUMBER'
END_LINE  = 'END_LINE'



FLOAT     = 'FLOAT'
INTEGER   = 'INTEGER'




######################
# TOKEN DICTIONARIES #
######################

KEYWORDS = ['agent',        'and',          'array',        'attributes',
            'boolean',      'character',    'dictionary',   'else',
            'elseif',       'end',          'environment',  'exchange',
            'extends',      'false',        'float',        'for',
            'function',     'if',           'import',       'in',
            'input',        'integer',      'io',           'item',
            'list',         'message',      'not',          'or',
            'output',       'pass',         'patch',        'rule',
            'self',         'setup',         'string',      'table',
            'true',         'variables',    'while',        'xor']

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
BOOLEANS = ['true','false']



##############
# NODE TYPES #
##############
EMPTY_NODE          = 'EMPTY'
FULL_IMPORT_NODE    = 'FULL_IMPORT'
ID_NODE             = 'ID'
PARTIAL_IMPORT_NODE = 'PARTIAL_IMPORT'
ROOT_NODE           = 'ROOT'
FLOAT_NODE          = 'FLOAT'
INT_NODE            = 'INT'
BOOL_NODE           = 'BOOL'
ASSIGNMENT_NODE     = 'ASSIGNMENT'



NODE_TYPES = [ASSIGNMENT_NODE,
              BOOL_NODE,
              EMPTY_NODE,
              FLOAT_NODE,
              FULL_IMPORT_NODE,
              ID_NODE,
              INT_NODE,
              PARTIAL_IMPORT_NODE,
              ROOT_NODE]

############################
# SYMBOLS TO COPY ON LEXER #
############################
ASSIGNMENT_SYMBOL = '='
TRUE_SYMBOL = 'true'
FALSE_SYMBOL = 'false'
