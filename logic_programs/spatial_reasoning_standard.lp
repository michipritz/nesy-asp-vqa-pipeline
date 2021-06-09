
relate(Id',left,Id) :- obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2),
                       obj(Id',Shape',Size',Color',Material',X1',Y1',X2',Y2'),
                       X1'<X1,
                       Id!=Id'.

relate(Id',right,Id) :- obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2),
                        obj(Id',Shape',Size',Color',Material',X1',Y1',X2',Y2'),
                        Id!=Id',
                        not relate(Id',left,Id).

relate(Id',front,Id) :- obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2),
                        obj(Id',Shape',Size',Color',Material',X1',Y1',X2',Y2'),
                        Y2'>Y2,
                        Id!=Id'.

relate(Id',behind,Id) :- obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2),
                         obj(Id',Shape',Size',Color',Material',X1',Y1',X2',Y2'),
                         Id!=Id',
                         not relate(Id',front,Id).