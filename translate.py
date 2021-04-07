trans_template_dict = {
    "scene": "out({id_out},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)) " +
             ":- obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2).\n",
    "unique": "out({id_out}, obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)) " +
              ":- out({id_in}, obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)).\n" +
              ":- out({id_in},obj(Id,_,_,_,_,_,_,_,_)), out({id_in},obj(Id',_,_,_,_,_,_,_,_)), Id!=Id'.\n",
    "relate": "out({id_out},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)) " +
              ":- out({id_in},obj(Id',Shape',Size',Color',Material',X1',Y1',X2',Y2'))," +
              "obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2), relate(Id,Id',{val}).\n",
    "count": "out({id_out},N) :- #count {{Id:out({id_in},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2))}}=N.\n",
    "exist": "out({id_out},true) :- #count {{Id:out({id_in},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2))}}=N,N>=1.\n " +
             "out({id_out},false) :- not out({id_out},true).\n",
    "filter_size": "out({id_out},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)) " +
                   ":- out({id_in},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)), Size={val}.\n",
    "filter_color": "out({id_out},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)) " +
                    ":- out({id_in},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)), Color={val}.\n",
    "filter_material": "out({id_out},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)) " +
                       ":- out({id_in},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)), Material={val}.\n",
    "filter_shape": "out({id_out},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)) " +
                    ":- out({id_in},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)), Shape={val}.\n",
    "query_size": "out({id_out},Size) :- out({id_in},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)).",
    "query_color": "out({id_out},Color) :- out({id_in},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)).",
    "query_material": "out({id_out},Material) :- out({id_in},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)).",
    "query_shape": "out({id_out},Shape) :- out({id_in},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)).",
    "same_size": "out({id_out},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)) " +
                 ":- out({id_in},obj(Id',Shape',Size',Color',Material',X1',Y1',X2',Y2')), " +
                 "obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2), Size=Size', Id!=Id'.\n",
    "same_color": "out({id_out},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)) " +
                  ":- out({id_in},obj(Id',Shape',Size',Color',Material',X1',Y1',X2',Y2')), " +
                  "obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2), Color=Color', Id!=Id'.\n",
    "same_material": "out({id_out},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)) " +
                     ":- out({id_in},obj(Id',Shape',Size',Color',Material',X1',Y1',X2',Y2')), " +
                     "obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2), Material=Material', Id!=Id'.\n",
    "same_shape": "out({id_out},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)) " +
                  ":- out({id_in},obj(Id',Shape',Size',Color',Material',X1',Y1',X2',Y2')), " +
                  "obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2), Shape=Shape', Id!=Id'.\n",
    "equal_integer": "out({id_out},true) :- out({id_in1},N), out({id_in2},N'), N=N'.\n" +
                     "out({id_out},false) :- not out({id_out},true).\n",
    "less_than": "out({id_out},true) :- out({id_in1},N), out({id_in2},N'), N<N'.\n" +
                 "out({id_out},false) :- not out({id_out},true).\n",
    "greater_than": "out({id_out},true) :- out({id_in1},N), out({id_in2},N'), N>N'.\n" +
                    "out({id_out},false) :- not out({id_out},true).\n",
    "equal_size": "out({id_out},true) :- out({id_in1},Size), out({id_in2},Size'), Size=Size'.\n" +
                  "out({id_out},false) :- not out({id_out},true).\n",
    "equal_color": "out({id_out},true) :- out({id_in1},Color), out({id_in2},Color'), Color=Color'.\n" +
                   "out({id_out},false) :- not out({id_out},true).\n",
    "equal_material": "out({id_out},true) :- out({id_in1},Material), out({id_in2},Material'), Material=Material'.\n" +
                      "out({id_out},false) :- not out({id_out},true).\n",
    "equal_shape": "out({id_out},true) :- out({id_in1},Shape), out({id_in2},Shape'), Shape=Shape'.\n" +
                   "out({id_out},false) :- not out({id_out},true).\n",
    "union": "out({id_out},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)) " +
             ":- out({id_in1},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)).\n" +
             "out({id_out},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)) " +
             ":- out({id_in2},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)).\n",
    "intersect": "out({id_out},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)) " +
                 ":- out({id_in1},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2))," +
                 "out({id_in2},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2))."
}

func_type = {
    "const": ["scene"],
    "unary": ["unique", "count", "exist", "query_size", "query_color", "query_material",
              "query_shape", "same_size", "same_color", "same_material", "same_shape"],
    "binary_val": ["relate", "filter_size", "filter_color", "filter_material", "filter_shape"],
    "binary_in": ["equal_integer", "less_than", "greater_than", "equal_size", "equal_color", "equal_shape",
                  "equal_material", "union", "intersect"]
}


def translate(program):
    program_trans = ""

    for i, func in enumerate(program):
        func_name = func["function"]
        if func_name in func_type["const"]:
            program_trans += trans_template_dict[func_name].format(id_out=i)
        elif func_name in func_type["unary"]:
            id_in = func["inputs"][0]
            program_trans += trans_template_dict[func_name].format(id_out=i, id_in=id_in)
        elif func_name in func_type["binary_val"]:
            id_in = func["inputs"][0]
            val = func["value_inputs"][0]
            program_trans += trans_template_dict[func_name].format(id_out=i, id_in=id_in, val=val)
        elif func_name in func_type["binary_in"]:
            id_in1 = func["inputs"][0]
            id_in2 = func["inputs"][1]
            program_trans += trans_template_dict[func_name].format(id_out=i, id_in1=id_in1, id_in2=id_in2)
        else:
            print("Unknown function name: " + func_name)

    program_trans += "ans(N) :- out({id_in},N).\n".format(id_in=len(program) - 1)
    return program_trans
