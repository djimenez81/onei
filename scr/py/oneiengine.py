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
# Sep. 6, 2017: There might be a problem when the thing is reading strings. It
#               could be important to fix it some time soon.
#
#



###############
###############
##           ##
##  IMPORTS  ##
##           ##
###############
###############

import xml.etree.ElementTree as ET
from xml.dom import minidom
import pdb #; pdb.set_trace()
from oneilexer import *
from oneiparser import *


#############
#############
##         ##
## METHODS ##
##         ##
#############
#############




def splitStream(stream):
    # This funtion is made to test splitting of the file.
    stream.toBeginning()
    N              = stream.length()
    k              = 0
    lexParts       = []
    level          = 0
    locstrm        = OneiStream()
    startSubstream = True # This boolean specified if a stream is starting
    expectEnd      = False
    declareOpen    = False
    while k < N:
        tok = stream.next()
        cnt = tok.getContent()
        locstrm.add(tok)
        if cnt in DEFINERS:
            level += 1
            if startSubstream:
                expectEnd      = True
                startSubstream = False
        elif cnt == END_SING:
            level -= 1
            if level == 0:
                lexParts.append(locstrm)
                locstrm = OneiStream()
                startSubstream = True
            if declareOpen:
                declareOpen = False
        elif cnt in SCOPERS:
            level += 1
        elif cnt in DECLARERS:
            if not declareOpen:
                declareOpen = True
                level += 1
        else:
            if startSubstream:
                expectEnd      = False
                startSubstream = False
            if cnt == SEMI_COLON:
                if not expectEnd:
                    lexParts.append(locstrm)
                    locstrm        = OneiStream()
                    startSubstream = True
        k += 1
    return lexParts
