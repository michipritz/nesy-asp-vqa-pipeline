
#const e = 5.

% relate(Id',left,Id) :- obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2), obj(Id',Shape',Size',Color',Material',X1',Y1',X2',Y2'), X1'<X1.
% relate(Id',right,Id) :- obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2), obj(Id',Shape',Size',Color',Material',X1',Y1',X2',Y2'), X1'>X1.
% relate(Id',behind,Id) :- obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2), obj(Id',Shape',Size',Color',Material',X1',Y1',X2',Y2'), Y1'<Y1.
% relate(Id',front,Id) :- obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2), obj(Id',Shape',Size',Color',Material',X1',Y1',X2',Y2'), Y1'>Y1.

relate(Id',left,Id) :- obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2),
                       obj(Id',Shape',Size',Color',Material',X1',Y1',X2',Y2'),
                       X1'<X1,
                       Id!=Id',
                       D=|X1-X1'|,
                       D > e.

relate(Id',left,Id); relate(Id,left,Id') :- obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2),
                                            obj(Id',Shape',Size',Color',Material',X1',Y1',X2',Y2'),
                                            Id!=Id',
                                            D=|X1-X1'|,
                                            D <= e.

relate(Id',right,Id) :- obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2),
                        obj(Id',Shape',Size',Color',Material',X1',Y1',X2',Y2'),
                        Id!=Id',
                        not relate(Id',left,Id).

relate(Id',front,Id) :- obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2),
                        obj(Id',Shape',Size',Color',Material',X1',Y1',X2',Y2'),
                        Y2'>Y2,
                        Id!=Id',
                        D=|Y2-Y2'|,
                        D > e.

relate(Id',front,Id); relate(Id,front,Id') :- obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2),
                                              obj(Id',Shape',Size',Color',Material',X1',Y1',X2',Y2'),
                                              Id!=Id',
                                              D=|Y2-Y2'|,
                                              D <= e.

relate(Id',behind,Id) :- obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2),
                         obj(Id',Shape',Size',Color',Material',X1',Y1',X2',Y2'),
                         Id!=Id',
                         not relate(Id',front,Id).