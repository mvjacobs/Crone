__author__ = 'marc'

import scipy.spatial
import numpy as np
from numpy import *
from itertools import groupby
from operator import itemgetter
import math


def get_group_vector(unit_vectors):
    M = np.array(unit_vectors)
    rows_count, cols_count = M.shape
    group_vector = []
    for i in range(0, cols_count):
        group_vector.append(sum(M[:, i]))

    return group_vector


def get_cosine_similarity(unit_vector, group_vector):
    np.seterr(divide='ignore', invalid='ignore')
    return 1.0 - scipy.spatial.distance.cosine(unit_vector, group_vector)


def groupby_element(all_vectors, element_index, start_vector, end_vector):
    all_vectors.sort(key=itemgetter(element_index))
    grouped = []
    for elt, items in groupby(all_vectors, itemgetter(element_index)):
        grouped.append((elt, [item[start_vector:end_vector] for item in items]))
    return grouped


def groupby_one_element(all_vectors, element_index, index):
    all_vectors.sort(key=itemgetter(element_index))
    grouped = []
    for elt, items in groupby(all_vectors, itemgetter(element_index)):
        grouped.append((elt, [item[index] for item in items]))

    return grouped


def replace_nan_to_zero(arrays):
    new_arr = arrays
    for k, arr in enumerate(arrays):
        for k2, item in enumerate(arr):
            if isinstance(item, float) and math.isnan(item):
                new_arr[k][k2] = float(0.0)
    return new_arr





