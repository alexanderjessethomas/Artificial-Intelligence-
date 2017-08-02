%setting family tree definitions
%this is based off of figure 8.7 on page 318 of the text book
%each section is based off of the spouse
spouse(george,mum).
child(margaret, mum).
child(elizabeth,mum).
child(margaret,george).
child(elizabeth,george).
male(george).
female(mum).
female(elizabeth).
female(margaret).

spouse(spencer,kydd).
child(diana,spencer).
child(diana,kydd).
male(spencer).
female(kydd).
female(diana).

spouse(elizabeth,philip).
child(charles,elizabeth).
child(anne,elizabeth).
child(andrew,elizabeth).
child(edward,elizabeth).
child(charles,philip).
child(anne,philip).
child(andrew,philip).
child(edward,philip).
male(philip).
female(elizabeth).
male(charles).
female(anne).
male(andrew).
male(edward).

spouse(diana,charles).
child(william,diana).
child(harry,diana).
child(william,charles).
child(harry,charles).
male(charles).
female(diana).
male(harry).
male(william).

spouse(anne,mark).
child(peter,anne).
child(zara,anne).
child(peter,mark).
child(zara,mark).
male(mark).
female(anne).
male(peter).
female(zara).

spouse(andrew,sarah).
child(beatrice,andrew).
child(eugenie,andrew).
chiild(beatrice,sarah).
child(eugenie,andrew).
male(andrew).
female(sarah).
male(eugenie).
female(beatrice).

spouse(edward,sophie).
child(louise,edward).
child(james,edward).
child(louise,sophie).
child(james,sophie).
male(edward).
female(sophie).
male(james).
female(louise).

%dynamic programming test
spouse(johnny,emily).
child(mary,johnny).
child(elli-joe,johnny).
child(bubba,johnny).
child(mary,emily).
child(elli-joe,emily).
child(bubba,emily).
male(johnny).
female(emily).
female(mary).
female(elli-joe).
male(bubba).


spouse(mailman,mary).
child(cindy,mailman).
child(cindy,mary).
male(mailman).
female(mary).
female(cindy).

spouse(johnny,mary).
child(john-jr,mary).
child(johnny-b,mary).
child(frank,mary).
child(john-jr,johnny).
child(johnny-b,johnny).
child(frank,johnny).
male(johnny).
female(mary).
male(john-jr).
male(johnny-b).
male(frank).

spouse(elli-joe,bubba).
child(moose,ellie-joe).
child(crystal,ellie-joe).
child(moose,bubba).
child(crystal,bubba).
male(bubba).
female(ellie-joe).
male(moose).
female(crystal).

spouse(bubba,marysue).
child(floe,bubba).
child(floe,marysue).
male(bubba).
female(marysue).
male(floe).

spouse(frank,jenny).
child(maybelle,frank).
child(maybelle,jenny).
male(frank).
female(jenny).
female(maybelle).

spouse(floe,sue-ann).
child(hank,floe).
child(hank,sue-ann).
male(floe).
female(sue-ann).
male(hank).

%ancestor predicates
grandchild(CHILD,ANCESTOR):-
    child(CHILD,PARENT),
    child(PARENT,ANCESTOR).

greatGrandParent(ANCESTOR,CHILD):-
    child(GRANDPARENT,ANCESTOR),
    child(PARENT,GRANDPARENT),
    child(CHILD,PARENT).

ancestor(ANCESTOR,INPUT):-
    child(INPUT,CHILD),
    ancestor(ANCESTOR,CHILD).
ancestor(ANCESTOR,INPUT):-
    child(INPUT,ANCESTOR).

%immediate family predicates
brother(NAME1,NAME2):-
    child(NAME1,NAME3),
    child(NAME2,NAME3),
    female(NAME3),
    male(NAME1).

sister(NAME1,NAME2):-
    child(NAME1,NAME3),
    child(NAME2,NAME3),
    female(NAME1),
    female(NAME3).

daughter(NAME1,NAME2):-
    child(NAME1,NAME2),
    female(NAME1).

son(NAME1,NAME2):-
    child(NAME1,NAME2),
    male(NAME1).

sibling(NAME1,NAME2):-
    child(NAME1,NAME3),
    child(NAME2,NAME3),
    female(NAME3),
    NAME2 \= NAME1.

%extended family predicates
firstCousin(NAME1,NAME2):-
    child(NAME1,PARENT1),
    child(NAME2,PARENT2),
    child(PARENT1,GRANDPARENT),
    child(PARENT2,GRANDPARENT),
    female(GRANDPARENT),
    NAME1 \= NAME2,
    PARENT1 \= PARENT2.

brotherInLaw(NAME1,NAME2):-
    ((spouse(NAME1,SPOUSE);spouse(SPOUSE,NAME1)),
     female(PARENT),
     child(SPOUSE,PARENT),child(NAME2,PARENT),
     NAME2 \= SPOUSE);
    ((spouse(NAME2,SPOUSE),spouse(SPOUSE,NAME2)),
    female(PARENT),
    child(SPOUSE,PARENT),
    child(NAME1,PARENT),
    SPOUSE \= NAME1),
    male(NAME1).

sisterInLaw(NAME1,NAME2):-
     ((spouse(NAME1,SPOUSE);spouse(SPOUSE,NAME1)),
     female(PARENT),
     child(SPOUSE,PARENT),child(NAME2,PARENT),
     NAME2 \= SPOUSE);
    ((spouse(NAME2,SPOUSE),spouse(SPOUSE,NAME2)),
    female(PARENT),
    child(SPOUSE,PARENT),
    child(NAME1,PARENT),
    SPOUSE \= NAME1),
    female(NAME1).

aunt(NAME1,NAME2):-
    female(NAME1),
    (child(NAME1, PARENT),
     female(PARENT),
     child(CHILD, PARENT),
     NAME1 \= CHILD,
     child(NAME2, CHILD));
    ((spouse(NAME1, SPOUSE);spouse(SPOUSE, NAME1)),
     child(SPOUSE, PARENT),
     female(PARENT),
     child(CHILD, PARENT),
     SPOUSE \= CHILD,
     child(NAME2, CHILD)).

uncle(NAME1,NAME2):-
    male(NAME1),
   (child(NAME1, PARENT),
    female(PARENT),
    child(CHILD, PARENT),
    NAME1 \= CHILD,
    child(NAME2, CHILD));
   ((spouse(NAME1, SPOUSE);spouse(SPOUSE, NAME1)),
    child(SPOUSE, PARENT),
    female(PARENT),
    child(CHILD, PARENT),
    SPOUSE \= CHILD,
    child(NAME2, CHILD)).
