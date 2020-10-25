from DT import *


def predict_epsilon(query, epsilon_df, leafs_array, tree):
    '''
    build_tree returns trinity - feature, subtrees[(delimiter, subtree_below), (delimiter, subtree_above)],
    majority_class (diagnosis)
    '''
    # if leaf tree[1] == []:
    if not tree[1]:
        # append leaf diagnosis
        leafs_array.append((tree[2], tree[3]))
        return
    # check if epsilon condition holds
    elif abs(query[tree[0]].values[0] - tree[1][0][0]) <= epsilon_df[tree[0]].values[0]:
        predict_epsilon(query, epsilon_df, leafs_array, tree[1][0][1])
        predict_epsilon(query, epsilon_df, leafs_array, tree[1][1][1])
        return
    # epsilon condition does not hold - continue as usual
    # else, if test_database[feature]->diagnosis lower than tree[subtrees[subtree_below[delimiter]]]
    elif query[tree[0]].values[0] <= tree[1][0][0]:
        # check accuracy of the the subtree_below
        predict_epsilon(query, epsilon_df, leafs_array, tree[1][0][1])
        return
    # check accuracy of the the subtree_above
    else:
        predict_epsilon(query, epsilon_df, leafs_array, tree[1][1][1])
        return


def determine_classification(results_array):
    count_positive_diagnosis = 0
    count_total = 0
    for result in results_array:
        count_total += (result[1]).shape[0]
        count_positive_diagnosis += (result[1].loc[result[1]['diagnosis'] == 1]).shape[0]
    if count_positive_diagnosis >= count_total / 2:
        return 1
    return 0


def test_accuracy_with_epsilon(tree):
    num_correct_prediction = 0
    dataset = pd.read_csv('test.csv')
    df = dataset.apply(pd.to_numeric, errors='coerce')
    v = np.std(df, axis=0, ddof=0)
    epsilon = 0.1 * v
    epsilon_dataset = pd.DataFrame()
    features = df.keys()
    for feature_index in range(len(features)):
        epsilon_dataset[features[feature_index]] = [epsilon[feature_index]]
    epsilon_df = epsilon_dataset.apply(pd.to_numeric, errors='coerce')
    total_data_size = df.shape[0]
    for i in range(total_data_size):
        leafs_array = []
        predict_epsilon(df.iloc[[i]], epsilon_df, leafs_array, tree)
        classification = determine_classification(leafs_array)
        if classification == df.iloc[[i]]['diagnosis'].values[0]:
            num_correct_prediction += 1
    return num_correct_prediction / total_data_size


def build_id3_epsilon_decision_tree():
    dataset = pd.read_csv('train.csv')
    df = dataset.apply(pd.to_numeric, errors='coerce')
    tree = build_tree(df, df.keys()[1:], prune_at=9)
    # print('The prediction accuracy is: ' + str(test_accuracy_with_epsilon(tree) * 100) + '%')
    # pprint(tree)
    print(test_accuracy_with_epsilon(tree))


if __name__ == '__main__':
    build_id3_epsilon_decision_tree()