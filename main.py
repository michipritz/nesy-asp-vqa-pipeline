import json
import clingo
import re
import time

from translate import translate


def print_stats(total, correct, invalid):
    correct_rel = correct / total
    invalid_rel = invalid / total

    print("Questions total: " + str(total))
    print("Questions correct: " + str(correct) + "\t\t(" + str(correct_rel) + ")")
    print("Questions invalid: " + str(invalid) + "\t\t(" + str(invalid_rel) + ")\n")


if __name__ == "__main__":
    with open("data/scenes/CLEVR_val_scenes.json") as scenes_file:
        scenes = json.load(scenes_file)

    with open("data/questions/CLEVR_val_questions.json") as questions_file:
        questions = json.load(questions_file)

    with open("theory.lp") as hard_rules_file:
        theory = hard_rules_file.read()

    questions_dict = {}
    for i, q in enumerate(questions["questions"]):
        if q["image_index"] in questions_dict:
            questions_dict[q["image_index"]].append(q)
        else:
            questions_dict[q["image_index"]] = [q]

    q_total = 0
    q_correct = 0
    q_invalid = 0

    start_time = time.time()
    for i, scene in enumerate(scenes["scenes"]):
        program = ""

        objects = ""
        spacial_relations = ""
        for j, obj in enumerate(scenes["scenes"][i]["objects"]):
            left = ""
            right = ""
            behind = ""
            front = ""

            objects += "obj(id" + str(j) + "," \
                       + obj["shape"] + "," \
                       + obj["size"] + "," \
                       + obj["color"] + "," \
                       + obj["material"] + "," \
                       + str("pixel_coords"[0]) + "," \
                       + str("pixel_coords"[1]) + "," \
                       + str(round(obj["pixel_coords"][2]*100)) + ").\n"

            for k in scenes["scenes"][i]["relationships"]["left"][j]:
                left += "relate(id" + str(k) + ",id" + str(j) + ",left)."

            for k in scenes["scenes"][i]["relationships"]["right"][j]:
                left += "relate(id" + str(k) + ",id" + str(j) + ",right)."

            for k in scenes["scenes"][i]["relationships"]["behind"][j]:
                left += "relate(id" + str(k) + ",id" + str(j) + ",behind)."

            for k in scenes["scenes"][i]["relationships"]["front"][j]:
                left += "relate(id" + str(k) + ",id" + str(j) + ",front)."

            spacial_relations += left + "\n" + right + "\n" + behind + "\n" + front + "\n"

        program += "\n" + objects + "\n" + spacial_relations + "\n"

        for j, q in enumerate(questions_dict[i]):
            if q_total % 5000 == 0 and q_total > 0:
                print_stats(q_total, q_correct, q_invalid)

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
                elif guess_val == "true":
                    if ground_truth == "yes":
                        q_correct += 1
                elif guess_val == "false":
                    if ground_truth == "no":
                        q_correct += 1
                else:
                    if ground_truth == guess_val:
                        q_correct += 1
            else:
                q_invalid += 1

            q_total += 1

    end_time = time.time()

    print("Total time (s): " + str((end_time - start_time)))
    print_stats(q_total, q_correct, q_invalid)
