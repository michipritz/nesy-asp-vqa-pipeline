import argparse
import errno
import json
import os

import clingo
from clingo.symbol import SymbolType
from tqdm import tqdm

from utils import help_messages, func_to_asp


def encode_scene(objects, spatial_relations):
    encoding = []
    for obj_id, obj in enumerate(objects):
        size = obj["size"]
        color = obj["color"]
        material = obj["material"]
        shape = obj["shape"]
        encoding.append(f"obj(0,{obj_id},{size},{color},{material},{shape},0,0,0,0).")

    for rel in spatial_relations:
        for id1, ids in enumerate(spatial_relations[rel]):
            for id2 in ids:
                encoding.append(f"{rel}({id2},{id1}).")

    return "\n".join(encoding)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-o', '--out', type=str,
                        default='reasoning_ground_truth/out.txt', help=help_messages['results_out'])

    args = parser.parse_args()
    print(f'Command line arguments: {args}')

    # Create output directory and file if not existing
    if not os.path.exists(os.path.dirname(args.out)) and os.path.dirname(args.out):
        try:
            os.makedirs(os.path.dirname(args.out))
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

    with open("data/CLEVR_v1.0/scenes/CLEVR_val_scenes.json", "r") as fp:
        scenes = json.load(fp)["scenes"]
        scene_info = {}
        for scene in scenes:
            scene_info[scene["image_index"]] = encode_scene(scene["objects"], scene["relationships"])

    with open("data/CLEVR_v1.0/questions/CLEVR_val_questions.json") as fp:
        questions = json.load(fp)["questions"]

    # Array to hold output content
    lines = []

    # print(scene_info[63])
    # exit()

    for question in tqdm(questions):
        question_encoding = func_to_asp(question["program"])
        scene_encoding = scene_info[question['image_index']]
        encoding = "\n".join([scene_encoding, question_encoding])
        models = set()
        answer_type = ""

        # Set up clingo
        ctl = clingo.Control(['--models=0'], message_limit=0)
        ctl.add("base", [], encoding)
        ctl.load(f"commonsense_knowledge/commonsense_knowledge.lp")

        # Ground and solve
        ctl.ground([("base", [])])
        with ctl.solve(yield_=True) as handle:
            for model in handle:
                for ans in model.symbols(shown=True):
                    val = ans.arguments[0]
                    if val.type == SymbolType.Number:
                        val = str(val.number)
                    elif val.type == SymbolType.Function:
                        if val.name in ['true', 'false']:
                            val = 'no' if val.name == 'false' else 'yes'
                        else:
                            val = val.name
                    models.add(val)

        # Check if computed answer(s) and ground truth are the same
        if models:
            guesses = [guess for guess in models]

            ground_truth = str(question["answer"])

            if ground_truth in guesses:
                answer_type = "correct"
            else:
                answer_type = "wrong"
                if question['program'][-1]['function'] == "count":
                    print(f"Image index: {question['image_index']}")
                    print(f"{question['program']}")
                    print(f"{question_encoding}")
        else:
            guesses = []
            answer_type = "invalid"

        lines.append(f"{question['program'][-1]['function']}|{answer_type}|{guesses}")

    with open(args.out, 'w') as fp:
        fp.write("\n".join(lines))
