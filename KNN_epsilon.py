from DT_epsilon import *
from sklearn import metrics
import sklearn
import csv
import math


def KNN_Builder(df_train, df_test):
    line_train = []
    col_train = []
    line_test = []
    col_test = []
    y_pred = []

    maxV = []
    minV = []

    train_num_lines = 0
    test_num_lines = 0

    for leaf in df_train:
        for line in leaf:
            train_num_lines = train_num_lines + 1
            col_train.append(line[0])
            col = 1
            new_line = []
            while col < 31:
                new_line.append(line[col])
                col += 1
            line_train.append(new_line)

    for line in df_test:
        test_num_lines = test_num_lines + 1
        col_test.append(line[0])
        col = 1
        new_line = []
        while col < 31:
            new_line.append((line[col]))
            col += 1
        line_test.append(new_line)

    # finding max and min of every column of train matrix for the normalize
    for k in range(len(line_train[0])):
        kth_column = [sub[k] for sub in line_train]
        kth_more = [float(i) for i in kth_column]
        minV.append(min(kth_more))
        maxV.append(max(kth_more))

    # getting y_pred vec by comparing to k neighbors
    for test_line in range(len(line_test)):
        res_list = []
        for train_line in range(len(line_train)):
            curr_sum = 0
            for category in range(len(line_train[0])):
                curr_sum += math.pow(float(line_test[test_line][category]) - float(line_train[train_line][category]), 2)
            dist = math.sqrt(curr_sum)
            res_list.append((dist, col_train[train_line]))
        res_list.sort(key=lambda tup: tup[0])

        count_pos = 0
        k = 9
        for t in range(k):
            if (res_list[t])[1] == 1:
                count_pos = count_pos + 1
        if count_pos > 4:
            y_pred.append(1)
        else:
            y_pred.append(0)

    # print('The prediction accuracy is: ' + str(sklearn.metrics.accuracy_score(col_test, y_pred) * 100) + '%')
    return y_pred


def determine_classification(results_array):
    count_positive_diagnosis = 0
    count_total = 0
    for result in results_array:
        count_total += (result[1]).shape[0]
        count_positive_diagnosis += (result[1].loc[result[1]['diagnosis'] == 1]).shape[0]
    if count_positive_diagnosis >= count_total / 2:
        return 1
    return 0


def determine_classification_KNN_epsilon(results_array, df, i):
    relevant_examples_count = 0
    for result in results_array:
        if result[2]:
            relevant_examples_count += (result[1]).shape[0]
    if relevant_examples_count < 9:
        return determine_classification(results_array)
    values_array = []
    for leaf in results_array:
        if leaf[2]:  # came from epsilon rule
            values_array.append(leaf[1].values)
            # relevant_leafs.concat(leaf[1])
    # print("called KNN")
    y_pred = KNN_Builder(values_array, df.iloc[[i]].values)
    if len(y_pred) > 1:
        print("FUCK.")
    return y_pred[0]


def predict_KNN_epsilon(query, epsilon_df, leafs_array, tree, came_from_epsilon):
    '''
    build_tree returns trinity - feature, subtrees[(delimiter, subtree_below), (delimiter, subtree_above)],
    majority_class (diagnosis)
    '''
    # if leaf tree[1] == []:
    if not tree[1]:
        # append leaf diagnosis
        if came_from_epsilon[0]:
            leafs_array.append((tree[2], tree[3], True))
            return
        else:
            leafs_array.append((tree[2], tree[3], False))
            return
    # check if epsilon condition holds
    elif abs(query[tree[0]].values[0] - tree[1][0][0]) <= epsilon_df[tree[0]].values[0]:
        came_from_epsilon[0] = True
        predict_KNN_epsilon(query, epsilon_df, leafs_array, tree[1][0][1], came_from_epsilon)
        predict_KNN_epsilon(query, epsilon_df, leafs_array, tree[1][1][1], came_from_epsilon)
        return
    # epsilon condition does not hold - continue as usual
    # else, if test_database[feature]->diagnosis lower than tree[subtrees[subtree_below[delimiter]]]
    elif query[tree[0]].values[0] <= tree[1][0][0]:
        # check accuracy of the the subtree_below
        predict_KNN_epsilon(query, epsilon_df, leafs_array, tree[1][0][1], came_from_epsilon)
        return
    # check accuracy of the the subtree_above
    else:
        predict_KNN_epsilon(query, epsilon_df, leafs_array, tree[1][1][1], came_from_epsilon)
        return

def test_accuracy_with_KNN_epsilon(tree):
    num_correct_prediction = 0
    dataset = pd.read_csv('test.csv')
    df = dataset.apply(pd.to_numeric, errors='coerce')
    v = np.std(df, axis=0, ddof=0)
    epsilon = 0.1 * v
    epsilon_dataset = pd.DataFrame()
    features = df.keys()
    for feature_index in range(len(list(features))):
        epsilon_dataset[features[feature_index]] = [epsilon[feature_index]]
    epsilon_df = epsilon_dataset.apply(pd.to_numeric, errors='coerce')
    total_data_size = df.shape[0]
    for i in range(total_data_size):
        leafs_array = []
        predict_KNN_epsilon(df.iloc[[i]], epsilon_df, leafs_array, tree, [False])
        classification = determine_classification_KNN_epsilon(leafs_array, df, i)
        if classification == df.iloc[[i]]['diagnosis'].values[0]:
            num_correct_prediction += 1
    return num_correct_prediction / total_data_size


def build_KNN_epsilon_deision_tree():
    dataset = pd.read_csv('train.csv')
    df = dataset.apply(pd.to_numeric, errors='coerce')
    tree = build_tree(df=df, features=df.keys()[1:], prune_at=9)
    # print('The prediction accuracy is: ' + str(test_accuracy_with_KNN_epsilon(tree) * 100) + '%')
    print(test_accuracy_with_KNN_epsilon(tree))
    # pprint(tree)


if __name__ == '__main__':
    build_KNN_epsilon_deision_tree()
