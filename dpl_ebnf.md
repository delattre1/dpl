
# EBNF
sem (tipos básicos: variáveis, condicionais, loops e funções)

```python 
PROGRAM     = { DECLARATION } ;
DECLARATION = "fn", IDENTIFIER, "(", { PARAM, { "," , PARAM } } ")", { "semtemMaisQue", TYPE }, BLOCK;
BLOCK       = "{", {STATEMENT}, "}" ;

# Statement
STATEMENT   = ( λ | RETURN | PRINT | WHILE | IF | BLOCK | VAR_DEC | VAR_ASSIGN | FUNC_CALL ), ";" ;
RETURN = "return", STATEMENT ; 
PRINT      = "mostra", "(", OREXPR, ")" ;
WHILE      = "enquanto", "(", OREXPR, ")", STATEMENT ;
IF = "se", "(", OREXPR, ")", STATEMENT { "casoContrario", STATEMENT } ;
VAR_DEC = "var", IDENTIFIER, { "," IDENTIFIER } ":", TYPE { "recebe", OREXPR, { ",", OREXPR } } 
VAR_ASSIGN = IDENTIFIER, "recebe", OREXPR
FUNC_CALL = IDENTIFIER, "(", { OREXPR, "," }, ")"

# Factor
OREXPR  = ANDEXPR, {"ouTalvez",        ANDEXPR} ;
ANDEXPR = EQEXPR,  {"EE",        EQEXPR} ;
EQEXPR  = RELEXPR, {"ehIgualzinho",        RELEXPR} ;
RELEXPR = EXPR,    {("temMaisQue" | "temMenosQue"), EXPR} ;
EXPR    = TERM,    {("com" | "sem"), TERM} ;
TERM    = FACTOR,  {("multiplicadoPor" | "divididoPor"), FACTOR} ;
FACTOR  = STRING_VALUE |
          NUMBER |
          "com" | "sem" | "!", FACTOR | 
          "(", OREXPR, ")" | 
          "Read", "(", ")" |
          IDENTIFIER { "(", { OREXPR, { "," , OREXPR }, ")" } 

# Base values
NUMBER       = DIGIT, {DIGIT} ;
IDENTIFIER   = LETTER, {LETTER | DIGIT | "_"} ;
STRING_VALUE = '"', (LETTER | DIGIT), {(LETTER | DIGIT)}, '"' ;
PARAM        = TYPE, ":", IDENTIFIER ;
TYPE         = "inteiro" | "string" ;
LETTER = (a | ... | z | A | ... | Z) ;
DIGIT  = (1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;
```

