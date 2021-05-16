import json
import time

import clingo
import tqdm

from utils.utils import print_stats, get_guesses_from_models
from translate import translate
from scene_parser.scene_parser import SceneParser

if __name__ == "__main__":
    with open("data/CLEVR_v1.0/questions/CLEVR_val_questions.json") as questions_file:
        questions = json.load(questions_file)

    q_total = 0
    q_correct = 0
    q_wrong = 0
    q_invalid = 0

    start_time = time.time()

    # Parse all images in ./data/CLEVR_v1.0/images/val
    # Facts contains parsed scene information for all scenes as ASP facts afterwards
    sceneParser = SceneParser(config='./scene_parser/config/yolov3_scene_parser.cfg',
                              weights='./scene_parser/weights/yolov3_scene_parser.pth',
                              data='./data/CLEVR_v1.0/images/val_mini',
                              img_size=480)

    facts = sceneParser.parse(img_size=480,  # Size of input image (Non square images get padded)
                              conf_threshold=0.25,  # Bounding boxes with obj score less than this value are dropped
                              nms_threshold=0.5,
                              facts='./scene_parser/asp_facts_3.json',  # Path to file containing scene information
                              sd_factor=2,
                              backup_value=3)

    for q in tqdm.tqdm(questions["questions"], desc='Reasoning'):
        image_index = q['image_index']
        program = "\n" + '\n'.join(facts[str(image_index)]) + "\n"

        q_asp = translate(q["program"])
        composite_program = program + q_asp

        models = []
        ctl = clingo.Control("0", message_limit=0)
        ctl.add("base", [], composite_program)
        ctl.load("theory.lp")
        ctl.ground([("base", [])])
        ctl.solve(on_model=lambda m: models.append(m.symbols(atoms=True)))

        if models:
            guesses = get_guesses_from_models(models)

            ground_truth = str(q["answer"])

            if ground_truth in guesses:
                q_correct += 1
            else:
                q_wrong += 1
        else:
            q_invalid += 1

        q_total += 1

    end_time = time.time()

    print("\n-------------------------------")
    print("Results:")
    print("Total time (s): " + str((end_time - start_time)))
    print_stats(q_total, q_correct, q_wrong, q_invalid)
    print("-------------------------------")
