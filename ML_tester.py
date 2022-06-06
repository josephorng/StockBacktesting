import numpy as np
import csv
from ToolBox import text2list
import os.path

# Define input feature
test = []
test_output = []
with open('./stock_ML/ML_test.csv') as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)  # change contents to floats
    # each row is a list
    for row in reader:
        test.append(row[0:18])
        test_output.append(row[18])

input_features = np.array(test)
# input_features = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
print('input_features--> ' + str(input_features.shape))

# Define target output
target_output = np.array(test_output)
# target_output = np.array([[0,1,1,1]])

# Reshaping out target output into vector:
target_output = target_output.reshape(len(test[:]), 1)
print('target_output---> ' + str(target_output.shape))

# Define weight
weights = np.array([[1.00105524],
                    [1.00009986],
                    [1.00162135],
                    [0.9995192],
                    [1.00018286],
                    [0.9939754],
                    [0.97950967],
                    [0.97188149],
                    [0.95825546],
                    [1.00053709],
                    [1.00162135],
                    [0.9995192],
                    [1.00003469],
                    [1.00093966],
                    [1.00076425],
                    [1.0005939],
                    [1.00028815],
                    [0.01241651]])

start_weights = weights
'''
0 收盤價/前一日收盤價
1 開盤價/前一日收盤價
2 最高價/前一日收盤價
3 最低價/前一日收盤價
4 5日均價/前一日收盤價
5 20日均價/前一日收盤價
6 60日均價/前一日收盤價
7 100日均價/前一日收盤價
8 300日均價/前一日收盤價
9 開盤價近1日趨勢
10 最高價近1日趨勢
11 最低價近1日趨勢
12 5日均價近1日趨勢
13 20日均價近1日趨勢
14 60日均價趨勢
15 100日均價趨勢
16 300日均價趨勢
17 當天收盤價

output 下一天漲跌幅
27 下二天漲跌幅
'''

# weights = np.array([[0], [0.2]])
print('weights---------> ' + str(weights.shape))

# Bias weighy
bias = [0.99430951]
start_bias = bias

# learning rate
lr = 0.000000001


# signoid function


def ReLU(x):
    if x > 1:
        return 1 + 0.1 * (x - 1)
    elif x > 0:
        return x
    elif x <= 0:
        return x
    elif x < -1:
        return -1 + 0.1 * (x + 1)


def ReLU_der(x):
    if x > 1:
        return 0.01
    elif x > 0:
        return 0.1
    elif x <= 0:
        return 0.1
    elif x < -1:
        return 0.01



start_error_sum = 0
# Main logic for neural network
# Running our code 1000 times:

inputs = input_features

# feedforward input:
in_o = np.dot(inputs, weights) + bias

# feedforward output:
out_o = in_o
for j in range(len(in_o)):
    out_o[j] = ReLU(in_o[j])

# backproppogation
# calculating error
error = out_o - target_output

# going with formula
x = error.sum_q()
print(x)

correct = 0
for i in range(len(test_output)):
    if out_o[i] > 0 and test_output[i] > 0:
        correct += 1

print('correct rate')
print(correct / len(out_o))


print('weights')
print(weights)
print('bias')
print(bias)
print('error')
print(x)

