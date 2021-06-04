import json
import time

import clingo
import argparse
import tqdm

from utils.utils import print_stats, get_guesses_from_models, help_messages, PostprocessingMethod, AnswerMode
from translate import translate
from pytorchyolo.detect import create_data_loader
from scene_parser.scene_parser import SceneParser

USE_CONSTRAINTS = False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-m', '--model', type=str,
                        default='scene_parser/config/yolov3_scene_parser.cfg', help=help_messages['model'])

    parser.add_argument('-w', '--weights', type=str,
                        default='scene_parser/weights/yolov3_ckpt_150.pth', help=help_messages['weights'])

    parser.add_argument('-i', '--images', type=str,
                        default='data/CLEVR_v1.0/images/val', help=help_messages['images'])

    parser.add_argument('-q', '--questions', type=str,
                        default='data/CLEVR_v1.0/questions/CLEVR_val_questions.json', help=help_messages['questions'])

    parser.add_argument('--img_size', type=int,
                        default=480, help=help_messages['img_size'])

    parser.add_argument('--facts_out', type=str,
                        default='facts_out/facts_150_enhanced_multiple.json', help=help_messages['facts_out'])

    parser.add_argument('--results_out', type=str,
                        default='results_out/', help=help_messages['results_out'])

    parser.add_argument('--conf_thres', type=float,
                        default=0.5, help=help_messages['conf_thres'])

    parser.add_argument('--nms_thres', type=float,
                        default=0.5, help=help_messages['nms_thres'])

    parser.add_argument('--sd_factor', type=float,
                        default=1.0, help=help_messages['sd_factor'])

    parser.add_argument('--fallback_value', type=int,
                        default=2, help=help_messages['fallback_value'])

    parser.add_argument('--postprocessing_method', type=PostprocessingMethod,
                        default=PostprocessingMethod.enhanced, choices=list(PostprocessingMethod),
                        help=help_messages['postprocessing_method'])

    parser.add_argument('--answer_mode', type=AnswerMode, default=AnswerMode.multiple,
                        choices=list(AnswerMode), help=help_messages['answer_mode'])

    args = parser.parse_args()
    print(f'Command line arguments: {args}')

    start_time = time.time()

    dataloader = create_data_loader(args.images, 16, args.img_size, 8)

    sceneParser = SceneParser(config=args.model,
                              weights=args.weights,
                              images=args.images,
                              img_size=args.img_size,
                              facts_out=args.facts_out,
                              conf_thres=args.conf_thres,
                              nms_thres=args.nms_thres,
                              sd_factor=args.sd_factor,
                              fallback_value=args.fallback_value,
                              postprocessing_method=args.postprocessing_method)

    facts = sceneParser.parse(data=dataloader)

    # Load questions from specified file
    with open(args.questions) as questions_file:
        questions = json.load(questions_file)

    q_total = 0
    q_correct = 0
    q_wrong = 0
    q_invalid = 0

    optMode = '--opt-mode=optN' if USE_CONSTRAINTS else '--opt-mode=ignore'
    for q in tqdm.tqdm(questions["questions"], desc='Reasoning'):
        program = "\n" + '\n'.join(facts[str(q['image_index'])]) + "\n" + translate(q["program"])

        models = []
        ctl = clingo.Control(['--models=0', optMode, '--parallel-mode=8'], message_limit=0)
        ctl.add("base", [], program)
        ctl.load("theory.lp")
        ctl.ground([("base", [])])
        with ctl.solve(yield_=True) as handle:
            for model in handle:
                if USE_CONSTRAINTS:
                    if model.optimality_proven:
                        models.append(model.symbols(atoms=True))
                else:
                    models.append(model.symbols(atoms=True))

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
