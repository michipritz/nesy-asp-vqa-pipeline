
for epoch in 25 50 200; do # Network training epochs
  for conf_thres in 25 50; do # low and normal conf threshold
    /usr/bin/python3.8 reason.py -f results/facts_enhanced/facts_enhanced_${epoch}_conf${conf_thres}.json \
      -q data/CLEVR_v1.0/questions/CLEVR_val_sample_15000.json \
      -o results/reasoning_sample15k_nondet_single/reasoning_sample15k_nondet_${epoch}_conf${conf_thres}.txt \
      -t commonsense_knowledge/theory.lp \
      --epoch ${epoch} \
      --conf 0.${conf_thres} \
      --answer_mode single
  done
done
