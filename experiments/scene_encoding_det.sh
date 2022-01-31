for epoch in 25 50 200; do # Network training epochs
  for conf in 25 50; do # Bounding box confidence threshold (0.25, 0.5)
    # Note that alpha and k value are not used in standard detection
    /usr/bin/python3.8 encode_scenes.py -m utils/config/yolov3_scene_encoder.cfg \
      -w utils/weights/yolov3_softmax_ckpt_${epoch}.pth \
      -i data/CLEVR_v1.0/images/val \
      -o results/scene_encodings_det_softmax/scene_encoding_det_softmax_epoch${epoch}_conf${conf}.json \
      --img_size 480 \
      --bounding_box_thres 0.${conf} \
      --nms_thres 0.5 \
      --postprocessing_method deterministic
  done
done
