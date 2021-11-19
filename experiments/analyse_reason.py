import argparse

if __name__ == "__main__":
    # Command line argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, help='Path to the .txt file containing the reasoning results')
    args = parser.parse_args()
    print(f'Command line arguments: {args}')

    # for filename in os.listdir(args.input):
    stats = {"correct": 0, "wrong": 0, "invalid": 0, "total": 0}

    with open(f"{args.input}", "r") as fp:
        for i, line in enumerate(fp):
            line = line.strip()
            q_type, answer_type, answers = line.split("|")

            if q_type not in stats:
                stats[q_type] = {"correct": 0, "wrong": 0, "invalid": 0, "total": 0}

            stats["total"] += 1
            stats[q_type]["total"] += 1

            if answer_type == "correct":
                stats["correct"] += 1
                stats[q_type]["correct"] += 1
            elif answer_type == "wrong":
                stats["wrong"] += 1
                stats[q_type]["wrong"] += 1
            elif answer_type == "invalid":
                stats["invalid"] += 1
                stats[q_type]["invalid"] += 1
            else:
                print(f"Unknown answer type: {answer_type}")
                exit()

    print(f"Evaluation results for {args.input}")
    print(f"Total correct: {stats['correct']} ({stats['correct'] / stats['total'] * 100:.2f}%)")
    print(f"Total wrong: {stats['wrong']} ({stats['wrong'] / stats['total'] * 100:.2f}%)")
    print(f"Total invalid: {stats['invalid']} ({stats['invalid'] / stats['total'] * 100:.2f}%)\n")
