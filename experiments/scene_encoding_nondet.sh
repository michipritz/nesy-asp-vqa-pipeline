for epoch in 25 50 200; do # Network training epochs
  for conf in 25 50; do
    /usr/bin/python3.8 encode_scenes.py -m utils/config/yolov3_scene_encoder.cfg \
      -w utils/weights/yolov3_ckpt_${epoch}.pth \
      -i data/CLEVR_v1.0/images/val \
      -o results/scene_encodings_nondet/scene_encoding_nondet_epoch${epoch}_conf${conf}.json \
      --img_size 480 \
      --bounding_box_thres 0.${conf} \
      --nms_thres 0.5 \
      --alpha 1 \
      --k 2 \
      --postprocessing_method non_deterministic
  done
done
