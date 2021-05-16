import json
import time

import clingo
import tqdm

from utils.utils import print_stats, get_guesses_from_models
from translate import translate
from scene_parser.scene_parser import SceneParser

# Config file for YOLOv3 network
CONFIG_PATH = './scene_parser/config/yolov3_scene_parser.cfg'

# Weights file for YOLOv3 network
WEIGHTS_PATH = './scene_parser/weights/yolov3_ckpt_100.pth'

# Path to folder containing CLEVR scene images
DATA_PATH = './data/CLEVR_v1.0/images/val_mini'

# Path to file containing parsed scene information in json format
# Will be generated and saved if it does not exist
SCENES_PARSED_PATH = './scene_parser/asp_facts_enhanced_100.json'

# Path to CLEVR questions
QUESTIONS_PATH = 'data/CLEVR_v1.0/questions/CLEVR_val_questions.json'

# Size of input images, non square images will be padded s.t. dimension is IMG_SIZExIMG_SIZE
IMG_SIZE = 416

# Confidence threshold used by YOLOv3. Bounding boxes with object_score < CONF_THRESHOLD are discarded
CONF_THRESHOLD_NETWORK = 0.5

CONF_THRESHOLD_PARSER = 0

# Non maximum suppression threshold used by YOLOv3. Bounding boxes with smaller maximum class score having
# Intersection of Union (IoU) greater than NMS_THRESHOLD are discarded
NMS_THRESHOLD = 0.5

# Scaling factor used by scene parser to calculate confidence threshold. Class scores with a value less than
# conf_mean - SD_FACTOR * conf_sd are discarded. conf_mean is the estimated mean of maximum class scores over all
# bounding boxes predicted by the network and conf_sd the corresponding estimation of the standard deviation
SD_FACTOR = 1.5

# Backup value used by scene parser to choose the number of bounding box predictions if no class score surpasses
# the value of conf_mean - SD_FACTOR * conf_sd. If this case arises the BACKUP_VALUE highest class scores are picked
BACKUP_VALUE = 3

# If true simply the highest scoring class is picked for one bounding box prediction, no disjunction is used
STANDARD_DETECTION = False

if __name__ == "__main__":
    with open(QUESTIONS_PATH) as questions_file:
        questions = json.load(questions_file)

    q_total = 0
    q_correct = 0
    q_wrong = 0
    q_invalid = 0

    start_time = time.time()

    sceneParser = SceneParser(config=CONFIG_PATH,
                              weights=WEIGHTS_PATH,
                              data=DATA_PATH,
                              img_size=IMG_SIZE)

    facts = sceneParser.parse(img_size=IMG_SIZE,
                              conf_threshold_network=CONF_THRESHOLD_NETWORK,
                              conf_threshold_parser=CONF_THRESHOLD_PARSER,
                              nms_threshold=NMS_THRESHOLD,
                              facts=SCENES_PARSED_PATH,
                              sd_factor=SD_FACTOR,
                              backup_value=BACKUP_VALUE,
                              standard_detection=STANDARD_DETECTION)

    for q in tqdm.tqdm(questions["questions"][:5000], desc='Reasoning'):
        program = "\n" + '\n'.join(facts[str(q['image_index'])]) + "\n" + translate(q["program"])

        models = []
        ctl = clingo.Control("0", message_limit=0)
        ctl.add("base", [], program)
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
