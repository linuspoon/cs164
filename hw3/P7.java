/* HW3, Problem 7. */
/* -*-Java*- */

/* Use javac to compile this file.  The command
 *   java P7
 * will then read lines from the standard input (one boolean
 * expression per line) and print out whether each is true. 
 * The command
 *   java P7 FILE
 * does the same, but takes input from FILE. */

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.util.function.Function;
import java.util.HashMap;
import java.util.Map;
import java.lang.RuntimeException;

public class P7 {

    /** Current input string. */
    private String theInput;

    /** Current position in theInput. */
    private int posn;

        
    /** Return the syntactic category of the next token. Following yacc
     *  conventions, these are simply integers, and, since there are only
     *  single-character tokens in this problem, the syntactic categories 
     *  are just the characters themselves (e.g., '(' is the category for 
     *  left parenthesis). End of file is 0 (the ASCII NUL character).
     */
    char next() {
        while (posn < theInput.length()
               && Character.isWhitespace(theInput.charAt(posn))) {
            posn += 1;
        }
        if (posn >= theInput.length()) {
            return '\0';
        } else {
            return theInput.charAt(posn);
        }
    }

    /** Report an error for the current string, raising an exception. */
    void ERROR() {
        throw new IllegalArgumentException("unexpected token");
    }

    /** If the next token is C, scan past it to the following token of
     *  the input.  Otherwise, flag an error. */
    void scan(char c) {
        if (c == next()) {
            posn += 1;
        } else {
            ERROR ();
        }
    }

    //// OTHER DECLARATIONS HERE AS NEEDED.
    //private enum Token {
    //    TRUE('1'), 
    //    FALSE('0'), 
    //    LEFT_PARENTHESE('('), 
    //    RIGHT_PARENTHESE(')'),
    //    OR('+'),
    //    AND('*'),
    //    NOT('-'), 
    //};
    
    Map<String, String> grammar = new HashMap<String, String>();

    public P7() {
        grammar.put("(0)", "0");
        grammar.put("(1)", "1");
        grammar.put("-1", "0");
        grammar.put("-0", "1");
        grammar.put("1*1", "1");
        grammar.put("1*0", "0");
        grammar.put("0*1", "0");
        grammar.put("0*0", "0");
        grammar.put("1+1", "1");
        grammar.put("1+0", "1");
        grammar.put("0+1", "1");
        grammar.put("0+0", "0");
    }

    public String fuck_once(String input) {
        var iter = grammar.entrySet().iterator();
        while(iter.hasNext()) {
            var pair = (Map.Entry<String, String>)iter.next();
            var pattern = pair.getKey();
            var value = pair.getValue();
            var fuckedInput = input;
            do {
                input = fuckedInput;
                fuckedInput = input.replace(pattern, value);
            } while(fuckedInput != input);
            input = fuckedInput;
        }
        return input;
    }

    /** The top-level routine.  Returns true or false depending on whether
     *  the boolean sentence in the input is true or false.  */
    Boolean sentence ()
    {
        // REPLACE WITH SOLUTION
        var currentInput = theInput.trim();
        var previousInput = currentInput;
        do {
            previousInput = currentInput;
            currentInput = fuck_once(currentInput);
        } while(currentInput != previousInput);
        // If the grammar is ok, final string should be either '1' or '0'.
        if(currentInput.equals("1"))
            return true;
        else if(currentInput.equals("0"))
            return false;
        else {
            throw new RuntimeException("The final deducted string is incorrect: " + currentInput);
        }
    }

    // ADD ADDITIONAL FUNCTIONS AS NEEDED (declare them above).

    public static void main(String... fileArgs) {
        new P7().process(fileArgs);
    }

    private void process(String[] fileArgs) {
        Scanner inp;

        if (fileArgs.length > 0) {
            try {
                inp = new Scanner(new File(fileArgs[0]));
            } catch (FileNotFoundException excp) {
                inp = null;
                System.err.printf("Could not open %s.%n", fileArgs[0]);
                System.exit(1);
            }
        } else {
            inp = new Scanner(System.in);
        }

        while (inp.hasNextLine()) {
            try {
                theInput = inp.nextLine();
                posn = 0;
                System.out.printf("\"%s\" is ", theInput);
                System.out.printf("%s.%n", sentence());
	    } catch (IllegalArgumentException excp) {
                System.out.println("badly formed.");
            }
        }
    }
}
