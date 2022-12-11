## Objetivos
1. Criar uma Linguagem de Programação.
2. A linguagem deve ter todas as estruturas básicas de uma linguagem de programação: variáveis, condicionais, loops e funções.

## Tarefas:
- Atividade Prática Supervisionada (estimativa de esforço de 20h).
1. Estruturar a linguagem segundo o padrão EBNF.
2. Utilizar as ferramentas Flex e Bison (ou semelhantes) para realizar as etapas de Análise Léxica e Sintática.
3. Utilizar a LLVM (ou semelhantes - incluindo o próprio compilador) para implementar a sua linguagem até a fase final de compilação. Não é preciso implementar um compilador novo.
4. Criar um exemplo de testes que demonstre as características da sua Linguagem.
5. Fazer uma apresentação com slides apresentando sua linguagem (Motivação, Características, Curiosidades e Exemplos).


# EBNF
- (tipos básicos: variáveis, condicionais, loops e funções)

```python 
PROGRAM     = { DECLARATION } ;
DECLARATION = "receita", IDENTIFIER, "(", { PARAM, { "," , PARAM } } ")", { "->", TYPE }, BLOCK;
BLOCK       = "{", {STATEMENT}, "}" ;

# Statement
STATEMENT   = ( λ | RETURN | PRINT | WHILE | IF | BLOCK | VAR_DEC | VAR_ASSIGN | FUNC_CALL ), ";" ;
RETURN = "resultado", STATEMENT ; 
PRINT      = "mostra", "(", OREXPR, ")" ;
WHILE      = "enquanto", "(", OREXPR, ")", STATEMENT ;
IF = "se", "(", OREXPR, ")", STATEMENT { "casoContrario", STATEMENT } ;
VAR_DEC = "ingrediente", IDENTIFIER, { "," IDENTIFIER } ":", TYPE { "recebe", OREXPR, { ",", OREXPR } } 
VAR_ASSIGN = IDENTIFIER, "recebe", OREXPR
FUNC_CALL = IDENTIFIER, "(", { OREXPR, "," }, ")"

# Factor
OREXPR  = ANDEXPR, {"ouTalvez",     ANDEXPR} ;
ANDEXPR = EQEXPR,  {"EE",           EQEXPR} ;
EQEXPR  = RELEXPR, {"ehIgualzinho", RELEXPR} ;
RELEXPR = EXPR,    {("temMaisQue" | "temMenosQue"), EXPR} ;
EXPR    = TERM,    {("com" | "sem"), TERM} ;
TERM    = FACTOR,  {("multiplicadoPor" | "divididoPor"), FACTOR} ;
FACTOR  = STRING_VALUE |
          NUMBER |
          "com" | "sem" | "!", FACTOR | 
          "(", OREXPR, ")" | 
          "entrada", "(", ")" |
          IDENTIFIER { "(", { OREXPR, { "," , OREXPR }, ")" } 

# Base values
NUMBER       = DIGIT, {DIGIT} ;
IDENTIFIER   = LETTER, {LETTER | DIGIT | "_"} ;
STRING_VALUE = '"', (LETTER | DIGIT), {(LETTER | DIGIT)}, '"' ;
PARAM        = TYPE, ":", IDENTIFIER ;
TYPE         = "inteiro" | "texto" ;
LETTER = (a | ... | z | A | ... | Z) ;
DIGIT  = (1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;
```


### Valid "fruit" or related words:

```python
FRUITS = {
    'abacate',      'abacaxi',    'abiu',       'abricó',         'abrunho',     'acai',      'acerola',      'akee',        'alfarroba',      'ameixa',      'amendoa',
    'amora',        'ananás',     'anona',      'araca',          'arando',      'araticum',  'ata',          'atemoia',     'avela',          'babaco',      'babacu',
    'bacaba',       'bacuri',     'bacupari',   'banana',         'baru',        'bergamota', 'biriba',       'buriti',      'butia',          'cabeludinha', 'cacau',
    'cagaita',      'caimito',    'caja',       'caju',           'calabaça',    'calabura',  'calamondin',   'cambuca',     'cambuci',        'camuCamu',    'caqui',
    'carambola',    'carnauba',   'castanha',   'castanhaDoPara', 'cereja',      'ciriguela', 'ciruela',      'coco',        'cranberry',      'cupuacu',
    'damasco',      'dekopon',    'dende',      'diospiro',       'dovyalis',    'duriao',    'embauba',      'embaubarana', 'engkala',        'escropari',
    'esfregadinha', 'figo',       'framboesa',  'frutaDoConde',   'frutaPao',    'feijoa',    'frutaDeCedro', 'frutaDeLobo', 'frutaDoMilagre', 'frutaDeTatu',
    'gabiroba',     'glicosmis',  'goiaba',     'granadilla',     'gravata',     'graviola',  'groselha',     'grumixama',   'guabiju',        'guabiroba',
    'guaraná',      'hawthorn',   'heisteria',  'hilocéreo',      'ibacurupari', 'ilama',     'imbe',         'imbu',        'inaja',          'inga',
    'inhare',       'jabuticaba', 'jaca',       'jambo',          'jambolao',    'jamelao',   'jaracatia',    'jatoba',      'jenipapo',       'jeriva',
    'jua',          'jujuba',     'kiwi',       'kumquat',        'kinkan',      'kino',      'kiwano',       'kabosu',      'karite',         'laranja',
    'limao',        'lima',       'lichia',     'longan',         'lucuma',      'lacucha',   'lulo',         'lobeira',     'langsat',        'laranjaDePacu',
    'mabolo',       'maca',       'macadamia',  'macauba',        'mamao',       'mamey',     'mamoncillo',   'manaCubiu',   'manga',          'mangaba',
    'mangostao',    'maracuja',   'marang',     'marmelo',        'marolo',      'marula',    'massala',      'melancia',    'melao',          'meloa',
    'mexerica',     'mirtilo',    'morango',    'murici',         'naranjilla',  'nectarina', 'nespera',      'noni',        'noz',            'nozPeca',
    'nozMacadamia', 'oiti',       'oxicoco',    'orangelo',       'pera',        'pessego',   'pitanga',      'pinha',       'pitaia',         'pitomba',
    'pitangatuba',  'pindaiba',   'pequi',      'pequia',         'physalis',    'pulasan',   'pomelo',       'pupunha',     'puca',           'pataua',
    'pajura',       'pixirica',   'pistache',   'quina',          'quiuí',       'roma',      'rambai',       'rambutao',    'rukam',          'saguaraji',
    'salak',        'santol',     'sapota',     'sapoti',         'sapucaia',    'saputa',    'seriguela',    'sorvinha',    'tangerina',      'tamarindo',
    'tamara',       'toranja',    'tucuma',     'taiuva',         'tapia',       'taruma',    'tangor',       'tucuja',      'uva',            'umbu',
    'uvaia',        'uchuva',     'ume',        'uxi',            'vacínio',     'veludo',    'vergamota',    'wampi',       'xixa',           'yamamomo',
    'yuzu',         'zimbro' 
    }

MIX = { 'leite', 'acucar', 'sal', 'agua', 'manteiga', 'leiteCondensado' }

FUNCTIONS = { 'Main', 'mistura', 'tempera', 'junta' }
```

Code example:
```python

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


# Idea:

To create a program in this language, all variables must be represented by fruit names (in portuguese) or by some cooking ingredients. If you use more than 5 variables that doenst follow this rule, your program will crash.

Example of allowed 