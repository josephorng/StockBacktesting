import numpy as np
import csv
from ToolBox import text2list
import os.path

# Define input feature
train = []
train_output = []
with open('./stock_ML/ML_train.csv') as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)  # change contents to floats
    # each row is a list
    for row in reader:
        train.append([row[0]] + row[2:12] + row[13:18])
        train_output.append(row[18])

input_features = np.array(train)
# input_features = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
print('input_features--> ' + str(input_features.shape))

# Define target output
target_output = np.array(train_output)
# target_output = np.array([[0,1,1,1]])

# Reshaping out target output into vector:
target_output = target_output.reshape(len(train[:]), 1)
print('target_output---> ' + str(target_output.shape))

# Define weight
weights = [[1.0] * len(train[0][:])]
start_weights = weights
weights = np.array(weights)
weights = weights.reshape(len(train[0][:]), 1)

weights = np.array([[0.99990653],
                    [0.9998824],
                    [0.99999131],
                    [0.99997268],
                    [0.99993829],
                    [0.99993703],
                    [0.99995397],
                    [1.00003748],
                    [0.99995998],
                    [0.9998824],
                    [0.99999131],
                    [0.99999802],
                    [0.99999819],
                    [0.99999797],
                    [0.9999982],
                    [0.82157356]])

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

18 output 下一天漲跌幅
19 下二天漲跌幅
'''

# weights = np.array([[0], [0.2]])
print('weights---------> ' + str(weights.shape))

# Bias weighy
bias = [0.99395257]
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


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_der(x):
    return sigmoid(x) * (1 - sigmoid(x))


start_error_sum = 0
# Main logic for neural network
# Running our code 1000 times:
epoch_round = 1000
start_error_sum = 0
x = 0
for epoch in range(epoch_round):
    epoch_round += 1

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

    if epoch_round == 0:
        start_error_sum = x

    print('error_sum = ' + str(x))
    derror_douto = error
    douto_dino = out_o
    for j in range(len(out_o)):
        douto_dino[j] = ReLU_der(out_o[j])

    # douto_dino = sigmoid_der(out_o)

    # Multiplying individual derivatives:
    deriv = derror_douto * douto_dino

    # Multiplying with the 3rd individual derivative
    # finding the transpose of input_features :
    inputs = input_features.T
    deriv_final = np.dot(inputs, deriv)

    # Updating the weights values
    weights -= lr * deriv_final

    # updating the bias weight value :
    for i in deriv:
        bias -= lr * i
i = 0
while os.path.isfile('./stock_ML/ML_result_' + str(i) + '.csv'):
    i = i + 1
with open('./stock_ML/ML_result_' + str(i) + '.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['start weights'])
    writer.writerow(start_weights)
    writer.writerow(['start bias'])
    writer.writerow(start_bias)
    writer.writerow(['start_error_sum'])
    writer.writerow([start_error_sum])
    writer.writerow(['learning rate'])
    writer.writerow([lr])
    writer.writerow(['epoch'])
    writer.writerow([epoch_round])

    writer.writerow(['weights'])
    writer.writerow(weights)
    writer.writerow(['bias'])
    writer.writerow(bias)
    writer.writerow(['error_sum'])
    writer.writerow([x])
print('weights')
print(weights)
print('bias')
print(bias)
print('error')
print(x)
'''
print (bias) #Taking inputs:
single_point = np.array([1,0]) #1st step:
result1 = np.dot(single_point, weights) + bias #2nd step:
result2 = sigmoid(result1) #Print final result
print(result2) #Taking inputs:
single_point = np.array([1,1]) #1st step:
result1 = np.dot(single_point, weights) + bias #2nd step:
result2 = sigmoid(result1) #Print final result
print(result2) #Taking inputs:
single_point = np.array([0,0]) #1st step:
result1 = np.dot(single_point, weights) + bias #2nd step:
result2 = sigmoid(result1) #Print final result
print(result2)




'''
