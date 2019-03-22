/* Lexer for problem 6.  Compile with flex. */

%option noyywrap

%%

[ \t\n\r]   { }
[-10+*()]   { return yytext[0]; }
.           { cerr << "Bad character: '" << yytext << "'" << endl; }

%%
