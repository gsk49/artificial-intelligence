import pandas as pd
import numpy as np
import plotly.express as px
import random
import plotly.io as pio
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import math

def sigmoid(z):
    return 1.0 / (1 + math.exp(-z))


def prediction(data, w, b):
    y = []
    for i in range(len(data)):
        y.append(np.dot(data[i], w) + b)

    predictions = []
    for i in y:
        predictions.append(sigmoid(i))


    pList = []
    for x in range(len(predictions)):
        if predictions[x] >= .5:
            pList.append(1)
        else:
            pList.append(0)

    return np.array(pList)


def MSE(data, w, b, c):
    mse = 0

    for i in range(len(data)):
        y_hat = sigmoid(np.dot(data[i], w) + b)
        diff = pow(c[i]-y_hat, 2)
        mse += diff

    mse = mse / len(data)
    return mse


def plotBoundary(data, iris, w, b, title):
    print("w",w)
    print("b", b)
    intercept = -b / w[3]
    slope = -w[2] / w[3]

    x = np.array([.5, 7])
    y = slope * x + intercept
    classes = prediction(iris, w, b)

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data["petal_length"], y=data["petal_width"], mode='markers', name='points', marker={'color': ['red' if c == 1 else 'black' for c in classes]}))
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='decision boundary'))
    fig.update_layout(title=title)
    fig.show()


def gradient(w, b, LnW, goal):
    grad = []
    b_grad = 0

    c = prediction(LnW, w, b)

    for i in range(len(LnW)):
        b_grad += c[i] - goal[i]

    for i in range(len(w)):
        gSum = 0
        for j in range(len(LnW)):
            temp = c[j] - goal[j]
            temp = temp * LnW[j][i]
            gSum += temp

        grad.append(gSum)

    return np.array(grad), b_grad


def boundary_diff(data, pW, pB, LnW, goal, step, i):
    w = pW
    b = pB
    for x in range(i):
        #plotBoundary(data, LnW, w, b, i)
        wGradient, bGradient = gradient(w, b, LnW, goal)

        w -= step*wGradient
        b -= step*bGradient

    plotBoundary(data, LnW, w, b, i)


def main():
    data = pd.read_csv("/Users/grant/PycharmProjects/AI2_Classify/iris2.csv")
    data = data[50:]
    vals = data.iloc[:, 0:4].to_numpy()
    goal = data.iloc[:, -1].to_numpy()



    temporary = []
    for i in range(len(goal)):
        if goal[i] == "Iris-versicolor":
            temporary.append(0)
        else:
            temporary.append(1)
    goal = np.array(temporary)

    optimal_w = np.array([-2.98924, -7.09957,  5.94623, 11.00846])
    optimal_b = -9.122299999996885

    optimal_MSE = MSE(vals, optimal_w, optimal_b, goal)

    # bad_w = np.array([10, 1, 1, 1])
    # bad_b = -.7
    # bad_MSE = MSE(vals, bad_w, bad_b, goal)

    print("Optimal MSE: ", optimal_MSE)
    # plotBoundary(data, vals, optimal_w, optimal_b, "Linear Decision Boundary for very small error")

    # print("Bad MSE: ", bad_MSE)
    # plotBoundary(data, vals, bad_w, bad_b, "Linear Decision Boundary for very large error")

    boundary_diff(data, np.array([10.57978000000002, -8.069180000000031, 14.859540000000006, 12.980889999999988]), -5.9, vals, goal, 0.0001, 100000)


main()
