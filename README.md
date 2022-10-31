# EBNF
- (tipos básicos: variáveis, condicionais, loops e funções)

```python 
BLOCK     = "{", {STATEMENT}, "}";
STATEMENT = (λ | VARIABLE_DECLARATION | ASSIGNMENT | PRINT | IF | WHILE | BLOCK | FUNCCAL | FUNCDEF), ";";

FUNCDEF   = PARAM, "(", {PARAM ","}, ")", BLOCK;
FUNCCALL  = IDENTIFIER, "(", {OREXPR ","}, ")";
PARAM     = TYPE, IDENTIFIER;


VARIABLE_DECLARATION = (TYPE, IDENTIFIER, "=", EXPR) |
                       (TYPE, IDENTIFIER );

ASSIGNMENT = IDENTIFIER, "=", EXPR ;
PRINT      = "print", "(", EXPR, ")" ;
WHILE      = "while", "(", OREXPR, ")", STATEMENT;

IF = "if", "(", OREXPR, ")", STATEMENT |
     "if", "(", OREXPR, ")", STATEMENT, "else", STATEMENT;

OREXPR  = ANDEXPR, {"||",        ANDEXPR};
ANDEXPR = EQEXPR,  {"&&",        EQEXPR};
EQEXPR  = RELEXPR, {"==",        RELEXPR};
RELEXPR = EXPR,    {(">" | "<"), EXPR};
EXPR    = TERM,    {("+" | "-"), TERM};
TERM    = FACTOR,  {("*" | "/"), FACTOR};
FACTOR  = (("+" | "-"), FACTOR) | NUMBER | BOOL_VALUE | STRING_VALUE | "(", EXPR, ")" | IDENTIFIER;

IDENTIFIER   = LETTER, {LETTER | DIGIT | "_"};
NUMBER       = DIGIT, {DIGIT};

STRING_VALUE = '"', (LETTER | NUMBER), {(LETTER | NUMBER)}, '"';
BOOL_VALUE   = "True" | "False";
TYPE         = "int" | "bool" | "string";

LETTER = (a | ... | z | A | ... | Z) ;
DIGIT  = (1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 );
```
