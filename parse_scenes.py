import argparse
import errno
import json
import os
from datetime import datetime

from pytorchyolo.detect import create_data_loader
from scene_parser import SceneParser
from utils import help_messages, PostprocessingMethod

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-m', '--model', type=str,
                        default='scene_parser/config/yolov3_scene_parser.cfg', help=help_messages['model'])

    parser.add_argument('-w', '--weights', type=str,
                        default='scene_parser/weights/yolov3_ckpt_150.pth', help=help_messages['weights'])

    parser.add_argument('-i', '--images', type=str,
                        default='data/CLEVR_v1.0/images/val', help=help_messages['images'])

    parser.add_argument('--img_size', type=int,
                        default=480, help=help_messages['img_size'])

    parser.add_argument('-o', '--out', type=str,
                        default='facts_out/facts.json', help=help_messages['facts_out'])

    parser.add_argument('--conf_thres', type=float,
                        default=0.5, help=help_messages['conf_thres'])

    parser.add_argument('--nms_thres', type=float,
                        default=0.5, help=help_messages['nms_thres'])

    parser.add_argument('--sd_factor', type=float,
                        default=1.0, help=help_messages['sd_factor'])

    parser.add_argument('--fallback_value', type=int,
                        default=2, help=help_messages['fallback_value'])

    parser.add_argument('--postprocessing_method', type=PostprocessingMethod,
                        default=PostprocessingMethod.enhanced, choices=list(PostprocessingMethod),
                        help=help_messages['postprocessing_method'])

    parser.add_argument('--batch_size', type=int, default=4, help=help_messages['batch_size'])

    parser.add_argument('--n_cpu', type=int, default=4, help=help_messages['n_cpu'])

    args = parser.parse_args()
    print(f'Command line arguments: {args}')

    # Create output directory and file if not existing
    if not os.path.exists(os.path.dirname(args.out)) and os.path.dirname(args.out):
        try:
            os.makedirs(os.path.dirname(args.out))
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

    # Write argument infos to the output file
    with open(args.out, 'w') as out_fp:
        info = {
            'info': {
                'creation_time': str(datetime.now()),
                'model': args.model,
                'weights': args.weights,
                'images': args.images,
                'img_size': args.img_size,
                'conf_thres': args.conf_thres,
                'nms_thres': args.nms_thres,
                'sd_factor': args.sd_factor,
                'fallback_value': args.fallback_value,
                'postprocessing': str(args.postprocessing_method)
            }
        }
        json.dump(info, out_fp, indent=4)

    # Initialize dataloader with command line arguments
    dataloader = create_data_loader(args.images, args.batch_size, args.img_size, args.n_cpu)

    # Initialize scene parser with command line arguments
    sceneParser = SceneParser(config=args.model,
                              weights=args.weights,
                              images=args.images,
                              img_size=args.img_size,
                              facts_out=args.out,
                              conf_thres=args.conf_thres,
                              nms_thres=args.nms_thres,
                              sd_factor=args.sd_factor,
                              fallback_value=args.fallback_value,
                              postprocessing_method=args.postprocessing_method)

    # Parse images provided by dataloader
    facts, conf_mean, conf_sd = sceneParser.parse(data=dataloader)

    # Add facts and stats from scene parsing to output file
    with open(args.out, 'r') as out_fp:
        out_json = json.load(out_fp)

    out_json['info']['conf_mean'] = conf_mean
    out_json['info']['conf_sd'] = conf_sd
    out_json['facts'] = facts

    with open(args.out, 'w') as out_fp:
        json.dump(out_json, out_fp, indent=4)
