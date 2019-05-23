import numpy as np
from rdkit.Chem import AllChem, DataStructs
from rdkit import Chem
import csv

def load_csv(file):
    # load data
    expression = []
    with open(file, "r") as csv_file:
        reader = csv.reader(csv_file, dialect='excel')
        for row in reader:
            expression.append(row)
    return expression

def get_feature_dict(file, delimiter=',', key_index=0, use_int=False):
    with open(file, "r") as csv_file:
        reader = csv.reader(csv_file, dialect='excel', delimiter=delimiter)
        next(reader)
        if use_int:
            my_dict = {}
            for row in reader:
                list = []
                for value in row[1:]:
                    list.append(int(value))
                my_dict[row[key_index]] = list
            return my_dict
        return dict((row[key_index], row[1:]) for row in reader)
i = 0
finger_dimension = 2048
molecules = []
fps = []
id = []
smiles = []
names = []

import os
path = os.path.dirname(os.path.abspath(__file__))
print(path)
# drug_dict = get_feature_dict('GSE92742_Broad_LINCS_pert_info.txt', delimiter='\t', use_int=False) # uncomment for phase 1
# drug_dict = get_feature_dict('GSE70138_Broad_LINCS_pert_info.txt', delimiter='\t', use_int=False) # uncomment for phase 2

# rnaseq drugs # uncomment this and change filename below to get inhouse_morgan_2048.csv
drug_dict = {}
drug_dict['BRD-K42644990'] = ['','','','','','O=S(=O)(Nc1nc2ccccc2nc1NCCC3=CCCCC3)c4ccccc4']

count = 0
for key in drug_dict:
    count += 1
    try:
        smiles = drug_dict[key][5]
        m = Chem.MolFromSmiles(smiles)
        molecules.append(m)
        fp = np.zeros((1,))
        DataStructs.ConvertToNumpyArray(AllChem.GetMorganFingerprintAsBitVect(m, 2, nBits=finger_dimension), fp)
        fps.append(fp)
        id.append(key)
    except:
        print(i, key, m)
    i += 1

header = ["mol"]
for i in range(finger_dimension):
    header.append("fps" + str(i))

fps = np.array(fps).reshape(len(fps),finger_dimension)
id = np.array(id)    
id = id.reshape(len(fps), 1)
data = np.hstack((id, fps))
header = np.array(header).reshape(1, len(header))
data_header = np.vstack((header, data))
np.savetxt("stem_cell_compounds_morgan_2048.csv", data_header, delimiter=",", fmt="%s")
