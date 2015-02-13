/* HW3, Problem 7. */
/* -*-C++-*- */

/* Use 'make' with the Makefile in this directory to compile
 * this file with g++ to produce class executable file 7.  The command
 *   ./7
 * will then read lines from the standard input (one boolean
 * expression per line) and print out whether it is true. 
 * The command
 *   ./7 FILE
 * does the same, but takes input from FILE. */

#include <cstdlib>
#include <cctype>
#include <cstdio>
#include <iostream>
#include <string>
#include <stdexcept>

using namespace std;

/** Current input string. */
static string theInput;

/** Current position in theInput. */
static unsigned int posn;

/* Lexical Analyzer Functions. */

extern int next();
extern void ERROR () __attribute__ ((__noreturn__));
extern void scan (int);

/** Return the syntactic category of the next token. Following yacc
 *  conventions, these are simply integers, and, since there are only
 *  single-character tokens in this problem, the syntactic categories 
 *  are just the characters themselves (e.g., '(' is the category for 
 *  left parenthesis). End of file is 0.
 */
int next () {
    while (posn < theInput.size () && isspace(theInput[posn])) {
        posn += 1;
    }
    if (posn >= theInput.size ()) {
        return 0;
    } else {
        return theInput[posn];
    }
}

/** Report an error for the current string, raising an exception. */
void ERROR () {
    throw invalid_argument ("unexpected token");
}

/** If the next token is C, scan past it to the following token of
 *  the input.  Otherwise, flag an error. */
void scan(int c) {
    if (c == next ()) {
        posn += 1;
    } else {
        ERROR ();
    }
}

/* C++ hint: C++ requires functions to be declared before being used.
 * To allow for mutual recursion, it is necessary to declare some
 * functions before providing their bodies.  Indeed, it doesn't hurt
 * to do this with all the functions you define, as in the
 * declaration of sentence below (in C++ terminology, a function
 * header without a body is a "declaration" (sometimes called a "forward
 * declaration"), and with a body is a "definition". */

bool sentence ();
// OTHER DECLARATIONS HERE AS NEEDED.

/** The top-level routine.  Returns true or false depending on whether
 *  the boolean sentence in the input is true or false.  */
bool sentence ()
{
    // REPLACE WITH SOLUTION
    return true;
}

// ADD ADDITIONAL FUNCTIONS AS NEEDED (declare them above).

int
main (int argc, char* argv[]) {
    if (argc > 1) {
        if (freopen(argv[1], "r", stdin) == NULL) {
            cerr << "Could not open " << argv[1] << endl;
            exit (1);
        }
    }

    while (true) {
        try {
            getline (cin, theInput);
            posn = 0;
            if (cin.eof ()) {
                return 0;
            }
            cout << "\"" << theInput << "\" is";
            if (sentence ()) {
		cout << "true." << endl;
	    } else {
		cout << "false." << endl;
	    }
        } catch (const invalid_argument& excp) {
            cout << "badly formed." << endl;
        }
    }
}
