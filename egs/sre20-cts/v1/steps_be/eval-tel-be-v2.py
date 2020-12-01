#!/usr/bin/env python
"""
  Copyright 2019 Johns Hopkins University  (Author: Jesus Villalba)
  Apache 2.0  (http://www.apache.org/licenses/LICENSE-2.0)  

  Evals Cosine
"""
import sys
import os
import argparse
import time
import logging

import numpy as np

from hyperion.hyp_defs import float_cpu, config_logger
from hyperion.utils import TrialNdx, TrialScores
from hyperion.utils.math import cosine_scoring
from hyperion.pdfs import PLDA
from hyperion.helpers import TrialDataReader as TDR
from hyperion.helpers import PLDAFactory as F
from hyperion.transforms import TransformList


def eval_plda(iv_file, ndx_file, enroll_file, test_file,
              preproc_file, score_file, pool_method, **kwargs):
    
    logging.info('loading data')
    if preproc_file is not None:
        preproc = TransformList.load(preproc_file)
    else:
        preproc = None

    tdr = TDR(iv_file, ndx_file, enroll_file, test_file, preproc)
    x_e, x_t, enroll, ndx = tdr.read()
    enroll, ids_e = np.unique(enroll, return_inverse=True)

    t1 = time.time()
    logging.info('computing llr')
    D_e = PLDA.compute_stats_hard(x_e, class_ids=ids_e)
    x_e=D_e[1]/np.expand_dims(D_e[0], axis=-1)
    scores = cosine_scoring(x_e, x_t)
    
    dt = time.time() - t1
    num_trials = len(enroll) * x_t.shape[0]
    logging.info('scoring elapsed time: %.2f s. elapsed time per trial: %.2f ms.'
                 % (dt, dt/num_trials*1000))

    logging.info('saving scores to %s' % (score_file))
    s = TrialScores(enroll, ndx.seg_set, scores)
    s.save_txt(score_file)


    
if __name__ == "__main__":

    parser=argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,                
        fromfile_prefix_chars='@',
        description='Eval cosine scoring')

    parser.add_argument('--iv-file', dest='iv_file', required=True)
    parser.add_argument('--ndx-file', dest='ndx_file', default=None)
    parser.add_argument('--enroll-file', dest='enroll_file', required=True)
    parser.add_argument('--test-file', dest='test_file', default=None)
    parser.add_argument('--preproc-file', dest='preproc_file', default=None)

    TDR.add_argparse_args(parser)
    parser.add_argument('--pool-method', dest='pool_method', type=str.lower,
                         default='vavg-lnorm',
                         choices=['vavg','savg'],
                         help=('(default: %(default)s)'))

    parser.add_argument('--score-file', dest='score_file', required=True)
    parser.add_argument('-v', '--verbose', dest='verbose', default=1,
                        choices=[0, 1, 2, 3], type=int)

    args=parser.parse_args()
    config_logger(args.verbose)
    del args.verbose
    logging.debug(args)

    assert args.test_file is not None or args.ndx_file is not None
    eval_plda(**vars(args))

            
