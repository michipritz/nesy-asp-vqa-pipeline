:- use_module(library(aggregate)).
unique(-1,-1).
relate_left(-1,-1).
relate_right(-1,-1).
relate_front(-1,-1).
relate_behind(-1,-1).
count(-1,-1).
exist(-1,-1).
filter_large(-1,-1).
filter_small(-1,-1).
filter_gray(-1,-1).
filter_red(-1,-1).
filter_blue(-1,-1).
filter_green(-1,-1).
filter_brown(-1,-1).
filter_purple(-1,-1).
filter_cyan(-1,-1).
filter_yellow(-1,-1).
filter_metal(-1,-1).
filter_rubber(-1,-1).
filter_sphere(-1,-1).
filter_cylinder(-1,-1).
filter_cube(-1,-1).
query_size(-1,-1).
query_color(-1,-1).
query_material(-1,-1).
query_shape(-1,-1).
and(-1,-1,-1).
or(-1,-1).
or(-1,-1,-1).
same_size(-1,-1).
same_color(-1,-1).
same_material(-1,-1).
same_shape(-1,-1).
equal_integer(-1,-1,-1).
less_than(-1,-1,-1).
greater_than(-1,-1,-1).
equal_size(-1,-1,-1).
equal_color(-1,-1,-1).
equal_material(-1,-1,-1).
equal_shape(-1,-1,-1).
size(-1,-1).
color(-1,-1).
material(-1,-1).
shape(-1,-1).
bool(-1,-1).
int(-1,-1).
int(-1,-1).
label(-1,-1,-1,-1).
end(-2).

% Scene rule
obj(Z,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- scene(T,0), Z is T+1, obj(0,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2).

% Unique rule/constraint
% obj(Z,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- unique(T,T1), Z is T+1, obj(T1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2).
%:- unique(T,T1), obj(T1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), obj(T1,ID1,SIZE1,COLOR1,MATERIAL1,SHAPE1,X11,Y11,X21,Y21), ID=\=ID1.
failure :- unique(T,T1), Z is T+1, obj(T1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), obj(T1,ID1,SIZE1,COLOR1,MATERIAL1,SHAPE1,X11,Y11,X21,Y21), ID \= ID1.
obj(Z,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- unique(T,T1), Z is T+1, obj(T1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2).


% Relate rules
obj(Z,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- relate_left(T,T1), Z is T+1, obj(0,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), obj(T1,ID1,SIZE1,COLOR1,MATERIAL1,SHAPE1,X11,Y11,X21,Y21), ID=\=ID1, X1<X11.
obj(Z,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- relate_right(T,T1), Z is T+1, obj(0,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), obj(T1,ID1,SIZE1,COLOR1,MATERIAL1,SHAPE1,X11,Y11,X21,Y21), ID=\=ID1, X1>=X11.
obj(Z,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- relate_front(T,T1), Z is T+1, obj(0,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), obj(T1,ID1,SIZE1,COLOR1,MATERIAL1,SHAPE1,X11,Y11,X21,Y21), ID=\=ID1, Y2>Y21.
obj(Z,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- relate_behind(T,T1), Z is T+1, obj(0,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), obj(T1,ID1,SIZE1,COLOR1,MATERIAL1,SHAPE1,X11,Y11,X21,Y21), ID=\=ID1, Y2=<Y21.

% Count rule
int(T,N,ID,1) :- count(T,T1), obj(T1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2).
int(T,0,0,0) :- count(T,T1), \+ obj(T1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2).
int(T, sum<X>) :- count(T,T1), int(T,N,ID,X).

% Exist rule
bool(T,true) :- exist(T,T1), obj(T1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2).
bool(T,false) :- exist(T,T1), \+ bool(T,true).

% Filtering rules
obj(Z,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_large(T,T1), Z is T+1, obj(T1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), SIZE=large.
obj(Z,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_small(T,T1), Z is T+1, obj(T1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), SIZE=small.
obj(Z,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_gray(T,T1), Z is T+1, obj(T1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), COLOR=gray.
obj(Z,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_red(T,T1), Z is T+1, obj(T1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), COLOR=red.
obj(Z,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_blue(T,T1), Z is T+1, obj(T1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), COLOR=blue.
obj(Z,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_green(T,T1), Z is T+1, obj(T1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), COLOR=green.
obj(Z,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_brown(T,T1), Z is T+1, obj(T1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), COLOR=brown.
obj(Z,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_purple(T,T1), Z is T+1, obj(T1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), COLOR=purple.
obj(Z,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_cyan(T,T1), Z is T+1, obj(T1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), COLOR=cyan.
obj(Z,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_yellow(T,T1), Z is T+1, obj(T1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), COLOR=yellow.
obj(Z,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_metal(T,T1), Z is T+1, obj(T1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), MATERIAL=metal.
obj(Z,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_rubber(T,T1), Z is T+1, obj(T1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), MATERIAL=rubber.
obj(Z,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_sphere(T,T1), Z is T+1, obj(T1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), SHAPE=sphere.
obj(Z,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_cylinder(T,T1), Z is T+1, obj(T1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), SHAPE=cylinder.
obj(Z,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_cube(T,T1), Z is T+1, obj(T1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), SHAPE=cube.

% Query functions
size(T,SIZE) :- query_size(T,T1), obj(T1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2).
color(T,COLOR) :- query_color(T,T1), obj(T1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2).
material(T,MATERIAL) :- query_material(T,T1), obj(T1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2).
shape(T,SHAPE) :- query_shape(T,T1), obj(T1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2).

% Logical operators
obj(Z,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- and(T,T1,T2), Z is T+1, obj(T1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), obj(T2,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2).

or(T,T1) :- or(T,T1,T2).
or(T,T2) :- or(T,T1,T2).
obj(Z,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- or(T,T1), Z is T+1, obj(T1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2).

% Same-attribute relations
obj(Z,ID1,SIZE1,COLOR1,MATERIAL1,SHAPE1,X11,Y11,X21,Y21) :- same_size(T,T1), Z is T+1, obj(T1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), obj(0,ID1,SIZE1,COLOR1,MATERIAL1,SHAPE1,X11,Y11,X21,Y21), ID=\=ID1, SIZE=SIZE1.
obj(Z,ID1,SIZE1,COLOR1,MATERIAL1,SHAPE1,X11,Y11,X21,Y21) :- same_color(T,T1), Z is T+1, obj(T1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), obj(0,ID1,SIZE1,COLOR1,MATERIAL1,SHAPE1,X11,Y11,X21,Y21), ID=\=ID1, COLOR=COLOR1.
obj(Z,ID1,SIZE1,COLOR1,MATERIAL1,SHAPE1,X11,Y11,X21,Y21) :- same_material(T,T1), Z is T+1, obj(T1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), obj(0,ID1,SIZE1,COLOR1,MATERIAL1,SHAPE1,X11,Y11,X21,Y21), ID=\=ID1, MATERIAL=MATERIAL1.
obj(Z,ID1,SIZE1,COLOR1,MATERIAL1,SHAPE1,X11,Y11,X21,Y21) :- same_shape(T,T1), Z is T+1, obj(T1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), obj(0,ID1,SIZE1,COLOR1,MATERIAL1,SHAPE1,X11,Y11,X21,Y21), ID=\=ID1, SHAPE=SHAPE1.

% Integer comparison
bool(T,true) :- equal_integer(T,T1,T2), int(T1,V1), int(T2,V2), V1=V2.
bool(T,false) :- equal_integer(T,T1,T2), int(T1,V1), int(T2,V2), V1=\=V2.

% bool(T,false) :- equal_integer(T,T1,T2), \+ bool(T,true).

bool(T,true) :- less_than(T,T1,T2), int(T1,V1), int(T2,V2), V1<V2.
bool(T,false) :- less_than(T,T1,T2), int(T1,V1), int(T2,V2), V1>=V2.
% bool(T,false) :- less_than(T,T1,T2), \+ bool(T,true).

bool(T,true) :- greater_than(T,T1,T2), int(T1,V1), int(T2,V2), V1>V2.
bool(T,false) :- greater_than(T,T1,T2), int(T1,V1), int(T2,V2), V1=<V2.
% bool(T,false) :- greater_than(T,T1,T2), \+ bool(T,true).

% Attribute comparison
bool(T,true) :- equal_size(T,T1,T2), size(T1,V1), size(T2,V2), V1=V2.
bool(T,false) :- equal_size(T,T1,T2), size(T1,V1), size(T2,V2), V1 \= V2.
% bool(T,false) :- equal_size(T,T1,T2), \+ bool(T,true).

bool(T,true) :- equal_color(T,T1,T2), color(T1,V1), color(T2,V2), V1=V2.
bool(T,false) :- equal_color(T,T1,T2), color(T1,V1), color(T2,V2), V1 \= V2.
% bool(T,false) :- equal_color(T,T1,T2), \+ bool(T,true).

bool(T,true) :- equal_material(T,T1,T2), material(T1,V1), material(T2,V2), V1=V2.
bool(T,false) :- equal_material(T,T1,T2), material(T1,V1), material(T2,V2), V1 \= V2.
% bool(T,false) :- equal_material(T,T1,T2), \+ bool(T,true).

bool(T,true) :- equal_shape(T,T1,T2), shape(T1,V1), shape(T2,V2), V1=V2.
bool(T,false) :- equal_shape(T,T1,T2), shape(T1,V1), shape(T2,V2), V1 \= V2.
% bool(T,false) :- equal_shape(T,T1,T2), \+ bool(T,true).

% Derive answer (T must equal the last point in time)
ans(V) :- end(T), size(T,V), not failure.
ans(V) :- end(T), color(T,V), not failure.
ans(V) :- end(T), material(T,V), not failure.
ans(V) :- end(T), shape(T,V), not failure.
ans(V) :- end(T), bool(T,V), not failure.
ans(V) :- end(T), int(T,V), not failure.

obj(0,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- label(0,img,ID,obj(ID,SHAPE,SIZE,COLOR,MATERIAL,X1,Y1,X2,Y2)).
