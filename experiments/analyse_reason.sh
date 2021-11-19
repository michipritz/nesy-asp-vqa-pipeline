for epoch in 25 50 200; do # Network training epochs
  for conf in 25 50; do # low and normal conf threshold
    /usr/bin/python3.8 experiments/analyse_reason.py -i results/reasoning_nondet/reasoning_nondet_epoch${epoch}_conf${conf}.txt
  done
done