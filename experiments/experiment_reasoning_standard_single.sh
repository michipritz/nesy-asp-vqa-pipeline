for epoch in 50 125 200; do # Network training epochs
  for conf_thres in 25 50; do # low and normal conf threshold
    /usr/bin/python3.8 reason.py -f facts_standard/facts_standard_${epoch}_conf${conf_thres}.json \
      -q data/CLEVR_v1.0/questions/CLEVR_val_questions.json \
      -o reasoning_standard_single/reasoning_standard_${epoch}_conf${conf_thres}.txt \
      -t commonsense_knowledge/spatial_reasoning.lp \
      --answer_mode single
  done
done
