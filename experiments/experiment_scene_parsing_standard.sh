#for epoch in 25 50 125 200; do # Network training epochs
#  for conf in 25 50; do
#    # Note that sd_factor and fallback value are not used in standard detection
#    /usr/bin/python3.8 parse_scenes.py -m scene_parser/config/yolov3_scene_parser.cfg \
#      -w scene_parser/weights/yolov3_ckpt_${epoch}.pth \
#      -i data/CLEVR_v1.0/images/val \
#      -o facts_standard/facts_standard_${epoch}_conf${conf}.json \
#      --img_size 480 \
#      --conf_thres 0.${conf} \
#      --nms_thres 0.5 \
#      --postprocessing_method standard
#  done
#done

for epoch in 25 50 125 200; do # Network training epochs
  for conf in 25 50; do
    # Note that sd_factor and fallback value are not used in standard detection
    /usr/bin/python3.8 parse_scenes.py -m scene_parser/config/yolov3_scene_parser.cfg \
      -w scene_parser/weights/yolov3_ckpt_${epoch}.pth \
      -i data/CLEVR_v1.0/images/val \
      -o results/facts_standard/facts_standard_${epoch}_conf${conf}.json \
      --img_size 480 \
      --conf_thres 0.${conf} \
      --nms_thres 0.5 \
      --postprocessing_method standard
  done
done
