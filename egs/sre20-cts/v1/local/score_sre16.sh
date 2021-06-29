#!/bin/bash
# Copyright 2019 Johns Hopkins University (Jesus Villalba)  
# Apache 2.0.
#
if [ $# -ne 3 ]; then
  echo "Usage: $0 <data-root> <subset> <score-dir>"
  exit 1;
fi

set -e

data_dir=$1
subset=$2
score_dir=$3

key=$data_dir/trials

echo "SRE16 ${dev_eval}"

#Compute performance
python local/score_dcf.py --key-file $key \
       --score-file $score_dir/sre16_${subset}_scores \
       --output-path $score_dir/sre16_${subset}





