from sklearn.metrics import jaccard_similarity_score

# def get_jaccard_score_of_rnaseq_drug(drug_id, lincs_drugs):
# #     rnaseq_drugs = get_feature_dict('Data/inhouse_morgan_2048.csv')
# #
# #     rnaseq_drug = rnaseq_drugs[drug_id]
# #     rnaseq_drug = np.reshape(np.array(rnaseq_drug, np.float16), (1, -1))
# #     rnaseq_drug = remove_corr_features(rnaseq_drug)
# #     scores = []
# #     for lincs_drug in lincs_drugs:
# #         score = jaccard_similarity_score(lincs_drug, rnaseq_drug[0])
# #         scores.append(score)
# #     return np.mean(scores)