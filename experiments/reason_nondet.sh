for epoch in 25 50 200; do # Network training epochs
  for conf in 25 50; do # low and normal conf threshold
    for alpha in 0 1; do
      printf "\n--------------------------------------------------------------------------------------------\n"
      printf "Epoch: ${epoch} \t Bounding box confidence: 0.${conf} \t Confidence rate (alpha): ${alpha}.5"
      printf "\n--------------------------------------------------------------------------------------------\n"

      python reason.py -f results/scene_encodings_nondet_k1/scene_encoding_nondet_epoch${epoch}_conf${conf}_alpha${alpha}5_k1.json \
        -q data/CLEVR_v1.0/questions/CLEVR_val_questions.json \
        -o results/reasoning_nondet/reasoning_nondet_epoch${epoch}_conf${conf}_alpha${alpha}5_k1.txt \
        -t utils/theory.lp \
        --answer_mode single
    done
  done
done