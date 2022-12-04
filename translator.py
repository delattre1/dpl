TRANSLATOR_EBNF = {
    # Keywords
    'if'    : 'se',
    'else'  : 'casoContrario',
    'print' : 'mostra',
    'while' : 'enquanto',
    'func'  : 'receita',
    'true'  : 'verdadeVerdadeira',
    'false' : 'mentira',
    'int'   : 'inteiro',
    'float' : 'pedaco',
    'bool'  : 'simOuNao',

    # Operators (daqui pra baixo tá certo, arrumar ali pra cima ^)
    '+'   : 'com'                   ,
    '-'   : 'sem'                   ,
    '*'   : 'multiplicadoPor'       ,
    '/'   : 'divididoPor'           ,
    '>'   : 'temMaisQue'            ,
    '<'   : 'temMenosQue'           ,
    '>='  : 'temMaisOuIgualA'       ,
    '<='  : 'temMenosOuIgualA'      ,
    '=='  : 'ehIgualzinho'          ,
    '"="' : '"recebe"'              ,
    '&&'  : 'EE'                    ,
    '||'  : 'ouTalvez'              ,
}

# Antigo, mudar 
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
    '-'    : 'menas',
    '*'    : 'vezes',
    '/'    : 'dividido',
    '&&'   : 'ee',
    '||'   : 'ou',

    'print' : 'mostra',
    'while' : 'enquanto',
    'func'  : 'receita',
    'true'  : 'verdadeVerdadeira',
    'false' : 'mentira',
    'int'   : 'inteiro',
    'float' : 'pedaco',
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

if __name__ =='__main__':
    translate_ebnf()
