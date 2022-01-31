import argparse
import errno
import json
import os
from datetime import datetime

from pytorchyolo.detect import create_data_loader
from utils.scene_encoder import SceneEncoder
from utils.utils import help_messages, PostprocessingMethod

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--model', type=str, default='utils/config/yolov3_scene_encoder.cfg', help=help_messages['model'])
    parser.add_argument('-w', '--weights', type=str, required=True, help=help_messages['weights'])
    parser.add_argument('-i', '--images', type=str, default='data/CLEVR_v1.0/images/val', help=help_messages['images'])
    parser.add_argument('--img_size', type=int, default=480, help=help_messages['img_size'])
    parser.add_argument('-o', '--out', type=str, required=True, help=help_messages['facts_out'])
    parser.add_argument('--bounding_box_thres', type=float, default=0.5, help=help_messages['bounding_box_thres'])
    parser.add_argument('--nms_thres', type=float, default=0.5, help=help_messages['nms_thres'])
    parser.add_argument('--alpha', type=float, default=1.0, help=help_messages['alpha'])
    parser.add_argument('-k', '--k', type=int, default=1, help=help_messages['k'])
    parser.add_argument('--batch_size', type=int, default=1, help=help_messages['batch_size'])
    parser.add_argument('--n_cpu', type=int, default=1, help=help_messages['n_cpu'])
    parser.add_argument('--postprocessing_method', type=PostprocessingMethod,
                        default=PostprocessingMethod.non_deterministic, choices=list(PostprocessingMethod),
                        help=help_messages['postprocessing_method'])
    args = parser.parse_args()
    print(f'Configuration: {args}')

    # Create output directory and file (if not existing)
    if not os.path.exists(os.path.dirname(args.out)) and os.path.dirname(args.out):
        try:
            os.makedirs(os.path.dirname(args.out))
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

    # Write configuration to the output file
    with open(args.out, 'w') as out_fp:
        meta = {
            'meta': {
                'creation_time': str(datetime.now()),
                'model': args.model,
                'weights': args.weights,
                'images': args.images,
                'img_size': args.img_size,
                'bounding_box_thres': args.bounding_box_thres,
                'nms_thres': args.nms_thres,
                'alpha': args.alpha,
                'k': args.k,
                'postprocessing': str(args.postprocessing_method)
            }
        }
        json.dump(meta, out_fp, indent=4)

    ############
    # Dataloader
    ############
    dataloader = create_data_loader(args.images, args.batch_size, args.img_size, args.n_cpu)

    #########################
    # Scene Encoder
    #########################
    sceneParser = SceneEncoder(config=args.model,
                               weights=args.weights,
                               images=args.images,
                               img_size=args.img_size,
                               facts_out=args.out,
                               bounding_box_thres=args.bounding_box_thres,
                               nms_thres=args.nms_thres,
                               alpha=args.alpha,
                               k=args.k,
                               postprocessing_method=args.postprocessing_method)

    ###############
    # Encode images
    ###############
    facts, conf_mean, conf_sd = sceneParser.parse(data=dataloader)

    # Write encoding to the output file
    with open(args.out, 'r') as out_fp:
        out_json = json.load(out_fp)

    # Add computed confidence mean and std to configuration data in the output file
    out_json['meta']['conf_mean'] = conf_mean
    out_json['meta']['conf_sd'] = conf_sd

    # Add facts to output file
    out_json['facts'] = facts

    with open(args.out, 'w') as out_fp:
        json.dump(out_json, out_fp, indent=4)
