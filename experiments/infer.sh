#!/bin/bash

for dir in 'scene_encodings_det'; do
  for epoch in 25 50 200; do # Network training epochs
    for conf_thres in 25 50; do # low and normal conf threshold
      /usr/bin/python3.8 infer.py ${epoch} ${conf_thres} ${dir}
    done
  done
done
