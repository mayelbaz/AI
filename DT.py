import pandas as pd
import numpy as np
from pprint import pprint
from numpy import log2 as log
eps = np.finfo(float).eps



def entropy(column):
    elements, counts = np.unique(column, return_counts=True)
    entropy = np.sum(
        [(-counts[i] / np.sum(counts)) * np.log2(counts[i] / np.sum(counts)) for i in range(len(elements))])
    return entropy


def entropy_feature(data_size, positive_diagnosis, negative_diagnosis, feature, gap):
    below_positive = (positive_diagnosis.loc[positive_diagnosis[feature] <= gap]).shape[0]
    below_negative = (negative_diagnosis.loc[negative_diagnosis[feature] <= gap]).shape[0]
    total_below = below_negative + below_positive
    above_positive = positive_diagnosis.shape[0] - below_positive
    above_negative = negative_diagnosis.shape[0] - below_negative
    total_above = above_negative + above_positive
    if total_below == 0:
        entropy_below = 0
    else:
        entropy_below = -below_positive / total_below * log(below_positive / total_below + eps) + \
                        -below_negative / total_below * log(below_negative / total_below + eps)

    if total_above == 0:
        entropy_above = 0
    else:
        entropy_above = -above_positive / total_above * log(above_positive / total_above + eps) + \
                        -above_negative / total_above * log(above_negative / total_above + eps)
    feature_entropy = total_below / data_size * entropy_below + total_above / data_size * entropy_above
    return feature_entropy


def find_best_feature(df, features):
    pick_feature = []
    total = entropy(df['diagnosis'])
    data_size = df.shape[0]
    for feature in features:
        values = sorted(list(df[feature]), key=lambda x: float(x))
        gaps = []
        for i in range(len(values) - 1):
            gaps.append((values[i] + values[i + 1]) / 2)
        gaps = list(set(gaps))
        info_gain = []
        positive_diagnosis = df.loc[df['diagnosis'] == 1]
        negative_diagnosis = df.loc[df['diagnosis'] == 0]
        for gap in gaps:
            feature_entropy = entropy_feature(data_size, positive_diagnosis, negative_diagnosis, feature, gap)
            info_gain.append((total - feature_entropy, gap))
        feature_max_info_gain = max(info_gain, key=lambda info_gain_for_feature: info_gain_for_feature[0])
        pick_feature.append((feature_max_info_gain, feature))
    best_feature = max(pick_feature, key=lambda feature_info_gain: feature_info_gain[0][0])
    return best_feature[1], best_feature[0][1], best_feature[0][0]


def build_tree(df, features, prune_at=1):
    num_values = df.shape[0]
    if (df.loc[df['diagnosis'] == 1]).shape[0] >= df.shape[0] / 2:
        majority_class = 1
    else:
        majority_class = 0
    if (df.loc[df['diagnosis'] == majority_class]).shape[0] == num_values or features.shape[0] == 0:
        return None, [], majority_class, df
    if num_values <= prune_at:
        return None, [], majority_class, df
    feature, feature_value = find_best_feature(df, features)[0:2]
    below_feature_value = df.loc[df[feature] <= feature_value]
    above_feature_value = df.loc[df[feature] > feature_value]
    delimiter = (max(below_feature_value[feature]) + min(above_feature_value[feature])) / 2
    below_sub_tree = build_tree(below_feature_value, features, prune_at)
    above_sub_tree = build_tree(above_feature_value, features, prune_at)
    subtrees = [(delimiter, below_sub_tree), (delimiter, above_sub_tree)]
    return feature, subtrees, majority_class


def test_accuracy(tree):
    num_correct_prediction = 0
    dataset = pd.read_csv('test.csv')
    df = dataset.apply(pd.to_numeric, errors='coerce')
    total_data_size = df.shape[0]
    for i in range(total_data_size):
        if predict(df.iloc[[i]], tree) == df.iloc[[i]]['diagnosis'].values[0]:
            num_correct_prediction += 1
    return num_correct_prediction / total_data_size


def predict(query, tree):
    '''
    build_tree returns trinity - feature, subtrees[(delimiter, subtree_below), (delimiter, subtree_above)],
    majority_class (diagnosis)
    '''
    # if leaf tree[1] == []:
    if not tree[1]:
        # return leaf diagnosis
        return tree[2]
    # else, if test_database[feature]->diagnosis lower than tree[subtrees[subtree_below[delimiter]]]
    if query[tree[0]].values[0] <= tree[1][0][0]:
        # check accuracy of the the subtree_below
        return predict(query, tree[1][0][1])
    # check accuracy of the the subtree_above
    return predict(query, tree[1][1][1])


def build_id3_decision_tree():
    dataset = pd.read_csv('train.csv')
    df = dataset.apply(pd.to_numeric, errors='coerce')
    tree = build_tree(df=df, features=df.keys()[1:], prune_at=1)
    # print('The prediction accuracy is: ' + str(test_accuracy(tree) * 100) + '%')
    # pprint(tree)
    print(test_accuracy(tree))


if __name__ == '__main__':
    build_id3_decision_tree()