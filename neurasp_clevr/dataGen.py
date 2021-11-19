import torch
from tqdm import tqdm

from pytorchyolo.detect import create_data_loader
from pytorchyolo.models import load_model
from pytorchyolo.utils.utils import load_classes, non_max_suppression_neurasp, rescale_boxes, non_max_suppression


def termPath2dataList(termPath, img_size, domain, conf_thres, weights_path):
    """
    @param termPath: a string of the form 'term path' denoting the path to the files represented by term
    """
    factsList = []
    dataList = []
    # Load Yolo network, which is used to generate the facts for bounding boxes and a tensor for each bounding box
    config_path = 'utils/config/yolov3_scene_encoder.cfg'
    yolo = load_model(config_path, weights_path)
    yolo.eval()

    # feed each image into yolo
    term, path = termPath.split(' ')
    dataloader = create_data_loader(path, 1, img_size, 1)

    for _, img in tqdm(dataloader):
        # img = Variable(img.type(torch.FloatTensor))
        img = img.to("cuda")
        with torch.no_grad():
            output = yolo(img)

            facts, dataDic = postProcessing(output, term, domain, conf_thres=conf_thres)
            factsList.append(facts)
            dataList.append(dataDic)
    return factsList, dataList


def postProcessing(output, term, domain, num_classes=96, conf_thres=0.5, nms_thres=0.45):
    facts = ''
    dataDic = {}
    cls_name = load_classes('utils/clevr.names')
    #detections = non_max_suppression_neurasp(output, conf_thres, nms_thres)
    detections = non_max_suppression(output, conf_thres, nms_thres)

    if detections:
        for detection in detections:
            for idx, (x1, y1, x2, y2, cls_conf, cls_pred) in enumerate(detection):
                terms = '{},b{}'.format(term, idx)
                facts += 'box({}, {}, {}, {}, {}).\n'.format(terms, max(0, int(x1)), max(0, int(y1)), max(0, int(x2)), max(0, int(y2)))
                className = '{}'.format(cls_name[int(cls_pred)])
                X = torch.zeros([1, len(domain)], dtype=torch.float64)
                if className in domain:
                    X[0, domain.index(className)] += round(float(cls_conf), 3)
                else:
                    X[0, -1] += round(float(cls_conf), 3)
                dataDic[terms] = X

    #if detections:
    #    for detection in detections:
    #        detection = rescale_boxes(detection, 480, (320, 480))
    #        for idx, prediction in enumerate(detection):
    #
    #            x1, y1, x2, y2 = prediction[0], prediction[1], prediction[2], prediction[3]
    #            terms = '{},b{}'.format(term, idx)
    #            facts += 'box({}, {}, {}, {}, {}).\n'.format(terms, max(0, int(x1)), max(0, int(y1)), max(0, int(x2)), max(0, int(y2)))
    #            # className = '{}'.format(cls_name[int(cls_pred)])
    #            # X = torch.zeros([1, len(domain)], dtype=torch.float64)
    #            x = torch.tensor(prediction[4:])
    #            # if className in domain:
    #            #     X[0, domain.index(className)] += round(float(cls_conf), 3)
    #            # else:
    #            #     X[0, -1] += round(float(cls_conf), 3)
    #            dataDic[terms] = x
    return facts, dataDic
