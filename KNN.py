from sklearn import metrics
import sklearn
import csv
import math


def KNN_Builder():
    line_train = []
    col_train = []
    line_test = []
    col_test = []
    y_pred = []

    maxV = []
    minV = []

    train = open("train.csv")
    train_reader = csv.reader(train)
    next(train_reader, None)
    train_num_lines = 0
    test = open('test.csv')
    test_reader = csv.reader(test)
    next(test_reader, None)
    test_num_lines = 0

    for line in train_reader:
        train_num_lines = train_num_lines + 1
        line_train.append(line[1:30])
        col_train.append(line[0])

    for line in test_reader:
        test_num_lines = test_num_lines + 1
        line_test.append((line[1:30]))
        col_test.append(line[0])

    # finding max and min of every column of train matrix for the normalize
    for k in range(len(line_train[0])):
        kth_column = [sub[k] for sub in line_train]
        kth_more = [float(i) for i in kth_column]
        minV.append(min(kth_more))
        maxV.append(max(kth_more))

    # create new x matrixes (train and test) with normalized values
    for i in range(len(line_train[0])):
        for j in range(train_num_lines):
            line_train[j][i] = (float(line_train[j][i]) - minV[i]) / (maxV[i] - minV[i])

    for i in range(len(line_test[0])):
        for j in range(test_num_lines):
            line_test[j][i] = (float(line_test[j][i]) - minV[i]) / (maxV[i] - minV[i])

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
            if (res_list[t])[1] == '1':
                count_pos = count_pos + 1
        if count_pos > 4:
            y_pred.append('1')
        else:
            y_pred.append('0')

    print(sklearn.metrics.accuracy_score(col_test, y_pred))


if __name__ == '__main__':
    KNN_Builder()
