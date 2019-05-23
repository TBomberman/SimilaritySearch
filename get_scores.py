from sklearn.metrics import jaccard_similarity_score
from Helpers.data_loader import get_feature_dict, load_csv
import numpy as np
import os
import csv
import datetime

smiles_data_path = 'Data/'


def get_drug_features(row):
    introw = []
    for item in row[1:]:
        introw.append(int(item))
    drug_features = np.zeros(2048, dtype=np.int8)
    drug_features[introw] = 1
    return drug_features


def get_jaccard_scores():
    stem_cell_drugs = get_feature_dict('Data/stem_cell_compounds_morgan_2048.csv')
    stem_cell_drug_features = stem_cell_drugs["BRD-K42644990"]
    stem_cell_drug_features = np.reshape(np.array(stem_cell_drug_features, np.float16), (1, -1)).astype(np.int8)

    smi_files = os.listdir(smiles_data_path)

    for file in smi_files:
        if not file.endswith('.smi'):
            continue
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


get_jaccard_scores()
