%Successor Function
% takes in two types of input: (3,OUTPUT) (a number, a output variable)
% or (OUTPUT,3)(a number, a output variable)
% (3,OUTPUT) will return "OUTPUT = 4" because it finds the successor
% (OUTPUT,3) will return "OUTPUT = 2" because it find previous
successor(INPUT,SUCCESSOR):-
    var(INPUT) -> INPUT is SUCCESSOR -1; SUCCESSOR is INPUT + 1.

%Natural Number Function
%zero is included
%takes input like (4)
%returns true if number is greater than or equal to 0.
natNum(0).
natNum(INPUT):-
    successor(X, INPUT),
    X >= 0,
    natNum(X).

%Addition Function
%takes input like (3,4,OUTPUT) (number, number, output variable)
%(3,4,OUTPUT) will return "OUTPUT = 7"
plus(INPUT1, 0, INPUT1).
plus(INPUT1, INPUT2, OUTPUT):-
    successor(INPUT1, SUCCESSOR),successor(PREVIOUS, INPUT2),
    plus(SUCCESSOR, PREVIOUS, OUTPUT).

%Multiplication Function
%takes input like (3,4,OUTPUT) (number, number, output variable)
%(3,4,OUTPUT) will return "OUTPUT = 12"
mult(INPUT1,INPUT2,OUTPUT):-
    helper(INPUT1,INPUT1,INPUT2,OUTPUT).
helper(INPUT1,_,1,INPUT1).
helper(INPUT1,INPUT3,INPUT2,OUTPUT):-
    plus(INPUT1,INPUT3,OUTPUT2),successor(PREVIOUS,INPUT2),
    helper(OUTPUT2,INPUT3,PREVIOUS,OUTPUT).

%Exponential Function
%takes input like (3,4,OUTPUT) (number, number, output variable)
%(3,4,OUTPUT) will return "OUTPUT = 81"
exp(INPUT1,INPUT2,OUTPUT):-
    helperTwo(INPUT1,INPUT1,INPUT2,OUTPUT).
helperTwo(INPUT1,_,1,INPUT1).
helperTwo(INPUT1,INPUT3,INPUT2,OUTPUT):-
    mult(INPUT1,INPUT3,OUTPUT2),successor(PREVIOUS,INPUT2),
    helperTwo(OUTPUT2,INPUT3,PREVIOUS,OUTPUT).

