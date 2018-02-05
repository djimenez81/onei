#!/usr/bin/python
# module onei

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

# ################################################## 
# ##  THIS FILE SHOULD CONTAIN THE PARTS OF THE   ##  
# ## IMPLEMENTATION THAT HAVE BEEN ALREADY TESTED ## 
# ################################################## 





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


######################
######################
##                  ##
## GLOBAL VARIABLES ## 
##                  ##
######################
######################

#############
#############
##         ##
## METHODS ## 
##         ##
#############
#############
def oneiLexedXML(infile,outfile):
    # This method is just to check on the output of the lexing process. It
    # should not be considered part of the deployment.
    lexie = OneiLexer()
    lexie.tokenize(infile)

    theLines       = lexie.getLines()
    theStream      = lexie.getStream()
    tokenLine      = lexie.getTokenLine()
    lastLine       = len(theLines)
    counter        = 1
    tokenN         = 0
#    pdb.set_trace()
#   BIG ERROR:
#   What happens if there is only one line. Have to fix.
    curFirstToken  = tokenLine[counter-1][1]
    nextFirstToken = curFirstToken #[counter-1][1]

    root = ET.Element('OneiLexedOutput')
    line = ET.SubElement(root,'line',{'number':str(tokenLine[counter-1][0])})

    token = theStream.next()
    while token != None:
#    for token in theStream:
        tok = ET.SubElement(line,'token',{'value':token.getContent(),
                'type':token.getType()})
        tokenN += 1
        if tokenN >= nextFirstToken and counter < lastLine:
            line = ET.SubElement(root,'line',
                {'number':str(tokenLine[counter][0])})
            curFirstToken = nextFirstToken +1
            counter += 1
            if counter == lastLine:
                nextFirstToken += len(theLines[-1][1])
            else:
                nextFirstToken = tokenLine[counter-1][1]
        token = theStream.next()
    rough = ET.tostring(root)
    reparsed = minidom.parseString(rough)
    pretty   = reparsed.toprettyxml(indent="  ")
    root     = ET.fromstring(pretty)
    tree = ET.ElementTree(root)
    tree.write(outfile)

    return lexie


#############
#############
##         ##
## CLASSES ## 
##         ##
#############
#############



######################
######################
##                  ##
## GLOBAL VARIABLES ## 
##                  ##
######################
######################



