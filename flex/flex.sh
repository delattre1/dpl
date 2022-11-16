flex lexical.l &&
wc lex.yy.c &&
gcc lex.yy.c -o lex_out &&
rm lex.yy.c


