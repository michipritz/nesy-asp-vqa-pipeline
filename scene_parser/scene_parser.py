import os.path
import json
from pytorchyolo import detect, models
from scene_parser.utils.utils import predictions_to_asp_facts, get_confidence_mean_and_sd


# - Weight must be downloaded separately, due to big filesize.
class SceneParser:
    def __init__(self,
                 config='./scene_parser/config/yolov3_scene_parser.cfg',
                 weights='./scene_parser/weights/yolov3_scene_parser.pth',
                 data='./data/CLEVR_v1.0/images/val',
                 img_size=416):
        self.dataPath = data
        self.configPath = config
        self.weightsPath = weights
        self.model = models.load_model(config, weights)
        self.dataloader = detect._create_data_loader(data, 16, img_size, 8)

    def parse(self, img_size=480, conf_threshold=0.25, nms_threshold=0.45, facts='./scene_parser/asp_facts.json',
              sd_factor=2,
              backup_value=2):
        if os.path.isfile(facts):
            with open(facts, 'r') as fp:
                asp_facts = json.load(fp)
        else:
            predictions, _ = detect.detect(
                self.model,
                self.dataloader,
                '.',
                img_size,
                conf_threshold,
                nms_threshold
            )

            asp_facts = predictions_to_asp_facts(predictions, sd_factor=sd_factor, backup_value=backup_value)

            with open(facts, 'w') as fp:
                asp_facts['info']['sd_factor'] = sd_factor
                asp_facts['info']['backup_value'] = backup_value
                asp_facts['info']['img_size'] = img_size
                asp_facts['info']['conf_threshold'] = conf_threshold
                asp_facts['info']['nms_threshold'] = nms_threshold
                asp_facts['info']['data'] = self.dataPath
                asp_facts['info']['weights'] = self.weightsPath
                asp_facts['info']['config'] = self.configPath
                json.dump(asp_facts, fp, indent=4)

        return asp_facts
