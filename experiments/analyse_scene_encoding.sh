for epoch in 25 50 200; do # Network training epochs
  for conf in 25 50; do # low and normal conf threshold
    python experiments/analyse_scene_encoding_nondet.py -i results/scene_encodings_nondet_k1/scene_encoding_nondet_epoch${epoch}_conf${conf}_alpha05_k1.json
  done
done

for epoch in 25 50 200; do # Network training epochs
  for conf in 25 50; do # low and normal conf threshold
    python experiments/analyse_scene_encoding_nondet.py -i results/scene_encodings_nondet_k1/scene_encoding_nondet_epoch${epoch}_conf${conf}_alpha1_k1.json
  done
done

for epoch in 25 50 200; do # Network training epochs
  for conf in 25 50; do # low and normal conf threshold
    python experiments/analyse_scene_encoding_nondet.py -i results/scene_encodings_nondet_k1/scene_encoding_nondet_epoch${epoch}_conf${conf}_alpha2_k1.json
  done
done