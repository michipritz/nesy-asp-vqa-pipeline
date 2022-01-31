#!/bin/bash

for dir in 'infer_problog'; do
  for epoch in 25 50 200; do # Network training epochs
    for conf_thres in 25 50; do # low and normal conf threshold
      for k in 1 4; do # size of disjunctions
        /usr/bin/python3.8 infer_problog.py ${epoch} ${conf_thres} ${k} ${dir}
    done
  done
done
