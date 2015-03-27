/* HW #5, Problem 1: shared definitions. */

:- multifile typeof/3.

/* To help test your solution, here are some definitions for a very simple
 * language in which there are function calls and constructors (as in 
 * "new foo"), but not much else. */

/* Type environments: defn(X,T,Env) iff X has type T in Env. */
defn(X,Y,[def(X,Y)|_]).
defn(X,Y,[def(X1,_)|Env1]) :- dif(X,X1), defn(X,Y,Env1).

/* subtype(T0,T1) iff T0 is a proper subtype of T1 (that is, T0 is a subtype
 * of T1 other than T1 itself. */
subtype(T0,T1) :- parentof(T0,T1).
subtype(T0,T1) :- parentof(T0,T2), subtype(T2, T1).

/* typeof(A,T,Env): expression A has type T in type environment Env. */

/* Integer literals */
typeof(I,int,_) :- integer(I).

/* The construct new(T) has type T. */
typeof(new(T),T,_).

/* Identifiers */
typeof(X,T,Env) :- defn(X,T,Env).

/* The function call F(E0) has type T if F has type (T0)->T and E0 
   has type T0. */
typeof(call(F,E0),T,Env) :- typeof(F,func(T0,T),Env), typeof(E0,T0,Env).

/* The function call F(E0,E1) has type T if F has type (T0,T1)->T,
 * E0 has type T0, and E1 has type T1. */
typeof(call(F,E0,E1),T,Env) :- 
   typeof(F,func(T0,T1,T),Env), typeof(E0,T0,Env), typeof(E1,T1,Env).

/* If an expression E has type T1, it also has type T0 if T1 is a subtype of
 * T0. */
typeof(E,T0,Env) :- subtype(T1,T0), typeof(E,T1,Env).

/* Here's an example of one way to test: */

parentof(square,quadrilateral).
parentof(quadrilateral,polygon).

environ1([def(side,func(square,int)),
          def(area,func(polygon,int)),
          def(boundingbox,func(polygon,quadrilateral)),
          def(+,func(int,int,int)),
          def(setwid,func(quadrilateral,int,quadrilateral)),
          def(getwid,func(quadrilateral,int)),
          def(val1,polygon)]).

expr1(case_conform(k,val1,[case(square,
                                call(setwid,k,call(+,call(side,k),2))),
                           case(polygon,call(boundingbox,k))])).

/* Now, you can test to see whether you get expected results by typing 
 * queries like:

?- expr1(E), environ1(Env), typeof(E, square, Env).   (Should fail)
?- expr1(E), environ1(Env), typeof(E, polygon, Env).  (Should succeed)

*/


