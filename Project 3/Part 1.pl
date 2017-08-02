natNum(0).
natNum(X) :-
    successor(X, Y),
    X >= 0,
    natNum(X).

successor(Number,Successor):-
    var(Number) ->
    Number is Successor -1; Successor is Number + 1.
