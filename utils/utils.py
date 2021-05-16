from clingo.symbol import SymbolType


def print_stats(total, correct, wrong, invalid):
    correct_rel = correct / total * 100
    wrong_rel = wrong / total * 100
    invalid_rel = invalid / total * 100

    print("Questions total: \t{:7d}".format(total))
    print("Questions correct: \t{:7d} ({:4.2f}%)".format(correct, correct_rel))
    print("Questions wrong: \t{:7d} ({:4.2f}%)".format(wrong, wrong_rel))
    print("Questions invalid: \t{:7d} ({:4.2f}%)".format(invalid, invalid_rel))


def print_question_info(q_id, q_natural, q_true_ans, q_given_ans, q_family_id):
    print('Image ID: {}'.format(str(q_id)))
    print('Question: {}'.format(str(q_natural)))
    print('Question family ID: {}'.format(str(q_family_id)))
    print('Expected Answer: {}'.format(str(q_true_ans)))
    print('Given Answer: {}\n'.format(str(q_given_ans)))


def get_guesses_from_models(models):
    guesses = []
    for model in models:
        for atom in model:
            if atom.match('ans', 1):
                val = atom.arguments[0]
                if val.type == SymbolType.Number:
                    val = str(val.number)
                elif val.type == SymbolType.Function:
                    if val.name in ['true', 'false']:
                        val = 'no' if val.name == 'false' else 'yes'
                    else:
                        val = val.name

                guesses.append(val)
                break
    return guesses
