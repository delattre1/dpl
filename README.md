# EBNF
- (tipos básicos: variáveis, condicionais, loops e funções)

```python 
BLOCK     = "{", {STATEMENT}, "}";
STATEMENT = (λ | VARIABLE_DECLARATION | ASSIGNMENT | PRINT | IF | WHILE | BLOCK | FUNCCAL | FUNCDEF), "cambioDesligo";

FUNCDEF   = PARAM, "(", {PARAM ","}, ")", BLOCK;
FUNCCALL  = IDENTIFIER, "(", {OREXPR ","}, ")";
PARAM     = TYPE, IDENTIFIER;


VARIABLE_DECLARATION = (TYPE, IDENTIFIER, "recebe", EXPR) |
                       (TYPE, IDENTIFIER );

ASSIGNMENT = IDENTIFIER, "recebe", EXPR ;
PRINT      = "mostra", "(", EXPR, ")" ;
WHILE      = "enquanto", "(", OREXPR, ")", STATEMENT;

IF = "seForVerdade", "(", OREXPR, ")", STATEMENT |
     "seForVerdade", "(", OREXPR, ")", STATEMENT, "casoContrario", STATEMENT;

OREXPR  = ANDEXPR, {"ou",        ANDEXPR};
ANDEXPR = EQEXPR,  {"ee",        EQEXPR};
EQEXPR  = RELEXPR, {"ehIgualzinho",        RELEXPR};
RELEXPR = EXPR,    {("ehMaisMaiorDeGrande" | "ehMaisPiquitiquinho"), EXPR};
EXPR    = TERM,    {("soma" | "menas"), TERM};
TERM    = FACTOR,  {("vezes" | "dividido"), FACTOR};
FACTOR  = (("soma" | "menas"), FACTOR) | NUMBER | BOOL_VALUE | STRING_VALUE | "(", EXPR, ")" | IDENTIFIER;

IDENTIFIER   = LETTER, {LETTER | DIGIT | "_"};
NUMBER       = DIGIT, {DIGIT};

STRING_VALUE = '"', (LETTER | NUMBER), {(LETTER | NUMBER)}, '"';
BOOL_VALUE   = "verdadeVerdadeira" | "mentira";
TYPE         = "inteiro" | "simOuNao" | "string";

LETTER = (a | ... | z | A | ... | Z) ;
DIGIT  = (1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 );
```

Code example:
```text

    # Func 1

    a recebe 'hello world' cambioDesligo
    seForVerdade (a ehIgualzinho '123') {
        mostra('Acertou') cambioDesligo
    }
    casoContrario {
        mostra('Errou') cambioDesligo
    }

    contador recebe 0 cambioDesligo
    enquanto (verdadeVerdadeira):
        contador recebe contador soma 1cambioDesligo
    mostra(contador) cambioDesligo
    
```
