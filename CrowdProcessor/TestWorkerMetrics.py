__author__ = 'marc'

import VectorProcessing
import unicodecsv


def get_data_from_csv(path_to_csv):
    csvfile = open(path_to_csv, 'r')
    return list(unicodecsv.DictReader(csvfile))

tw2 = get_data_from_csv('Results/2tw.csv')
rows = VectorProcessing.prepocess_vectors(tw2)
unit_vectors = VectorProcessing.get_unit_vectors(rows)
worker_vectors = VectorProcessing.get_worker_vectors(rows)
