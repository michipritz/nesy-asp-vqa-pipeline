# trans_template_dict = {
#    "scene": "out({id_out},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)) " +
#             ":- obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2).\n",
#    "unique": "out({id_out}, obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)) " +
#              ":- out({id_in}, obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)).\n" +
#              ":- out({id_in},obj(Id,_,_,_,_,_,_,_,_)), out({id_in},obj(Id',_,_,_,_,_,_,_,_)), Id!=Id'.\n",
#    "relate": "out({id_out},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)) " +
#              ":- out({id_in},obj(Id',Shape',Size',Color',Material',X1',Y1',X2',Y2'))," +
#              "obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2), relate(Id,{val},Id').\n",
#    "count": "out({id_out},N) :- #count {{Id:out({id_in},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2))}}=N.\n",
#    "exist": "out({id_out},true) :- #count {{Id:out({id_in},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2))}}=N,N>=1.\n " +
#             "out({id_out},false) :- not out({id_out},true).\n",
#    "filter_size": "out({id_out},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)) " +
#                   ":- out({id_in},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)), Size={val}.\n",
#    "filter_color": "out({id_out},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)) " +
#                    ":- out({id_in},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)), Color={val}.\n",
#    "filter_material": "out({id_out},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)) " +
#                       ":- out({id_in},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)), Material={val}.\n",
#    "filter_shape": "out({id_out},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)) " +
#                    ":- out({id_in},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)), Shape={val}.\n",
#    "query_size": "out({id_out},Size) :- out({id_in},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)).",
#    "query_color": "out({id_out},Color) :- out({id_in},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)).",
#    "query_material": "out({id_out},Material) :- out({id_in},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)).",
#    "query_shape": "out({id_out},Shape) :- out({id_in},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)).",
#    "same_size": "out({id_out},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)) " +
#                 ":- out({id_in},obj(Id',Shape',Size',Color',Material',X1',Y1',X2',Y2')), " +
#                 "obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2), Size=Size', Id!=Id'.\n",
#    "same_color": "out({id_out},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)) " +
#                  ":- out({id_in},obj(Id',Shape',Size',Color',Material',X1',Y1',X2',Y2')), " +
#                  "obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2), Color=Color', Id!=Id'.\n",
#    "same_material": "out({id_out},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)) " +
#                     ":- out({id_in},obj(Id',Shape',Size',Color',Material',X1',Y1',X2',Y2')), " +
#                     "obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2), Material=Material', Id!=Id'.\n",
#    "same_shape": "out({id_out},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)) " +
#                  ":- out({id_in},obj(Id',Shape',Size',Color',Material',X1',Y1',X2',Y2')), " +
#                  "obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2), Shape=Shape', Id!=Id'.\n",
#    "equal_integer": "out({id_out},true) :- out({id_in1},N), out({id_in2},N'), N=N'.\n" +
#                     "out({id_out},false) :- not out({id_out},true).\n",
#    "less_than": "out({id_out},true) :- out({id_in1},N), out({id_in2},N'), N<N'.\n" +
#                 "out({id_out},false) :- not out({id_out},true).\n",
#    "greater_than": "out({id_out},true) :- out({id_in1},N), out({id_in2},N'), N>N'.\n" +
#                    "out({id_out},false) :- not out({id_out},true).\n",
#    "equal_size": "out({id_out},true) :- out({id_in1},Size), out({id_in2},Size'), Size=Size'.\n" +
#                  "out({id_out},false) :- not out({id_out},true).\n",
#    "equal_color": "out({id_out},true) :- out({id_in1},Color), out({id_in2},Color'), Color=Color'.\n" +
#                   "out({id_out},false) :- not out({id_out},true).\n",
#    "equal_material": "out({id_out},true) :- out({id_in1},Material), out({id_in2},Material'), Material=Material'.\n" +
#                      "out({id_out},false) :- not out({id_out},true).\n",
#    "equal_shape": "out({id_out},true) :- out({id_in1},Shape), out({id_in2},Shape'), Shape=Shape'.\n" +
#                   "out({id_out},false) :- not out({id_out},true).\n",
#    "union": "out({id_out},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)) " +
#             ":- out({id_in1},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)).\n" +
#             "out({id_out},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)) " +
#             ":- out({id_in2},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)).\n",
#    "intersect": "out({id_out},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2)) " +
#                 ":- out({id_in1},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2))," +
#                 "out({id_in2},obj(Id,Shape,Size,Color,Material,X1,Y1,X2,Y2))."
# }

actions = {
    "scene": "scene({T}).",
    "unique": "unique({T}).",
    "relate": "relate_{val}({T}).",
    "count": "count({T}).",
    "exist": "exist({T}).",
    "filter_size": "filter_{val}({T}).",
    "filter_color": "filter_{val}({T}).",
    "filter_material": "filter_{val}({T}).",
    "filter_shape": "filter_{val}({T}).",
    "query_size": "query_size({T}).",
    "query_color": "query_color({T}).",
    "query_material": "query_material({T}).",
    "query_shape": "query_shape({T}).",
    "same_size": "same_size({T}).",
    "same_color": "same_color({T}).",
    "same_material": "same_material({T}).",
    "same_shape": "same_shape({T}).",
    "equal_integer": "equal_integer({T},{T1},{T2}).",
    "less_than": "less_than({T},{T1},{T2}).",
    "greater_than": "greater_than({T},{T1},{T2}).",
    "equal_size": "equal_size({T},{T1},{T2}).",
    "equal_color": "equal_color({T},{T1},{T2}).",
    "equal_material": "equal_material({T},{T1},{T2}).",
    "equal_shape": "equal_shape({T},{T1},{T2}).",
    "union": "and({T},{T1},{T2}).",
    "intersect": "or({T},{T1},{T2})."
}

func_type = {
    "unary": ["scene", "unique", "count", "exist", "query_size", "query_color", "query_material",
              "query_shape", "same_size", "same_color", "same_material", "same_shape"],
    "binary_val": ["relate", "filter_size", "filter_color", "filter_material", "filter_shape"],
    "binary_in": ["equal_integer", "less_than", "greater_than", "equal_size", "equal_color", "equal_shape",
                  "equal_material", "union", "intersect"]
}


def translate(program):
    # Holds action sequence
    action_sequence = []
    # Time
    t = 0

    # Iterate over functional program and translate every basic function into an action atom
    for i, func in enumerate(program):
        t = i
        func_name = func["function"]
        if func_name in func_type["unary"]:
            action_sequence.append(actions[func_name].format(T=t))
        elif func_name in func_type["binary_val"]:
            val = func["value_inputs"][0]
            action_sequence.append(actions[func_name].format(T=t, val=val))
        elif func_name in func_type["binary_in"]:
            t1 = func["inputs"][0]
            t2 = func["inputs"][1]
            action_sequence.append(actions[func_name].format(T=t, T1=t1+1, T2=t2+1))
        else:
            print("Unknown function name: " + func_name)

    # Add end atom
    action_sequence.append(f"end({t}).")

    # Return action sequence as string
    return "\n".join(action_sequence)
