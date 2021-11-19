import os
import sys
import time

import torch

sys.path.append('../')

from neurasp_clevr.dataGen import termPath2dataList

termPath = f'img ./data/CLEVR_v1.0/images/val'
img_size = 480

domain = ['LaGraMeCy', 'LaGraMeSp', 'LaGraMeCu', 'LaGraRuCy', 'LaGraRuSp', 'LaGraRuCu', 'LaBlMeCy', 'LaBlMeSp', 'LaBlMeCu', 'LaBlRuCy',
          'LaBlRuSp', 'LaBlRuCu', 'LaBrMeCy', 'LaBrMeSp', 'LaBrMeCu', 'LaBrRuCy', 'LaBrRuSp', 'LaBrRuCu', 'LaYeMeCy', 'LaYeMeSp',
          'LaYeMeCu', 'LaYeRuCy', 'LaYeRuSp', 'LaYeRuCu', 'LaReMeCy', 'LaReMeSp', 'LaReMeCu', 'LaReRuCy', 'LaReRuSp', 'LaReRuCu',
          'LaGreMeCy', 'LaGreMeSp', 'LaGreMeCu', 'LaGreRuCy', 'LaGreRuSp', 'LaGreRuCu', 'LaPuMeCy', 'LaPuMeSp', 'LaPuMeCu', 'LaPuRuCy',
          'LaPuRuSp', 'LaPuRuCu', 'LaCyMeCy', 'LaCyMeSp', 'LaCyMeCu', 'LaCyRuCy', 'LaCyRuSp', 'LaCyRuCu', 'SmGraMeCy', 'SmGraMeSp',
          'SmGraMeCu', 'SmGraRuCy', 'SmGraRuSp', 'SmGraRuCu', 'SmBlMeCy', 'SmBlMeSp', 'SmBlMeCu', 'SmBlRuCy', 'SmBlRuSp', 'SmBlRuCu',
          'SmBrMeCy', 'SmBrMeSp', 'SmBrMeCu', 'SmBrRuCy', 'SmBrRuSp', 'SmBrRuCu', 'SmYeMeCy', 'SmYeMeSp', 'SmYeMeCu', 'SmYeRuCy',
          'SmYeRuSp', 'SmYeRuCu', 'SmReMeCy', 'SmReMeSp', 'SmReMeCu', 'SmReRuCy', 'SmReRuSp', 'SmReRuCu', 'SmGreMeCy', 'SmGreMeSp',
          'SmGreMeCu', 'SmGreRuCy', 'SmGreRuSp', 'SmGreRuCu', 'SmPuMeCy', 'SmPuMeSp', 'SmPuMeCu', 'SmPuRuCy', 'SmPuRuSp', 'SmPuRuCu',
          'SmCyMeCy', 'SmCyMeSp', 'SmCyMeCu', 'SmCyRuCy', 'SmCyRuSp', 'SmCyRuCu']

encoding_type = ["best", "all"]

for enc_type in encoding_type:
    # Create output directory
    out = "results/neurasp_clevr/scene_encodings_det" if enc_type == "best" else "results/neurasp_clevr/scene_encodings_nondet"
    if not os.path.exists(out):
        os.makedirs(out)

    epochs = [25, 50, 200]
    conf_thres = [0.25, 0.50]
    for epoch in epochs:
        for conf in conf_thres:
            factsList, dataList = termPath2dataList(termPath, img_size, domain, conf_thres=conf,
                                                    weights_path=f"utils/weights/yolov3_ckpt_{epoch}.pth")

            print(f"Epoch: {epoch}, Confidence: {conf}")
            torch.save(dataList, f"{out}/datalist_epoch{epoch}_conf{conf * 100:.0f}.pt")
            torch.save(factsList, f"{out}/factlist_epoch{epoch}_conf{conf * 100:.0f}.pt")
