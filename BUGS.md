# REPORTED BUGS

## GENERAL

No general bugs reported

## SPECIFIC

### LEXER

#### BUG 1

Some times when a statement of the form

    int x <- 0;

the lexer adds a token of the type "number" with empty content at the end, right
after the semicolon.

### PARSER

NO BUGS YET
