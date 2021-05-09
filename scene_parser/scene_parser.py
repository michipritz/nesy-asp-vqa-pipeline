from PIL import Image
import numpy as np
import os.path
import json
from pytorchyolo import detect, models
from scene_parser.utils.utils import predictions_to_asp_facts


# - Weight must be downloaded separately, due to big filesize.
class SceneParser:
    def __init__(self):
        self.model = models.load_model('./scene_parser/config/yolov3_scene_parser.cfg',
                                       './scene_parser/weights/yolov3_scene_parser.pth')
        self.dataloader = detect._create_data_loader(
            '/home/michael/PycharmProjects/neurasp_clevr/data/CLEVR_v1.0/images/val', 16, 480, 8)

    def parse(self, img_size=480, conf_threshold=0.7):
        # TODO: Refactor s.t. parser can process image batches
        if os.path.isfile('./scene_parser/asp_facts.json'):
            with open('./scene_parser/asp_facts.json', 'r') as fp:
                asp_facts = json.load(fp)
        else:
            predictions, _ = detect.detect(
                self.model,
                self.dataloader,
                '/home/michael/PycharmProjects/neurasp_clevr/scene_parser',
                img_size,
                conf_threshold,
                0.5
            )

            asp_facts = predictions_to_asp_facts(predictions)

            with open('./scene_parser/asp_facts.json', 'w') as fp:
                json.dump(asp_facts, fp, sort_keys=True, indent=4)

        return asp_facts
