TRANSLATOR_EBNF = {
    'if'   : 'seForVerdade',
    'else' : 'casoContrario',
    '>='   : 'maiorIgual',
    '<='   : 'menorIgual',
    '>'    : 'ehMaisMaiorDeGrande',
    '<'    : 'ehMaisPiquitiquinho',
    '=='   : 'ehIgualzinho',
    '"="'  : '"recebe"',
    '+'    : 'soma',
    '-'    : 'menos',
    '*'    : 'vezes',
    '/'    : 'dividido',
    '&&'   : 'ee',
    '||'   : 'ou',
    '";"'  : '"cambioDesligo"',

    'print' : 'mostra',
    'while' : 'enquanto',
    'func'  : 'receita',
    'true'  : 'verdadeVerdadeira',
    'false' : 'mentira',
    'int'   : 'inteiro',
    'float' : 'pedaco',
    'bool'  : 'simOuNao',
    'return': 'devolve'
}


TRANSLATOR_CODE = {
    'if'   : 'seForVerdade',
    'else' : 'casoContrario',
    '>='   : 'maiorIgual',
    '<='   : 'menorIgual',
    '>'    : 'ehMaisMaiorDeGrande',
    '<'    : 'ehMaisPiquitiquinho',
    '=='   : 'ehIgualzinho',
    '='    : 'recebe',
    '+'    : 'soma',
    '-'    : 'menos',
    '*'    : 'vezes',
    '/'    : 'dividido',
    '&&'   : 'ee',
    '||'   : 'ou',
    ';'    : 'cambioDesligo',

    'print' : 'mostra',
    'while' : 'enquanto',
    'func'  : 'receita',
    'true'  : 'verdadeVerdadeira',
    'false' : 'mentira',
    'int'   : 'inteiro',
    'float' : 'quebrado',
    'bool'  : 'simOuNao'
}

def translate(text, conversion_dict, before=None):
    """
    Translate words from a text using a conversion dictionary

    Arguments:
        text: the text to be translated
        conversion_dict: the conversion dictionary
        before: a function to transform the input
        (by default it will to a lowercase)
    """
    # if empty:
    if not text: return text
    # preliminary transformation:
    before = before or str
    t = before(text)
    for key, value in conversion_dict.items():
        t = t.replace(key, value)
    return t

def example1():
    code1 = '''
    # Func 1

    a = 'hello world';
    if a == '123' {
        print('Acertou');
    }
    else {
        print('Errou') ;
    }

    contador = 0;
    while (true):
        contador = contador + 1;
    print(contador);
    '''

    print(f'Original Code:\n{code1}\n------------\nTranslated code:\n')
    print(translate(code1, TRANSLATOR_CODE))

def translate_ebnf():
    with open('base_ebnf.md', 'r') as f:
        lines = f.readlines()

    text = ''.join(lines)

    text = translate(text, TRANSLATOR_EBNF)
    with open('dpl_ebnf.md', 'w') as f:
        f.writelines(text)

def manual_t():
    text = '''
"/*"		{ comment(); }
"if"		{ count(); returntoken(IF); }
"else"		{ count(); returntoken(ELSE); }
"||"		{ count(); returntoken(BOOL_OR_OP); }
"<="		{ count(); returntoken(LE_OP); }
">="		{ count(); returntoken(GE_OP); }
"=="		{ count(); returntoken(EQ_OP); }
"="			{ count(); returntoken(ASSIGN); }
"-"			{ count(); returntoken(MINUS); }
"+"			{ count(); returntoken(PLUS); }
"*"			{ count(); returntoken(STAR); }
"/"			{ count(); returntoken(SLASH); }
"<"			{ count(); returntoken(LT_OP); }
">"			{ count(); returntoken(GT_OP); }
"&&"		{ count(); returntoken(AND_OP); }
"!"			{ count(); returntoken(BANG); }

"{"     	{ count(); returntoken(LBRACE); }
"}"     	{ count(); returntoken(RBRACE); }
"("			{ count(); returntoken(LPAREN); }
")"			{ count(); returntoken(RPAREN); }
"["      	{ count(); returntoken(LBRACKET); }
"]"      	{ count(); returntoken(RBRACKET); }
","			{ count(); returntoken(COMMA); }
":"			{ count(); returntoken(COLON); }

"int"		{ count(); returntoken(INT); }
"return"	{ count(); returntoken(RETURN); }
"while"	{ count(); returntoken(WHILE); }
"print"	{ count(); returntoken(PRINT); }
"func"	{ count(); returntoken(FUNC); }
"float"	{ count(); returntoken(FLOAT); }
"int"	{ count(); returntoken(INT); }
"bool"	{ count(); returntoken(BOOL); }
"false"	{ count(); returntoken(FALSE); }
"true"	{ count(); returntoken(TRUE); }
";"	    { count(); returntoken(SEMICOLON); }
    '''
    text = translate(text, TRANSLATOR_EBNF)
    print('\n----------\n', text, '\n\n')


if __name__ =='__main__':
    translate_ebnf()
