import json

import clingo
import re
import time

from translate import translate
from scene_parser.scene_parser import SceneParser


def print_stats(total, correct, wrong, invalid):
    correct_rel = correct / total * 100
    wrong_rel = wrong / total * 100
    invalid_rel = invalid / total * 100

    print("Questions total: \t{:7d}".format(total))
    print("Questions correct: \t{:7d} ({:4.2f}%)".format(correct, correct_rel))
    print("Questions wrong: \t{:7d} ({:4.2f}%)".format(wrong, wrong_rel))
    print("Questions invalid: \t{:7d} ({:4.2f}%)\n".format(invalid, invalid_rel))


def print_question_info(q_id, q_natural, q_true_ans, q_given_ans):
    print('Image ID: {}'.format(str(q_id)))
    print('Question: {}'.format(str(q_natural)))
    print('Expected Answer: {}'.format(str(q_true_ans)))
    print('Given Answer: {}\n'.format(str(q_given_ans)))


if __name__ == "__main__":
    with open("data/CLEVR_v1.0/questions/CLEVR_val_questions.json") as questions_file:
        questions = json.load(questions_file)

    with open("theory.lp") as hard_rules_file:
        theory = hard_rules_file.read()

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
