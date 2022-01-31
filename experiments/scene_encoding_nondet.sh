for epoch in 25 50 200; do # Network training epochs
  for conf in 25 50; do
    for alpha in 0 1 2; do
      python encode_scenes.py -m utils/config/yolov3_scene_encoder.cfg \
        -w utils/weights/yolov3_ckpt_${epoch}.pth \
        -i data/CLEVR_v1.0/images/val \
        -o results/scene_encodings_nondet_k1/scene_encoding_nondet_epoch${epoch}_conf${conf}_alpha${alpha}5_k1.json \
        --img_size 480 \
        --bounding_box_thres 0.${conf} \
        --nms_thres 0.5 \
        --alpha ${alpha}.5 \
        --k 1 \
        --postprocessing_method non_deterministic
    done
  done
done
