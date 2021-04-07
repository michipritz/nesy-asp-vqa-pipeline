% -- Relate --
relate(Id',Id,left) :- obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2), obj(Id',Shape',Size',Color',Material',X1',Y1',X2',Y2'), X1'<X1.
relate(Id',Id,right) :- obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2), obj(Id',Shape',Size',Color',Material',X1',Y1',X2',Y2'), X1'>X1.
relate(Id',Id,behind) :- obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2), obj(Id',Shape',Size',Color',Material',X1',Y1',X2',Y2'), Y1'<Y1.
relate(Id',Id,front) :- obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2), obj(Id',Shape',Size',Color',Material',X1',Y1',X2',Y2'), Y1'>Y1.