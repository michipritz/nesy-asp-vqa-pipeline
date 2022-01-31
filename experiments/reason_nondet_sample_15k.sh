for epoch in 25 50 200; do # Network training epochs
  for conf in 25 50; do    # low and normal conf threshold
    for alpha in 1 2 3 4; do
      printf "\n--------------------------------------------------------------------------------------------\n"
      printf "Epoch: ${epoch} \t Bounding box confidence: ${conf} \t Confidence rate (alpha): ${alpha}"
      printf "\n--------------------------------------------------------------------------------------------\n"

      python reason.py -f results/scene_encodings_nondet_final/scene_encoding_nondet_epoch${epoch}_conf${conf}_alpha${alpha}_k1.json \
        -q data/CLEVR_v1.0/questions/CLEVR_val_sample_15000.json \
        -o results/reasoning_nondet_sample_15k/reasoning_nondet_epoch${epoch}_conf${conf}_alpha${alpha}_k1.txt \
        -t utils/theory.lp \
        --answer_mode single
    done
  done
done