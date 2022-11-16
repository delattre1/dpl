D			[0-9]
L			[a-zA-Z_]
H			[a-fA-F0-9]
E			[Ee][+-]?{D}+
FS			(f|F|l|L)
IS			(u|U|l|L)*


%{

/* this scanner sourced from: http://www.lysator.liu.se/c/ANSI-C-grammar-l.html */
/* this scanner sourced from: https://github.com/smvv/pybison/blob/master/examples/C/c.l */

void count();
int yylineno = 0;
#include <stdio.h>
#include <string.h>
#include "Python.h"
#define YYSTYPE void *
#include "tokens.h"
extern void *py_parser;
extern void (*py_input)(PyObject *parser, char *buf, int *result, int max_size);
#define returntoken(tok) /*printf("%d=%s\n", tok, yytext);*/ yylval = PyString_FromString(strdup(yytext)); return (tok);
#define YY_INPUT(buf,result,max_size) { (*py_input)(py_parser, buf, &result, max_size); }

%}


%%

"/*"                    { comment(); }
"seForVerdade"          { count(); returntoken(IF); }
"casoContrario"         { count(); returntoken(ELSE); }
"ou"                    { count(); returntoken(BOOL_OR_OP); }
"menorIgual"            { count(); returntoken(LE_OP); }
"maiorIgual"            { count(); returntoken(GE_OP); }
"ehIgualzinho"          { count(); returntoken(EQ_OP); }
"recebe"                { count(); returntoken(ASSIGN); }
"menos"                 { count(); returntoken(MINUS); }
"soma"                  { count(); returntoken(PLUS); }
"vezes"                 { count(); returntoken(STAR); }
"dividido"              { count(); returntoken(SLASH); }
"ehMaisPiquitiquinho"   { count(); returntoken(LT_OP); }
"ehMaisMaiorDeGrande"   { count(); returntoken(GT_OP); }
"ee"                    { count(); returntoken(AND_OP); }
"!"                     { count(); returntoken(BANG); }

"{"                     { count(); returntoken(LBRACE); }
"}"                     { count(); returntoken(RBRACE); }
"("                     { count(); returntoken(LPAREN); }
")"                     { count(); returntoken(RPAREN); }
"["                     { count(); returntoken(LBRACKET); }
"]"                     { count(); returntoken(RBRACKET); }
","                     { count(); returntoken(COMMA); }
":"                     { count(); returntoken(COLON); }

"inteiro"               { count(); returntoken(INT); }
"devolve"               { count(); returntoken(RETURN); }
"enquanto"              { count(); returntoken(WHILE); }
"mostra"                { count(); returntoken(PRINT); }
"receita"               { count(); returntoken(FUNC); }
"pedaco"                { count(); returntoken(FLOAT); }
"inteiro"               { count(); returntoken(INT); }
"simOuNao"              { count(); returntoken(BOOL); }
"mentira"               { count(); returntoken(FALSE); }
"verdadeVerdadeira"     { count(); returntoken(TRUE); }
"cambioDesligo"         { count(); returntoken(SEMICOLON); }


[ \t\v\n\f]		{ count(); }
.   			{ /* ignore bad characters */ }

%%

yywrap()
{
	return(1);
}


comment()
{
	char c, c1;

loop:
	while ((c = input()) != '*' && c != 0)
      /*putchar(c)*/;

	if ((c1 = input()) != '/' && c != 0)
	{
		unput(c1);
		goto loop;
	}

	if (c != 0)
      /*putchar(c1)*/;
}


int column = 0;

void count()
{
	int i;

	for (i = 0; yytext[i] != '\0'; i++)
		if (yytext[i] == '\n')
			column = 0;
		else if (yytext[i] == '\t')
			column += 8 - (column % 8);
		else
			column++;

	/*ECHO*/;
}


int check_type()
{
/*
* pseudo code --- this is what it should check
*
*	if (yytext == type_name)
*		return(TYPE_NAME);
*
*	return(IDENTIFIER);
*/

/*
*	it actually will only return IDENTIFIER
*/

	return(IDENTIFIER);
}

