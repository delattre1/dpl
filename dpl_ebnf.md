# EBNF
sem (tipos básicos: variáveis, condicionais, loops e funções)

```python 
BLOCK     = "{", {STATEMENT}, "}";
STATEMENT = (λ | VARIABLE_DECLARATION | ASSIGNMENT | PRINT | IF | WHILE | BLOCK | FUNCCAL | FUNCDEF), ";";

FUNCDEF   = PARAM, "(", {PARAM ","}, ")", BLOCK;
FUNCCALL  = IDENTIFIER, "(", {OREXPR ","}, ")";
PARAM     = TYPE, IDENTIFIER;


VARIABLE_DECLARATION = (TYPE, IDENTIFIER, "recebe", EXPR) |
                       (TYPE, IDENTIFIER );

ASSIGNMENT = IDENTIFIER, "recebe", EXPR ;
PRINT      = "mostra", "(", EXPR, ")" ;
WHILE      = "enquanto", "(", OREXPR, ")", STATEMENT;

IF = "se", "(", OREXPR, ")", STATEMENT |
     "se", "(", OREXPR, ")", STATEMENT, "casoContrario", STATEMENT;

OREXPR  = ANDEXPR, {"ouTalvez",        ANDEXPR};
ANDEXPR = EQEXPR,  {"EE",        EQEXPR};
EQEXPR  = RELEXPR, {"ehIgualzinho",        RELEXPR};
RELEXPR = EXPR,    {("temMaisQue" | "temMenosQue"), EXPR};
EXPR    = TERM,    {("com" | "sem"), TERM};
TERM    = FACTOR,  {("multiplicadoPor" | "divididoPor"), FACTOR};
FACTOR  = (("com" | "sem"), FACTOR) | NUMBER | BOOL_VALUE | STRING_VALUE | "(", EXPR, ")" | IDENTIFIER;

IDENTIFIER   = LETTER, {LETTER | DIGIT | "_"};
NUMBER       = DIGIT, {DIGIT};

STRING_VALUE = '"', (LETTER | NUMBER), {(LETTER | NUMBER)}, '"';
BOOL_VALUE   = "verdadeVerdadeira" | "mentira";
TYPE         = "inteiro" | "simOuNao" | "string";

LETTER = (a | ... | z | A | ... | Z) ;
DIGIT  = (1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 );
```

