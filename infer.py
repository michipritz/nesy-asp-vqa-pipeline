import json
import random
import sys

import torch
from clingo.symbol import SymbolType
from tqdm import tqdm

from neurasp import NeurASP
from neurasp_clevr.network import Net
from utils.question_encoder import encode_question

with open("data/CLEVR_v1.0/questions/CLEVR_val_sample_15000.json") as fp:
    questions = json.load(fp)["questions"]

dprogram = r'''
    nn(label(1,I,B), [obj(B,cylinder,large,gray,metal,X1,Y1,X2,Y2), obj(B,sphere,large,gray,metal,X1,Y1,X2,Y2), obj(B,cube,large,gray,metal,X1,Y1,X2,Y2), obj(B,cylinder,large,gray,rubber,X1,Y1,X2,Y2), obj(B,sphere,large,gray,rubber,X1,Y1,X2,Y2), obj(B,cube,large,gray,rubber,X1,Y1,X2,Y2), obj(B,cylinder,large,blue,metal,X1,Y1,X2,Y2), obj(B,sphere,large,blue,metal,X1,Y1,X2,Y2), obj(B,cube,large,blue,metal,X1,Y1,X2,Y2), obj(B,cylinder,large,blue,rubber,X1,Y1,X2,Y2), obj(B,sphere,large,blue,rubber,X1,Y1,X2,Y2), obj(B,cube,large,blue,rubber,X1,Y1,X2,Y2), obj(B,cylinder,large,brown,metal,X1,Y1,X2,Y2), obj(B,sphere,large,brown,metal,X1,Y1,X2,Y2), obj(B,cube,large,brown,metal,X1,Y1,X2,Y2), obj(B,cylinder,large,brown,rubber,X1,Y1,X2,Y2), obj(B,sphere,large,brown,rubber,X1,Y1,X2,Y2), obj(B,cube,large,brown,rubber,X1,Y1,X2,Y2), obj(B,cylinder,large,yellow,metal,X1,Y1,X2,Y2), obj(B,sphere,large,yellow,metal,X1,Y1,X2,Y2), obj(B,cube,large,yellow,metal,X1,Y1,X2,Y2), obj(B,cylinder,large,yellow,rubber,X1,Y1,X2,Y2), obj(B,sphere,large,yellow,rubber,X1,Y1,X2,Y2), obj(B,cube,large,yellow,rubber,X1,Y1,X2,Y2), obj(B,cylinder,large,red,metal,X1,Y1,X2,Y2), obj(B,sphere,large,red,metal,X1,Y1,X2,Y2), obj(B,cube,large,red,metal,X1,Y1,X2,Y2), obj(B,cylinder,large,red,rubber,X1,Y1,X2,Y2), obj(B,sphere,large,red,rubber,X1,Y1,X2,Y2), obj(B,cube,large,red,rubber,X1,Y1,X2,Y2), obj(B,cylinder,large,green,metal,X1,Y1,X2,Y2), obj(B,sphere,large,green,metal,X1,Y1,X2,Y2), obj(B,cube,large,green,metal,X1,Y1,X2,Y2), obj(B,cylinder,large,green,rubber,X1,Y1,X2,Y2), obj(B,sphere,large,green,rubber,X1,Y1,X2,Y2), obj(B,cube,large,green,rubber,X1,Y1,X2,Y2), obj(B,cylinder,large,purple,metal,X1,Y1,X2,Y2), obj(B,sphere,large,purple,metal,X1,Y1,X2,Y2), obj(B,cube,large,purple,metal,X1,Y1,X2,Y2), obj(B,cylinder,large,purple,rubber,X1,Y1,X2,Y2), obj(B,sphere,large,purple,rubber,X1,Y1,X2,Y2), obj(B,cube,large,purple,rubber,X1,Y1,X2,Y2), obj(B,cylinder,large,cyan,metal,X1,Y1,X2,Y2), obj(B,sphere,large,cyan,metal,X1,Y1,X2,Y2), obj(B,cube,large,cyan,metal,X1,Y1,X2,Y2), obj(B,cylinder,large,cyan,rubber,X1,Y1,X2,Y2), obj(B,sphere,large,cyan,rubber,X1,Y1,X2,Y2), obj(B,cube,large,cyan,rubber,X1,Y1,X2,Y2), obj(B,cylinder,small,gray,metal,X1,Y1,X2,Y2), obj(B,sphere,small,gray,metal,X1,Y1,X2,Y2), obj(B,cube,small,gray,metal,X1,Y1,X2,Y2), obj(B,cylinder,small,gray,rubber,X1,Y1,X2,Y2), obj(B,sphere,small,gray,rubber,X1,Y1,X2,Y2), obj(B,cube,small,gray,rubber,X1,Y1,X2,Y2), obj(B,cylinder,small,blue,metal,X1,Y1,X2,Y2), obj(B,sphere,small,blue,metal,X1,Y1,X2,Y2), obj(B,cube,small,blue,metal,X1,Y1,X2,Y2), obj(B,cylinder,small,blue,rubber,X1,Y1,X2,Y2), obj(B,sphere,small,blue,rubber,X1,Y1,X2,Y2), obj(B,cube,small,blue,rubber,X1,Y1,X2,Y2), obj(B,cylinder,small,brown,metal,X1,Y1,X2,Y2), obj(B,sphere,small,brown,metal,X1,Y1,X2,Y2), obj(B,cube,small,brown,metal,X1,Y1,X2,Y2), obj(B,cylinder,small,brown,rubber,X1,Y1,X2,Y2), obj(B,sphere,small,brown,rubber,X1,Y1,X2,Y2), obj(B,cube,small,brown,rubber,X1,Y1,X2,Y2), obj(B,cylinder,small,yellow,metal,X1,Y1,X2,Y2), obj(B,sphere,small,yellow,metal,X1,Y1,X2,Y2), obj(B,cube,small,yellow,metal,X1,Y1,X2,Y2), obj(B,cylinder,small,yellow,rubber,X1,Y1,X2,Y2), obj(B,sphere,small,yellow,rubber,X1,Y1,X2,Y2), obj(B,cube,small,yellow,rubber,X1,Y1,X2,Y2), obj(B,cylinder,small,red,metal,X1,Y1,X2,Y2), obj(B,sphere,small,red,metal,X1,Y1,X2,Y2), obj(B,cube,small,red,metal,X1,Y1,X2,Y2), obj(B,cylinder,small,red,rubber,X1,Y1,X2,Y2), obj(B,sphere,small,red,rubber,X1,Y1,X2,Y2), obj(B,cube,small,red,rubber,X1,Y1,X2,Y2), obj(B,cylinder,small,green,metal,X1,Y1,X2,Y2), obj(B,sphere,small,green,metal,X1,Y1,X2,Y2), obj(B,cube,small,green,metal,X1,Y1,X2,Y2), obj(B,cylinder,small,green,rubber,X1,Y1,X2,Y2), obj(B,sphere,small,green,rubber,X1,Y1,X2,Y2), obj(B,cube,small,green,rubber,X1,Y1,X2,Y2), obj(B,cylinder,small,purple,metal,X1,Y1,X2,Y2), obj(B,sphere,small,purple,metal,X1,Y1,X2,Y2), obj(B,cube,small,purple,metal,X1,Y1,X2,Y2), obj(B,cylinder,small,purple,rubber,X1,Y1,X2,Y2), obj(B,sphere,small,purple,rubber,X1,Y1,X2,Y2), obj(B,cube,small,purple,rubber,X1,Y1,X2,Y2), obj(B,cylinder,small,cyan,metal,X1,Y1,X2,Y2), obj(B,sphere,small,cyan,metal,X1,Y1,X2,Y2), obj(B,cube,small,cyan,metal,X1,Y1,X2,Y2), obj(B,cylinder,small,cyan,rubber,X1,Y1,X2,Y2), obj(B,sphere,small,cyan,rubber,X1,Y1,X2,Y2), obj(B,cube,small,cyan,rubber,X1,Y1,X2,Y2)]) :- box(I,B,X1,Y1,X2,Y2).
    '''

with open("utils/theory_neurasp.lp", "r") as fp:
    theory = fp.read()

epoch = sys.argv[1]
conf = sys.argv[2]
directory = sys.argv[3]

questionCounter = 1
questionsTotal = len(questions)
correct = 0
incorrect = 0
invalid = 0
total = 0

factsList = torch.load(f"results/neurasp_clevr/{directory}/factlist_epoch{epoch}_conf{conf}.pt")
dataList = torch.load(f"results/neurasp_clevr/{directory}/datalist_epoch{epoch}_conf{conf}.pt")

print(f"\nEpoch: {epoch}, Confidence: {conf}, Directory: {directory}")

for q in tqdm(questions):
    aspProgram = encode_question(q["program"])
    aspProgram += theory

    m = Net()
    nnMapping = {'label': m}

    facts = factsList[q['image_index']]
    NeurASPobj = NeurASP(dprogram + facts, nnMapping, optimizers=None)
    model_candidates = NeurASPobj.infer(dataDic=dataList[q['image_index']], obs='', mvpp=aspProgram + facts)
    answer_candidates = set()

    if len(model_candidates) > 0:
        val = model_candidates[-1][0].arguments[0]
        if val.type == SymbolType.Number:
            val = str(val.number)
        elif val.type == SymbolType.Function:
            if val.name in ['true', 'false']:
                val = 'no' if val.name == 'false' else 'yes'
            else:
                val = val.name
        answer_candidates.add(val)

    # Check if computed answer(s) and ground truth are the same
    if answer_candidates:
        # Break ties by picking a random answer
        # Occurs if there are multiple optimal answer sets, which can happen due to reduced precision introduced by rounding)
        guess = [random.choice(list(answer_candidates))]

        assert len(guess) == 1

        ground_truth = str(q["answer"])

        if ground_truth in guess:
            correct += 1
        else:
            incorrect += 1
    else:
        invalid += 1

    total += 1

print(f"Correct: {correct}/{total} ({correct / total * 100:.2f})")
print(f"Incorrect: {incorrect}/{total} ({incorrect / total * 100:.2f})")
print(f"Invalid: {invalid}/{total} ({invalid / total * 100:.2f})")
