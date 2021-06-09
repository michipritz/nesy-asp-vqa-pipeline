import argparse
import errno
import json
import os
import time
from datetime import datetime

import clingo
import tqdm

from utils import get_stats, get_guesses_from_models, help_messages, AnswerMode, translate

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--facts', type=str,
                        default='facts_out/facts_150_enhanced_multiple.json', help=help_messages['facts'])

    parser.add_argument('-q', '--questions', type=str,
                        default='data/CLEVR_v1.0/questions/CLEVR_val_questions.json', help=help_messages['questions'])

    parser.add_argument('-o', '--out', type=str,
                        default='results_out/results.txt', help=help_messages['results_out'])

    parser.add_argument('-t', '--theory', type=str, help='File (.lp) containing additional ASP rules, e.g. for spatial reasoning')

    parser.add_argument('--answer_mode', type=AnswerMode, default=AnswerMode.multiple,
                        choices=list(AnswerMode), help=help_messages['answer_mode'])

    args = parser.parse_args()
    print(f'Command line arguments: {args}')

    start_time = time.time()

    # Create output directory and file if not existing
    if not os.path.exists(os.path.dirname(args.out)) and os.path.dirname(args.out):
        try:
            os.makedirs(os.path.dirname(args.out))
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

    # Write creation timestamp in output file
    with open(args.out, 'w') as out_fp:
        out_fp.write(f'Created on {datetime.now()}\n\n')

    # Load facts from specified file
    with open(args.facts) as fp:
        facts = json.load(fp)['facts']

    # Load questions from specified file
    with open(args.questions) as questions_file:
        questions = json.load(questions_file)

    # Initialize stats
    q_total = 0
    q_correct = 0
    q_wrong = 0
    q_invalid = 0
    total_answers = 0
    total_answer_sets = 0

    # opt-mode=opt makes clingo use weak constraints (optimization statements in general)
    # opt-mode=ignore makes clingo ignore weak constraints (optimization statements in general)
    optMode = '--opt-mode=opt' if args.answer_mode == AnswerMode.single else '--opt-mode=ignore'

    for q in tqdm.tqdm(questions["questions"], desc='Reasoning'):
        program = "\n" + '\n'.join(facts[str(q['image_index'])]) + "\n" + translate(q["program"])

        # Set up clingo
        models = []
        ctl = clingo.Control(['--models=0', optMode], message_limit=0)
        ctl.add("base", [], program)
        ctl.load(args.theory)

        # Ground and solve
        ctl.ground([("base", [])])
        with ctl.solve(yield_=True) as handle:
            for model in handle:
                models.append(model.symbols(atoms=True))

        # Check if computed answer(s) and ground truth are the same
        if models:
            guesses = get_guesses_from_models(models)
            total_answers += len(guesses)

            ground_truth = str(q["answer"])

            if ground_truth in guesses:
                q_correct += 1
            else:
                q_wrong += 1
        else:
            q_invalid += 1

        q_total += 1

    end_time = time.time()

    print(f'Total answers: {total_answers}')

    with open(args.out, 'a') as fp:
        fp.write("Results:\n")
        fp.write("Total time (s): " + str((end_time - start_time)) + "\n")
        fp.write(get_stats(q_total, q_correct, q_wrong, q_invalid))
