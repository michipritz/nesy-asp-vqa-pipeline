import torch
import re
import json
from tqdm import tqdm

from pytorchyolo.detect import create_data_loader
from pytorchyolo.models import load_model
from pytorchyolo.utils.utils import load_classes, non_max_suppression_neurasp, rescale_boxes, non_max_suppression

def termPath2dataList(termPath, img_size, domain, epoch, conf, k):
    """
    @param termPath: a string of the form 'term path' denoting the path to the files represented by term
    """
    factsDict = {}
    # Load Yolo network, which is used to generate the facts for bounding boxes and a tensor for each bounding box
    config_path = './utils/config/yolov3_scene_encoder.cfg'
    weights_path = './utils/weights/yolov3_ckpt_'+epoch+'.pth'
    yolo = load_model(config_path, weights_path)
    yolo.eval()

    # feed each image into yolo
    term, path = termPath.split(' ')
    dataloader = create_data_loader(path, 1, img_size, 1)
    for i, img in tqdm(dataloader):
        image_filename = i[0].split('/')[3]
        img = img.to("cuda")
        with torch.no_grad():
            output = yolo(img)

            facts = postProcessing(output, term, domain, k = k, conf_thres=conf)
            factsDict[image_filename] = facts

    return factsDict


def postProcessing(output, term, domain, k = 0, num_classes=96, conf_thres=0.5, nms_thres=0.4):
    prob_facts = ''
    detections = non_max_suppression_neurasp(output, conf_thres, nms_thres)

    if k == 0:
        k = num_classes
    if detections:
        for detection in detections:
            for id, object in enumerate(detection):
                b_box = []
                b_box = rescale_boxes([object[0].item(),object[1].item(),object[2].item(),object[3].item()], 480, (320, 480))

                probs = object[4:].tolist()
                probs_dict = list_2_dict(probs)
                probs_dict = dict(sorted(probs_dict.items(), key=lambda item: item[1], reverse=True))
                probs.sort(reverse=True)
                probs = normalize(probs[:k])
                keys = list(probs_dict.keys())

                for i in range(k):
                    obj_class = decode_class_id(keys[i])
                    prob = probs[i]
                    prob_facts += '{}::obj(0, {}, {}, {}, {}, {}, {}, {}, {}, {});'.format(prob,id,obj_class[0],obj_class[1],obj_class[2],obj_class[3],b_box[0],b_box[1],b_box[2],b_box[3])
                prob_facts = prob_facts[:-1]
                prob_facts += '.\n'
                
    return prob_facts

def normalize(lst):
    norm = [float(i)/sum(lst) for i in lst]
    return norm

def list_2_dict(lst):
    dict = {}
    for i in range(len(lst)):
        dict[i] = lst[i]
    return dict

def decode_class_id(category_id):
    with open('./pytorchyolo/utils/mappings/id_to_category.json', 'r') as mapping_file:
        category_str = json.load(mapping_file)[str(int(category_id))]

    properties_s = re.findall('[A-Z][^A-Z]*', category_str)

    size_s = properties_s[0]
    color_s = properties_s[1]
    material_s = properties_s[2]
    shape_s = properties_s[3]

    with open('./pytorchyolo/utils/mappings/properties_short_to_long.json', 'r') as mapping_file:
        properties_mapping = json.load(mapping_file)
        size_l = properties_mapping['sizes'][size_s]
        color_l = properties_mapping['colors'][color_s]
        material_l = properties_mapping['materials'][material_s]
        shape_l = properties_mapping['shapes'][shape_s]

    return size_l, color_l, material_l, shape_l


def rescale_boxes(boxes, current_dim, original_shape):
    """
    Rescales bounding boxes to the original shape
    """
    orig_h, orig_w = original_shape

    # The amount of padding that was added
    pad_x = max(orig_h - orig_w, 0) * (current_dim / max(original_shape))
    pad_y = max(orig_w - orig_h, 0) * (current_dim / max(original_shape))

    # Image height and width after padding is removed
    unpad_h = current_dim - pad_y
    unpad_w = current_dim - pad_x

    # Rescale bounding boxes to dimension of original image
    boxes[0] = round(((boxes[0] - pad_x // 2) / unpad_w) * orig_w,2)
    boxes[1] = round(((boxes[1] - pad_y // 2) / unpad_h) * orig_h,2)
    boxes[2] = round(((boxes[2] - pad_x // 2) / unpad_w) * orig_w,2)
    boxes[3] = round(((boxes[3] - pad_y // 2) / unpad_h) * orig_h,2)
    return boxes


def func_to_asp(program):
    # Holds action sequence
    action_sequence = []
    # Time
    t = 0

    # Iterate over functional program and translate every basic function into an action atom
    for i, func in enumerate(program):
        t = i
        func_name = func["function"]
        if func_name in func_type["unary"]:
            if func_name == "scene":
                action_sequence.append(actions[func_name].format(T=t, T1=0))
            else:
                action_sequence.append(actions[func_name].format(T=t, T1=func["inputs"][0] + 1))
            # print(f"{func}, {action_sequence[-1]}")
        elif func_name in func_type["binary_val"]:
            val = func["value_inputs"][0]
            action_sequence.append(actions[func_name].format(T=t, T1=func["inputs"][0] + 1, val=val))
            # print(f"{func}, {action_sequence[-1]}")
        elif func_name in func_type["binary_in"]:
            t1 = func["inputs"][0]
            t2 = func["inputs"][1]
            if func_name in ["union", "intersect"]:
                action_sequence.append(actions[func_name].format(T=t, T1=t1+1, T2=t2+1))
            else:
                action_sequence.append(actions[func_name].format(T=t, T1=t1, T2=t2))
            # print(f"{func}, {action_sequence[-1]}")
        else:
            print("Unknown function name: " + func_name)

    # Add end atom
    action_sequence.append(f"end({t}).")

    # Return action sequence as string
    return "\n".join(action_sequence)
