/* This is a Bison file that will allow you to test your solution to
 * problem 6.  */

/* Use 'make' with the Makefile in this directory to convert this
 * file to C++ and then compile it to produce executable file 6.  The command
 *   ./6
 * will then read lines from the standard input (one boolean
 * expression per line) and print out whether it is true. 
 * The command
 *   ./6 < FILE
 * does the same, but takes input from FILE. */

/* Operator precedence and associativity, listed from lowest to highest. 
 * These declarations will resolve conflicts such as ``if we've 
 * recognized e*e in the input and the next symbol is "+", should we
 * assume that (1) e*e came from the production e->e*e, or should we 
 * assume that (2) the second 'e' is going to be part of a later e+e?'' 
 * If * has higher precedence that + (is listed after + in the declarations 
 * below), then the answer is (1), and otherwise (2).  For a situation
 * of equal precendence, such as seeing e+e when the next symbol is +, 
 * we can choose to group the initial e+e together---indicated by %left---
 * or group as if the input were e+(e+e)---indicated by %right. */

%left '+'
%left '*'
%left '-'

%{
    #include <string>
    using namespace std;
    extern int yylex();
    extern int yyerror(const string);
    static int truth;
%}

%%

/* Insert rules after this comment and before the next %% below.  Yacc and 
 * its progeny use ':' to mean "produces", '|' to mean "or" (as usual), 
 * and ';' to mark the end of a rule. For example:

	s : '0' '1' | '1' s '0' ;

 * or, as it is usually laid out:

	s : '0' '1' 
          | '1' s '0' 
          ;

 * The first non-terminal symbol listed to the left of a ':' is the start
 * symbol. 
 */

expr : true   { truth = 1; }
     | false  { truth = 0; }
     ;

/* REPLACE THE RULES BELOW WITH YOUR SOLUTION (ONE OR MORE RULES) */

true : '1'
     | '(' true ')'
     | '-' false
     | true '*' true
     | true '+' any
     | false '+' true
     ;

false: '0'
     | '(' false ')'
     | '-' true
     | false '*' any
     | true '*' false
     | false '+' false
     ;

any : true | false ;

%%

#include <cctype>
#include <iostream>
#include <string>

using namespace std;

#include "6-lexer.cc"

/* The following program reads boolean expressions written one per line
 * on the standard input, and then reprints them, indicating which are
 * accepted by the grammar above. */
int
main ()
{
    /* yydebug = 1; */ // Uncomment to see parser actions.
    while (true) {
	string input;
	getline (cin, input);
	if (cin.eof ())
	    return 0;
	if (input.find_last_not_of (' ') == input.npos)
	    continue;
	yy_scan_string(input.c_str());
	yyparse();
        if (truth)
	    cout << "\"" << input <<  "\" is true." << endl;
	else
	    cout << "\"" << input << "\" is false." << endl;
    }
}

int
yyerror (const string msg) {
    cerr << msg << endl;
    return 0;
}
