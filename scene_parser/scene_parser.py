from PIL import Image
import numpy as np
from pytorchyolo import detect, models
from utils.utils import predictions_to_asp_facts


# - Weight must be downloaded separately, due to big filesize.
class SceneParser:
    def __init__(self):
        self.model = models.load_model('./scene_parser/config/yolov3_scene_parser.cfg',
                                       './scene_parser/weights/yolov3_scene_parser.pth')

    def parse(self, images, img_size=480, conf_threshold=0.7):
        predictions = detect.detect_image(self.model, images, img_size=img_size, conf_thres=conf_threshold)
        return predictions_to_asp_facts(predictions), predictions
