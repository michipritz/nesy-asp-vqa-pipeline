# A Confidence-Based Interface for Visual Question Answering on CLEVR

This repository contains the implementation of our answer set programming (ASP) based visual question answering (VQA) 
approach for the CLEVR dataset, and we provide the code used to conduct our experiments.

## Requirements

The major software packages we used are:
1. [Python 3.8](https://www.python.org/downloads/)
2. [PyTorch 1.7.1](https://pytorch.org/get-started/previous-versions/)
3. [Clingo 5.5.1](https://potassco.org/clingo/)
4. [CUDA 11.3](https://developer.nvidia.com/cuda-11.3.0-download-archive)

We suggest using [Conda](https://docs.conda.io/en/latest/) for packet management.
Simply install the listed packages and perform the steps described in [Setup](#setup). 
Our experiments where done on a system running Ubuntu 20.04.3 LTS.

## Project Structure

```
PROJECT_NAME
│   README.md
│   mvpp.py                     // NeurASP implementation
│   neurasp.py                  // NeurASP implementation
│   encode_scenes.py            // Scene encoder (Our approach)
│   reason.py                   // Reasoning module (Our approach)
│   neurasp_scene_parser.py     // Scene encoder (NeurASP)
│   infer.py                    // Reasoning module (NeurASP)
│
└───data            // Folder containing CLEVR data, see section Setup
│   │   ...
│
└───experiments     // .py and .sh scripts to automate experiments
│   │   ...
│   
└───neurasp_clevr   // Auxiliary files for NeurASP experiments
│   │   ...
│   
└───pytorchyolo     // YOLOv3 implementation (Object Detection)
│   │   ...
│   
└───results         // Not contained in the repository.
│   │   ...         // Gets created when experiments are executed to store intermediate results.
│   
└───utils           // Contains utilities used during experiments
    │   ...
```

## Setup

You have to add data (CLEVR) and weights for YOLOv3 in order to make the code work.

### Data
    
Create the `data` directory, as shown in section [Project Structure](#project-structure).
Download  [CLEVR dataset](https://cs.stanford.edu/people/jcjohns/clevr/) (v1.0, ~18 GB).
Unzip the data, rename it to `CLEVR_v1.0` and place it into your `data` directory.
The structure should now look like the following:

```
PROJECT_NAME
│   README.md
│   infer.py
│   infer.sh
│   mvpp.py
│   neurasp.py
│   reason.py
│   neurasp_scene_parser.py
│
└───data            // Folder containing CLEVR data, see section Setup
│   │
│   └───images 
│   │   └───test
│   │   └───train
│   │   └───val 
│   │
│   └───questions
│   │   │   CLEVR_test_questions.json
│   │   │   CLEVR_train_questions.json
│   │   │   CLEVR_val_questions.json
│   └───scenes
│   │   │   CLEVR_train_scenes.json
│   │   │   CLEVR_val_scenes.json
│   │   COPYRIGHT.txt
│   │   LICENSE.txt
│   │   README.txt
│
...
```

Some of our experiments where run on a random sample of 15000 questions from the CLEVR val data.
To generate your own sample run `python utils/split_dataset.py`. To reproduce the sample we obtained, use `seed=1234`.
After executing the script you should see a file `data/CLEVR_v1.0/questions/CLEVR_val_sample_15000.json`.

### Weights

Create a directory `utils/weights` and put YOLOv3 weights in there.
You can download the weights we used [here](https://drive.google.com/drive/folders/1rt7X91ZPtNQjgHUN9IB-cCrM43Q9cxgo?usp=sharing).
The name of a weight file must match the schema `yolov3_ckpt_{epoch}.pth`,
where `{epoch}` gets replaced with the number of epochs the model was trained.

## Experiments

All experiments are done in two steps:

1. Generate scene encodings and store them in a file
2. Perform reasoning based on the generated encodings and CLEVR questions

### Our Approach

#### Scene Encoding

Execute `bash experiments/scene_encoding_[det|nondet].sh` to encode the images from
the CLEVR validation dataset using our deterministic/nondeterministic approach. The output
is stored as `.json` file in the directory specified by `-o`. You can also directly use
`scene_encoder.py`.

#### Reasoning

Execute `bash reason_[det|nondet].sh` to perform reasoning on the deterministic/nondeterministic
scene encodings and questions from the CLEVR validation dataset. You can also directly use
`reason.py`. The output is printed to the command line, showing the number of correct, incorrect
and invalid answering attempts as well as the runtime.

### NeurASP

#### Scene Encoding

Simply run `python scene_parser.py` to generate the data/factslists which encode scenes
in a NeurASP compatible way. The lists are stored in `results/neurasp_clevr/scene_encodings_[det|nondet]`.

#### Reasoning

To perform reasoning on scene encodings and questions using NeurASP simply run
`bash experiments/infer.py`. The output is printed to the command line.