% Remarks:
% - Can deal with ambiguity

% OBJECT SECTION

% object(id,shape,size,color,material,x1,y1,x2,y2)

object(id1,cube,small,brown,rubber,10,10,5,5); -object(id1,cube,small,brown,rubber,10,10,5,5).
object(id2,sphere,large,brown,metal,5,5,100,100); -object(id2,sphere,large,yellow,metal,5,5,100,100).
object(id3,cube,small,red,metal,15,15,5,5); -object(id3,cube,large,red,metal,15,15,5,5).

% HARD RULES

% -- Filter size --
:- filter_size(Size'), -object(_,_,Size,_,_,_,_,_,_), Size'=Size.
:- filter_size(Size'), object(Id,_,Size,_,_,_,_,_,_), Size'!=Size,
	not same_size(object(Id,_,Size,_,_,_,_,_,_), object(_,_,Size',_,_,_,_,_,_)),
	not same_color(object(Id,_,Size,_,_,_,_,_,_), object(_,_,Size',_,_,_,_,_,_)),
	not same_material(object(Id,_,Size,_,_,_,_,_,_), object(_,_,Size',_,_,_,_,_,_)),
	not same_shape(object(Id,_,Size,_,_,_,_,_,_), object(_,_,Size',_,_,_,_,_,_)).

% -- Filter color --
:- filter_color(Color'), -object(_,_,_,Color,_,_,_,_,_), Color'=Color.
:- filter_color(Color'), object(Id,_,_,Color,_,_,_,_,_), Color'!=Color,
	not same_size(object(Id,_,_,Color,_,_,_,_,_), object(_,_,_,Color',_,_,_,_,_)),
	not same_color(object(Id,_,_,Color,_,_,_,_,_), object(_,_,_,Color',_,_,_,_,_)),
	not same_material(object(Id,_,_,Color,_,_,_,_,_), object(_,_,_,Color',_,_,_,_,_)),
	not same_shape(object(Id,_,_,Color,_,_,_,_,_), object(_,_,_,Color',_,_,_,_,_)).

% -- Filter material --
:- filter_material(Material'), -object(_,_,_,_,Material,_,_,_,_), Material'=Material.
:- filter_material(Material'), object(Id,_,_,_,Material,_,_,_,_), Material'!=Material, 
	not same_size(object(Id,_,_,_,Material,_,_,_,_), object(_,_,_,_,Material',_,_,_,_)),
	not same_color(object(Id,_,_,_,Material,_,_,_,_), object(_,_,_,_,Material',_,_,_,_)),
	not same_material(object(Id,_,_,_,Material,_,_,_,_), object(_,_,_,_,Material',_,_,_,_)),
	not same_shape(object(Id,_,_,_,Material,_,_,_,_), object(_,_,_,_,Material',_,_,_,_)).

% -- Filter shape --
:- filter_shape(Shape'), -object(_,Shape,_,_,_,_,_,_,_), Shape'=Shape.
:- filter_shape(Shape'), object(Id,Shape,_,_,_,_,_,_,_), Shape'!=Shape,
	not same_size(object(Id,Shape,_,_,_,_,_,_,_), object(_,Shape',_,_,_,_,_,_,_)),
	not same_color(object(Id,Shape,_,_,_,_,_,_,_), object(_,Shape',_,_,_,_,_,_,_)),
	not same_material(object(Id,Shape,_,_,_,_,_,_,_), object(_,Shape',_,_,_,_,_,_,_)),
	not same_shape(object(Id,Shape,_,_,_,_,_,_,_), object(_,Shape',_,_,_,_,_,_,_)).

% -- Exist --
exist(true) :- exist, object(_,_,_,_,_,_,_,_,_).
exist(false) :- exist, not object(_,_,_,_,_,_,_,_,_).

% -- Count --
count(X) :- count, X = #count {Id:object(Id,_,_,_,_,_,_,_,_)}.

% -- Unique --
unique(true) :- unique, not unique(false).
unique(false) :- unique, object(Id,_,_,_,_,_,_,_,_), object(Id',_,_,_,_,_,_,_,_), Id!=Id'.

% -- Relate --
left_of(Id',Id) :- left_of, object(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2), object(Id',Shape',Size',Color',Material',X1',Y1',X2',Y2'), X1'<X1.

right_of(Id',Id) :- right_of, object(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2), object(Id',Shape',Size',Color',Material',X1',Y1',X2',Y2'), X1'>X1.

behind_of(Id',Id) :- behind_of, object(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2), object(Id',Shape',Size',Color',Material',X1',Y1',X2',Y2'), Y1'>Y1.

in_front_of(Id',Id) :- in_front_of, object(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2), object(Id',Shape',Size',Color',Material',X1',Y1',X2',Y2'), Y1'<Y1.

% -- Same size --
same_size(object(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2), object(Id',Shape',Size',Color',Material',X1',Y1',X2',Y2')) :- same_size, object(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2), object(Id',Shape',Size',Color',Material',X1',Y1',X2',Y2'), Size=Size', Id!=Id'.
:- same_size, not same_size(_,_).

% -- Same color --
same_color(object(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2), object(Id',Shape',Size',Color',Material',X1',Y1',X2',Y2')) :- same_color, object(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2), object(Id',Shape',Size',Color',Material',X1',Y1',X2',Y2'), Color=Color', Id!=Id'.
:- same_color, not same_color(_,_).

% -- Same material --
same_material(object(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2), object(Id',Shape',Size',Color',Material',X1',Y1',X2',Y2')) :- same_material, object(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2), object(Id',Shape',Size',Color',Material',X1',Y1',X2',Y2'), Material=Material', Id!=Id'.
:- same_material, not same_material(_,_).

% -- Same shape --
same_shape(object(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2), object(Id',Shape',Size',Color',Material',X1',Y1',X2',Y2')) :- same_shape, object(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2), object(Id',Shape',Size',Color',Material',X1',Y1',X2',Y2'), Shape=Shape', Id!=Id'.
:- same_shape, not same_shape(_,_).


% -- Equal size --
equal_size(false) :- equal_size, object(Id,_,Size,_,_,_,_,_,_), object(Id',_,Size',_,_,_,_,_,_), Size!=Size'.
equal_size(true) :- equal_size, not equal_size(false).

% -- Equal material --
equal_material(false) :- equal_material, object(Id,_,_,_,Material,_,_,_,_), object(Id',_,_,_,Material',_,_,_,_), Material!=Material'.
equal_material(true) :- equal_material, not equal_material(false).

% -- Equal color --
equal_color(false) :- equal_color, object(Id,_,_,Color,_,_,_,_,_), object(Id',_,_,Color',_,_,_,_,_), Color!=Color'.
equal_color(true) :- equal_color, not equal_color(false).

% -- Equal shape --
equal_shape(false) :- equal_shape, object(Id,Shape,_,_,_,_,_,_,_), object(Id',Shape',_,_,_,_,_,_,_), Shape!=Shape'.
equal_shape(true) :- equal_shape, not equal_shape(false).


% -- Query size --
size(Id,Size) :- query_size, object(Id,_,Size,_,_,_,_,_,_).

% -- Query color --
color(Id,Color) :- query_color, object(Id,_,_,Color,_,_,_,_,_).

% -- Query material --
material(Id,Material) :- query_material, object(Id,_,_,_,Material,_,_,_,_).

% -- Query shape --
shape(Id,Shape) :- query_shape, object(Id,Shape,_,_,_,_,_,_,_).

% QUESTION SECTION

