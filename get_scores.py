from sklearn.metrics import jaccard_similarity_score
from Helpers.data_loader import get_feature_dict
import numpy as np
import os
import csv
import datetime
import multiprocessing as mp
from multiprocessing import Pool
from contextlib import closing

smiles_data_path = 'Data/'


def get_drug_features(row):
    introw = []
    for item in row[1:]:
        introw.append(int(item))
    drug_features = np.zeros(2048, dtype=np.int8)
    drug_features[introw] = 1
    return drug_features


def get_jaccard_scores(file):
    stem_cell_drugs = get_feature_dict('Data/stem_cell_compounds_morgan_2048.csv')
    stem_cell_drug_features = stem_cell_drugs["BRD-K42644990"]
    stem_cell_drug_features = np.reshape(np.array(stem_cell_drug_features, np.float16), (1, -1)).astype(np.int8)

    print(datetime.datetime.now(), "Scoring file:", file)
    with open(smiles_data_path + file, "r") as csv_file:
        reader = csv.reader(csv_file, dialect='excel', delimiter=',')
        for row in reader:
            try:
                molecule_id = row[0]
                zinc_drug_features = get_drug_features(row)
                score = jaccard_similarity_score(stem_cell_drug_features[0], zinc_drug_features)
                if score > 0.98:
                    print(molecule_id, score)
            except:
                continue


def split_multi_process():
    print("Starting multiprocessing")
    all_files = os.listdir(smiles_data_path)

    processed_files = []
    if 'processed.txt' in all_files:
        with open(smiles_data_path + 'processed.txt', newline='') as csvfile:
            processed_files = list(csv.reader(csvfile))

    smi_files = []

    for file in all_files:
        if not file.endswith('.smi'):
            continue
        if [file] in processed_files:
            continue
        smi_files.append(file)

    with closing(Pool(mp.cpu_count())) as pool:
        pool.map(get_jaccard_scores, smi_files)


# get_jaccard_scores()
split_multi_process()
