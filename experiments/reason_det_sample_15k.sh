for epoch in 25 50 200; do # Network training epochs
  for conf in 25 50; do # low and normal conf threshold
    /usr/bin/python3.8 reason.py -f results/scene_encodings_det/scene_encoding_det_epoch${epoch}_conf${conf}.json \
      -q data/CLEVR_v1.0/questions/CLEVR_val_sample_15000.json \
      -o results/reasoning_det_sample_15k/reasoning_det_epoch${epoch}_conf${conf}.txt \
      -t utils/theory.lp \
      --answer_mode single
  done
done
