#for epoch in 50 125 200; do # Network training epochs
#  for conf_thres in 25 50; do # low and normal conf threshold
#    /usr/bin/python3.8 reason.py -f facts_enhanced/facts_enhanced_${epoch}_conf${conf_thres}.json \
#      -q data/CLEVR_v1.0/questions/CLEVR_val_questions.json \
#      -o reasoning_enhanced_multiple/reasoning_enhanced_multiple_${epoch}_conf${conf_thres}.txt \
#      -t commonsense_knowledge/theory.lp \
#      --answer_mode multiple
#  done
#done

for epoch in 25; do # Network training epochs
  for conf_thres in 25 50; do # low and normal conf threshold
    /usr/bin/python3.8 reason.py -f results/facts_enhanced/facts_enhanced_${epoch}_conf${conf_thres}.json \
      -q data/CLEVR_v1.0/questions/CLEVR_val_questions.json \
      -o results/reasoning_enhanced_multiple/reasoning_enhanced_multiple_${epoch}_conf${conf_thres}.txt \
      -t commonsense_knowledge/theory.lp \
      --answer_mode multiple
  done
done
