from onei import *

lexi = oneiLexedXML("try.onei","trylex.xml")
amy = lexi.getStream()
parseval = oneyParsedXML(lexi,"tryparsed.xml")
