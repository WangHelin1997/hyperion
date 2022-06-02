"""
 Copyright 2018 Johns Hopkins University  (Author: Jesus Villalba)
 Apache 2.0  (http://www.apache.org/licenses/LICENSE-2.0)
"""

import numpy as np
import h5py

import scipy.linalg as la

from ..np_model import NPModel
from ..pdfs import Normal
from .cent_whiten import CentWhiten


class CentWhitenUP(CentWhiten):
    """Class to do centering and whitening with uncertainty propagation."""

    def __init__(self, mu=None, T=None, update_mu=True, update_T=True, **kwargs):
        super().__init__(mu, T, update_mu, update_T, **kwargs)

    def predict(self, x):
        x_dim = int(x.shape[-1] / 2)
        m_x = x[:, :x_dim]
        s2_x = x[:, x_dim:]
        m_x = super().predict(m_x)
        for i in range(x.shape[0]):
            s2_x[i] = np.diag(np.dot(self.T.T * s2_x[i], self.T))
        return np.hstack((m_x, s2_x))

    def fit(self, x, sample_weight=None):
        x = x[:, : int(x.shape[-1] / 2)]
        super().fit(x, sample_weight=sample_weight)
