import json
import os
from PIL import Image
import numpy as np

import clingo
import re
import time

from translate import translate
from scene_parser.scene_parser import SceneParser


def print_stats(total, correct, wrong, invalid):
    correct_rel = correct / total
    wrong_rel = wrong / total
    invalid_rel = invalid / total

    print("Questions total: " + str(total))
    print("Questions correct: " + str(correct) + " (" + str(correct_rel) + ")")
    print("Questions wrong: " + str(wrong) + " (" + str(wrong_rel) + ")")
    print("Questions invalid: " + str(invalid) + " (" + str(invalid_rel) + ")\n")


if __name__ == "__main__":
    with open("data/CLEVR_v1.0/questions/CLEVR_val_questions.json") as questions_file:
        questions = json.load(questions_file)

    with open("theory.lp") as hard_rules_file:
        theory = hard_rules_file.read()

    # questions_dict = {}
    # for i, q in enumerate(questions["questions"]):
    #    if q["image_index"] in questions_dict:
    #        questions_dict[q["image_index"]].append(q)
    #    else:
    #        questions_dict[q["image_index"]] = [q]

    q_total = 0
    q_correct = 0
    q_wrong = 0
    q_invalid = 0

    start_time = time.time()

    # Parse all images in ./data/CLEVR_v1.0/images/val
    # Facts contains parsed scene information for all scenes as ASP facts afterwards
    facts = SceneParser().parse()

    for i, q in enumerate(questions["questions"]):
        image_index = q['image_index']

        program = theory
        program += "\n" + '\n'.join(facts[str(image_index)]) + "\n"

        if q_total % 500 == 0 and q_total > 0:
            print_stats(q_total, q_correct, q_wrong, q_invalid)

        q_asp = translate(q["program"])
        composite_program = program + q_asp

        models = []
        ctl = clingo.Control("0", message_limit=0)
        ctl.add("base", [], composite_program)
        ctl.ground([("base", [])])
        ctl.solve(on_model=lambda m: models.append(m.symbols(atoms=True)))

        guess = ""
        if models:
            for atom in models[0]:
                if "ans" in atom.name:
                    guess = str(atom)

        ground_truth = q["answer"]

        # print('Image ID: {}'.format(str(image_index)))
        # print('Question: {}'.format(q['question']))
        # print('Expected Answer: {}'.format(str(ground_truth)))
        # print('Given Answer: {}\n'.format(str(guess)))

        if guess:
            guess_val = re.search(r'\(([^)]+)', guess).group(1)
            if guess_val.isnumeric():
                if guess_val == str(ground_truth):
                    q_correct += 1
                else:
                    q_wrong += 1
            elif guess_val == "true":
                if ground_truth == "yes":
                    q_correct += 1
                else:
                    q_wrong += 1
            elif guess_val == "false":
                if ground_truth == "no":
                    q_correct += 1
                else:
                    q_wrong += 1
            else:
                if ground_truth == guess_val:
                    q_correct += 1
                else:
                    q_wrong += 1
        else:
            q_invalid += 1

        q_total += 1

    end_time = time.time()

    print("Total time (s): " + str((end_time - start_time)))
    print_stats(q_total, q_correct, q_wrong, q_invalid)
