import argparse
import errno
import json
import os

import clingo
from clingo.symbol import SymbolType
from tqdm import tqdm

from utils import help_messages, AnswerMode, func_to_asp

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--facts', type=str, help=help_messages['facts'])

    parser.add_argument('-q', '--questions', type=str,
                        default='data/CLEVR_v1.0/questions/CLEVR_val_questions.json', help=help_messages['questions'])

    parser.add_argument('-o', '--out', type=str,
                        default='results_out/results.txt', help=help_messages['results_out'])

    parser.add_argument('-t', '--theory', type=str,
                        help='File (.lp) containing additional ASP rules, e.g. for spatial reasoning')

    parser.add_argument('--answer_mode', type=AnswerMode, default=AnswerMode.multiple,
                        choices=list(AnswerMode), help=help_messages['answer_mode'])

    args = parser.parse_args()
    print(f'Command line arguments: {args}')

    # Create output directory and file if not existing
    if not os.path.exists(os.path.dirname(args.out)) and os.path.dirname(args.out):
        try:
            os.makedirs(os.path.dirname(args.out))
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

    # Load facts from specified file
    with open(args.facts) as fp:
        facts = json.load(fp)['facts']

    # Load questions from specified file
    with open(args.questions) as questions_file:
        questions = json.load(questions_file)

    # opt-mode=opt makes clingo use weak constraints (optimization statements in general)
    # opt-mode=ignore makes clingo ignore weak constraints (optimization statements in general)
    optMode = '--opt-mode=opt' if args.answer_mode == AnswerMode.single else '--opt-mode=ignore'

    # Array to hold output content
    lines = []

    for q in tqdm(questions["questions"], desc='Reasoning'):
        q_encoding = func_to_asp(q["program"])

        program = '\n'.join(facts[str(q['image_index'])]) + "\n" + q_encoding

        models = set()
        answer_type = ""

        # Set up clingo
        ctl = clingo.Control(['--models=0', optMode], message_limit=0)
        ctl.add("base", [], program)
        ctl.load(args.theory)

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

            ground_truth = str(q["answer"])

            if ground_truth in guesses:
                answer_type = "correct"
            else:
                # if q['program'][-1]['function'] == "count":
                #    print(f"{q_encoding}\n")
                answer_type = "wrong"
        else:
            guesses = []
            answer_type = "invalid"

        lines.append(f"{q['program'][-1]['function']}|{answer_type}|{guesses}")

    with open(args.out, 'w') as fp:
        fp.write("\n".join(lines))
