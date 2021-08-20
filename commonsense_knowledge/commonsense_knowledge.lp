% Show only ans atom
#show ans/1.

% Scene rule
obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- scene(T), obj(0,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2).

% Unique rule/constraint
obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- unique(T), obj(T,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2).
:- unique(T), obj(T,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), obj(T,ID',SIZE',COLOR',MATERIAL',SHAPE',X1',Y1',X2',Y2'), ID!=ID'.

% Relate rules
obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- relate_left(T), obj(T,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), obj(T,ID',SIZE',COLOR',MATERIAL',SHAPE',X1',Y1',X2',Y2'), ID!=ID', X1<X1'.
obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- relate_right(T), obj(T,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), obj(T,ID',SIZE',COLOR',MATERIAL',SHAPE',X1',Y1',X2',Y2'), ID!=ID', X1>=X1'.
obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- relate_front(T), obj(T,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), obj(T,ID',SIZE',COLOR',MATERIAL',SHAPE',X1',Y1',X2',Y2'), ID!=ID', Y2>Y2'.
obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- relate_behind(T), obj(T,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), obj(T,ID',SIZE',COLOR',MATERIAL',SHAPE',X1',Y1',X2',Y2'), ID!=ID', Y2<=Y2'.

% Count rule
int(T,V) :- count(T), #count {ID:obj(T,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2)}=V.

% Exist rule
bool(T,true) :- exist(T), obj(T,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2).
bool(T,false) :- exist(T), not bool(T,true).

% Filtering rules
obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_big(T), obj(T,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), SIZE=big.
obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_small(T), obj(T,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), SIZE=small.
obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_gray(T), obj(T,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), COLOR=gray.
obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_red(T), obj(T,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), COLOR=red.
obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_blue(T), obj(T,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), COLOR=blue.
obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_green(T), obj(T,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), COLOR=green.
obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_brown(T), obj(T,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), COLOR=brown.
obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_purple(T), obj(T,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), COLOR=purple.
obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_cyan(T), obj(T,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), COLOR=cyan.
obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_yellow(T), obj(T,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), COLOR=yellow.
obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_metal(T), obj(T,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), MATERIAL=metal.
obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_rubber(T), obj(T,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), MATERIAL=rubber.
obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_sphere(T), obj(T,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), SHAPE=sphere.
obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_cylinder(T), obj(T,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), SHAPE=cylinder.
obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- filter_cube(T), obj(T,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), SHAPE=cube.

% Query functions
size(T,SIZE) :- query_size(T), obj(T,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2).
color(T,COLOR) :- query_color(T), obj(T,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2).
material(T,MATERIAL) :- query_material(T), obj(T,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2).
shape(T,SHAPE) :- query_shape(T), obj(T,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2).

% Logical operators
obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- and(T,T',T''), obj(T',ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), obj(T'',ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2).

{or(T,T');or(T,T'')}=2 :- or(T,T',T'').
obj(T+1,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2) :- or(T,T'), obj(T,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2).

% Same-attribute relations
obj(T+1,ID',SIZE',COLOR',MATERIAL',SHAPE',X1',Y1',X2',Y2') :- same_size(T), obj(T,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), obj(0,ID',SIZE',COLOR',MATERIAL',SHAPE',X1',Y1',X2',Y2'), ID!=ID', SIZE=SIZE'.
obj(T+1,ID',SIZE',COLOR',MATERIAL',SHAPE',X1',Y1',X2',Y2') :- same_color(T), obj(T,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), obj(0,ID',SIZE',COLOR',MATERIAL',SHAPE',X1',Y1',X2',Y2'), ID!=ID', COLOR=COLOR'.
obj(T+1,ID',SIZE',COLOR',MATERIAL',SHAPE',X1',Y1',X2',Y2') :- same_size(T), obj(T,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), obj(0,ID',SIZE',COLOR',MATERIAL',SHAPE',X1',Y1',X2',Y2'), ID!=ID', MATERIAL=MATERIAL'.
obj(T+1,ID',SIZE',COLOR',MATERIAL',SHAPE',X1',Y1',X2',Y2') :- same_size(T), obj(T,ID,SIZE,COLOR,MATERIAL,SHAPE,X1,Y1,X2,Y2), obj(0,ID',SIZE',COLOR',MATERIAL',SHAPE',X1',Y1',X2',Y2'), ID!=ID', SHAPE=SHAPE'.

% Integer comparison
bool(T,true) :- equal_integer(T,T',T''), int(T',V'), int(T'',V''), V'=V''.
bool(T,false) :- equal_integer(T,T',T''), not bool(T,true).

bool(T,true) :- less_than(T,T',T''), int(T',V'), int(T'',V''), V'<V''.
bool(T,false) :- less_than(T,T',T''), not bool(T,true).

bool(T,true) :- greater_than(T,T',T''), int(T',V'), int(T'',V''), V'>V''.
bool(T,false) :- greater_than(T,T',T''), not bool(T,true).

% Attribute comparison
bool(T,true) :- equal_size(T,T',T''), size(T',V'), size(T'',V''), V'=V''.
bool(T,false) :- equal_size(T,T',T''), not bool(T,true).

bool(T,true) :- equal_color(T,T',T''), color(T',V'), color(T'',V''), V'=V''.
bool(T,false) :- equal_color(T,T',T''), not bool(T,true).

bool(T,true) :- equal_material(T,T',T''), material(T',V'), material(T'',V''), V'=V''.
bool(T,false) :- equal_material(T,T',T''), not bool(T,true).

bool(T,true) :- equal_shape(T,T',T''), shape(T',V'), shape(T'',V''), V'=V''.
bool(T,false) :- equal_shape(T,T',T''), not bool(T,true).

% Derive answer (T must equal the last point in time)
ans(V) :- end(T), size(T,V).
ans(V) :- end(T), color(T,V).
ans(V) :- end(T), material(T,V).
ans(V) :- end(T), shape(T,V).
ans(V) :- end(T), bool(T,V).
ans(V) :- end(T), int(T,V).


