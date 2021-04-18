% -- Relate --
relate(Id',Id,left) :- obj(Id,Shape,Size,Color,Material,X,Y,Z),
                       obj(Id',Shape',Size',Color',Material',X',Y',Z'), X'<X.

relate(Id',Id,right) :- obj(Id,Shape,Size,Color,Material,X,Y,Z),
                        obj(Id',Shape',Size',Color',Material',X',Y',Z'), X'>X.

relate(Id',Id,behind) :- obj(Id,Shape,Size,Color,Material,X,Y,Z),
                         obj(Id',Shape',Size',Color',Material',X',Y',Z'), Y'<Y.

relate(Id',Id,front) :- obj(Id,Shape,Size,Color,Material,X,Y,Z),
                        obj(Id',Shape',Size',Color',Material',X',Y',Z'), Y'>Y.