import random
import json
import glob
import shutil
import os
import re

# Take a sample of size n from CLEVR validation questions
# Copy images referred to in sample from src_dir to dst_dir
n = 15000
src_dir = "CLEVR_v1.0/images/val"
dst_dir = f"CLEVR_v1.0/images/val_sample_{n}"
seed = 1234

with open("data/CLEVR_v1.0/questions/CLEVR_val_questions.json", "r") as fp:
    questions = json.load(fp)["questions"]

random.seed(seed)
sample = random.sample(questions, n)

with open(f"data/CLEVR_v1.0/questions/CLEVR_val_sample_{n}.json", "w") as fp:
    json.dump(sample, fp)
