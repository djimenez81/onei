/**
 * Copyright (c) 2017 Universidad de Costa Rica
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *    - Redistributions of source code must retain the above copyright
 *      notice, this list of conditions and the following disclaimer.
 *    - Redistributions in binary form must reproduce the above copyright
 *      notice, this list of conditions and the following disclaimer in the
 *      documentation and/or other materials provided with the distribution.
 *    - Neither the name of the <organization> nor the
 *      names of its contributors may be used to endorse or promote products
 *      derived from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL UNIVERSIDAD DE COSTA RICA BE LIABLE FOR
 * ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
 * CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
 * DAMAGE.
 */

// Principal Investigator:
//         David Jimenez <david.jimenezlopez@ucr.ac.cr>
// Assistants:
//         Cristina Soto Rojas

grammar ONEI;

/*   ********************
 *   ********************
 *   **                **
 *   **  PARSER RULES  **
 *   **                **
 *   ********************
 *   ********************
 */

file : definitionOneiFile | scriptOneiFile ;

scriptOneiFile : ( oneiStatement ( ';' | NL ) | NL )* EOF ;

definitionOneiFile : oneiImport*
                     oneiSetup?
                     ( oneiEnvironment
                       | oneiFunction
                       | oneiPatch
                       | oneiAgent
                       | oneiRule
                       | oneiMessage  // Message sent from something to s else.
                       | oneiExchange // Exchage table of messages
                       | oneiItem
                       | oneiTable // Keeps track of what is where
                     )*
                     EOF
                     ;


oneiImport : FROM ID IMPORT importList NL
             | IMPORT importList NL
             ;


oneiFunction : FUNCTION ID ':' NL
               oneiInput?
               oneiOutput?
               oneiVariables?
               ( oneiStatement NL )*
               END NL
               ;


oneiSetup : SETUP ':' NL ( oneiStatement NL )* END NL;


oneiEnvironment : ( ENVIRONMENT ID EXTENDS ID ':' NL
                    | ENVIRONMENT ID ':' NL
                  )
                  oneiAttributes?
                  ( oneiFunction )*
                  END NL
                  ;


oneiPatch : ( PATCH ID EXTENDS ID ':' NL
              | PATCH ID ':' NL
            )
            oneiAttributes?
            ( oneiFunction )*
            END NL
            ;


oneiAgent : ( AGENT ID EXTENDS ID ':' NL
              | AGENT ID ':' NL
            )
            oneiAttributes?
            ( oneiFunction )*
            END NL
            ;


oneiRule : ( RULE ID EXTENDS ID ':' NL
             | RULE ID ':' NL
           )
           oneiAttributes?
           ( oneiFunction )*
           END NL
           ;


oneiMessage : ( MESSAGE ID EXTENDS ID ':' NL
                | MESSAGE ID ':' NL
              )
              oneiAttributes?
              ( oneiFunction )*
              END NL
              ;


oneiExchange : ( EXCHANGE ID EXTENDS ID ':' NL
                 | EXCHANGE ID ':' NL
               )
               oneiAttributes?
               ( oneiFunction )*
               END NL
               ;

oneiItem : ( ITEM ID EXTENDS ID ':' NL
             | ITEM ID ':' NL
           )
           oneiAttributes?
           ( oneiFunction )*
           END NL
           ;


oneiTable: ( TABLE ID EXTENDS ':' NL
             | TABLE ID ':' NL
           )
           oneiAttributes?
           ( oneiFunction )*
           END NL
           ;



importList : ID ',' importList
             | ID ';'
             ;

oneiInput : INPUT NL argumentList END NL
            | INPUT NL argumentList oneiOutput
            | INPUT NL argumentList oneiVariables
            ;

oneiOutput : OUTPUT NL argumentList END NL
             | OUTPUT NL argumentList oneiVariables
             ;

oneiVariables : OUTPUT NL argumentList END NL ;

oneiAttribute : ATTRIBUTES NL argumentList END NL ;

argumentList : argument ';' NL argumentList
               | argument ';' NL
               ;


argument : structureType? dataType ( ID ',' )* ID NL
           | structureType? dataType ID '<-' expression NL // check carefully
           ;


oneiStatement : ( assignment
                  | expression
                  | commandForm // Not sure what it is
                  | forCommand
                  | ifCommand
                  | whileCommand
                ) // should we include a switch case statement?
                ';'
                NL
                ;


assignment : ID '=' expression


ifCommand : IF expression ':' NL oneiStatement+
            ( ELSEIF expression ':' NL oneiStatement+ )* NL?
            ( ELSE ':' NL oneiStatement+ )? NL?
            END NL
            ;


whileCommand : WHILE expression ':' NL oneiStatement+ END NL ;


forCommand : FOR ID IN expression ':' NL oneiStatement+ END NL ;


expression : reference
             | '+' expression
             | '-' expression
             | NOT expression
             | expression '+'  expression
             | expression '-'  expression
             | expression '*'  expression
             | expression '/'  expression
             | expression '^'  expression
             | expression '<'  expression
             | expression '>'  expression
             | expression '==' expression
             | expression '<=' expression
             | expression '>=' expression
             | expression '!=' expression
             | expression AND  expression
             | expression OR   expression
             | expression XOR  expression
             ;


reference : ID
            | INTVAL
            | FLOATVAL
            | TRUE
            | FALSE
            | ID '(' ')'     // Call to method without input
            | ID '(' (expression ',')* expression ')'
            | '(' expression ')'
            | ID ('.'
                  (
                   ( ID '(' (expression ',')* expression ')'
                     | ID '(' ')'
                   )
                  )
                 )+
            ;


// Should we include void?
dataType : BOOL
           | INT
           | FLOAT
           | CHAR // Can we pull a python and have only strings?
           | IO // maybe a type for displaying
           ;



// Think whether to include Container, Stack, Queue, Double-ended queue,
// Tree, Graph.
structureType : LIST
                | ARRAY
                | STRING
                ;

/*   *******************
 *   *******************
 *   **               **
 *   **  LEXER RULES  **
 *   **               **
 *   *******************
 *   *******************
 */



/*  *********************
 *  * LANGUAGE KEYWORDS *
 *  *********************
 */

AGENT       : 'agent'       ; 
AND         : 'and'         ; 
ARRAY       : 'array'       ; 
ATTRIBUTES  : 'attibutes'   ; 
BOOL        : 'boolean'     ; 
CHAR        : 'character'   ; 
DICT        : 'dictonary'   ; 
ELSE        : 'else'        ; 
END         : 'end'         ; 
ENVIRONMENT : 'environment' ;
EXCHANGE    : 'exchage'     ; 
EXTENDS     : 'extends'     ; 
FALSE       : 'false'       ; 
FLOAT       : 'float'       ; 
FOR         : 'for'         ; 
FUNCTION    : 'function'    ; 
IF          : 'if'          ; 
IMPORT      : 'import'      ; 
IN          : 'in'          ; 
INPUT       : 'input'       ; 
INT         : 'integer'     ; 
IO          : 'io'          ; 
ITEM        : 'item'        ;  
LIST        : 'list'        ; 
MESSAGE     : 'message'     ; 
NOT         : 'not'         ; 
OR          : 'or'          ; 
OUTPUT      : 'output'      ; 
PASS        : 'pass'        ; 
PATCH       : 'patch'       ; 
RULE        : 'rule'        ; 
SELF        : 'self'        ; 
STRING      : 'string'      ; 
TABLE       : 'table'       ; 
TRUE        : 'true'        ; 
VARIABLES   : 'variables'   ; 
WHILE       : 'while'       ; 
XOR         : 'xor'         ; 


/*  *****************************
 *  * OPERATORS AND ASSIGNMENTS *
 *  *****************************
 */

CONTASSIG   : '<-' ; // Conditional assignment
ASSIGNING   : '='  ;
EQUAL       : '==' ;
NOTEQUAL    : '!=' ;
LST         : '<'  ;
GRT         : '>'  ;
LSTEQ       : '<=' ;
GRTEQ       : '>=' ;
PLUS        : '+'  ;
MINUS       : '-'  ;
TIMES       : '*'  ;
DIVISION    : '/'  ;
EXPONENTIAL : '^'  ;


/*  ****************************
 *  * DELIMITERS AND EXTENDERS *
 *  ****************************
*/

SEMICOLON    : ';' ;
COLON        : ':' ;
DOT          : '.' ;
COMMA        : ',' ;
LEFTPAREN    : '(' ;
RIGHTPAREN   : ')' ;
LEFTBRACKET  : '[' ;
RIGHTBRACKET : ']' ;
LEFTBRACE    : '{' ;
RIGHTBRACE   : '}' ;
AT           : '@' ; // Might want it as a referencer

/*  **************************
 *  * COMMENTS AND CONTIUERS *
 *  **************************
 */

COMMENT   : '#'   ; // Should we make a block comment sequence?
CONTINUER : '...' ; // This is for when a command does not end in the line.


/*  *********************************************
 *  * IDENTIFIERS, STRINGS, NUMBERS, WHITESPACE *
 *  *********************************************
 */

NL : '\n' -> channel(HIDDEN);

ID       : [a-zA-Z] [a-zA-Z0-9_]*;
DIGIT    : [0-9]                 ;
EXPONENT : ('e'|'E') ('+'|'-')? DIGIT+ ;
STRING : '\'' ( ~('\\'|'\'') )* '\'' 	 ;
INTVAL   : DIGIT+                ;
FLOATVAL :  DIGIT+ '.' DIGIT* EXPONENT?
          | DIGIT+ EXPONENT
          | '.' DIGIT+ EXPONENT?
         ;
