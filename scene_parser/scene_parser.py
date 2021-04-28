from pytorchyolo import detect, models


# Good to know:
# - Weight must be downloaded separately, due to big filesize.
class SceneParser:
    def __init__(self):
        self.model = models.load_model('./config/yolov3_scene_parser.cfg', './weights/yolov3_scene_parser.pth')
        self.model.eval()

    def parse(self):
        print('parse scene')
