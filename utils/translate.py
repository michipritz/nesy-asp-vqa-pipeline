actions = {
    "scene": "scene({T},{T1}).",
    "unique": "unique({T},{T1}).",
    "relate": "relate_{val}({T},{T1}).",
    "count": "count({T},{T1}).",
    "exist": "exist({T},{T1}).",
    "filter_size": "filter_{val}({T},{T1}).",
    "filter_color": "filter_{val}({T},{T1}).",
    "filter_material": "filter_{val}({T},{T1}).",
    "filter_shape": "filter_{val}({T},{T1}).",
    "query_size": "query_size({T},{T1}).",
    "query_color": "query_color({T},{T1}).",
    "query_material": "query_material({T},{T1}).",
    "query_shape": "query_shape({T},{T1}).",
    "same_size": "same_size({T},{T1}).",
    "same_color": "same_color({T},{T1}).",
    "same_material": "same_material({T},{T1}).",
    "same_shape": "same_shape({T},{T1}).",
    "equal_integer": "equal_integer({T},{T1},{T2}).",
    "less_than": "less_than({T},{T1},{T2}).",
    "greater_than": "greater_than({T},{T1},{T2}).",
    "equal_size": "equal_size({T},{T1},{T2}).",
    "equal_color": "equal_color({T},{T1},{T2}).",
    "equal_material": "equal_material({T},{T1},{T2}).",
    "equal_shape": "equal_shape({T},{T1},{T2}).",
    "union": "or({T},{T1},{T2}).",
    "intersect": "and({T},{T1},{T2})."
}

func_type = {
    "unary": ["scene", "unique", "count", "exist", "query_size", "query_color", "query_material",
              "query_shape", "same_size", "same_color", "same_material", "same_shape"],
    "binary_val": ["relate", "filter_size", "filter_color", "filter_material", "filter_shape"],
    "binary_in": ["equal_integer", "less_than", "greater_than", "equal_size", "equal_color", "equal_shape",
                  "equal_material", "union", "intersect"]
}


def func_to_asp(program):
    # Holds action sequence
    action_sequence = []
    # Time
    t = 0

    # Iterate over functional program and translate every basic function into an action atom
    for i, func in enumerate(program):
        t = i
        func_name = func["function"]
        if func_name in func_type["unary"]:
            if func_name == "scene":
                action_sequence.append(actions[func_name].format(T=t, T1=0))
            else:
                action_sequence.append(actions[func_name].format(T=t, T1=func["inputs"][0] + 1))
            # print(f"{func}, {action_sequence[-1]}")
        elif func_name in func_type["binary_val"]:
            val = func["value_inputs"][0]
            action_sequence.append(actions[func_name].format(T=t, T1=func["inputs"][0] + 1, val=val))
            # print(f"{func}, {action_sequence[-1]}")
        elif func_name in func_type["binary_in"]:
            t1 = func["inputs"][0]
            t2 = func["inputs"][1]
            if func_name in ["union", "intersect"]:
                action_sequence.append(actions[func_name].format(T=t, T1=t1+1, T2=t2+1))
            else:
                action_sequence.append(actions[func_name].format(T=t, T1=t1, T2=t2))
            # print(f"{func}, {action_sequence[-1]}")
        else:
            print("Unknown function name: " + func_name)

    # Add end atom
    action_sequence.append(f"end({t}).")

    # Return action sequence as string
    return "\n".join(action_sequence)
