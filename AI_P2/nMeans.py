# Iris Stuff
import copy
import csv
import random
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go


with open("iris.csv", "r") as file:
    data = csv.reader(file)

    irisData = []
    for row in data:
        iris = [float(x) for x in row[:4]]
        iris.append(row[4])
        iris.append(int())

        irisData.append(iris)

def boundaryLines(points):
    points.sort(key=lambda x: x[3])
    points.sort(key=lambda x: x[2])
    bLines = []
    for i in range(len(points)-1):
        mPoint = ((points[i][2]+points[i+1][2])/2, (points[i][3]+points[i+1][3])/2)

        if points[i+1][2]-points[i][2] != 0:
            slope = (points[i+1][3]-points[i][3]) / (points[i+1][2]-points[i][2])
            if slope != 0:
                slope = -1/slope
            else:
                slope = 999999999
        else:
            slope = 9999999999

        bLines.append([mPoint, slope, points[i][4], points[i+1][4]])
    return bLines


def kMeans(k):
    random.seed(0)
    samples = random.sample(irisData, k)
    for i in range(len(samples)):
        samples[i][5] = i

    sampleMeans = [[0 for _ in range(5)]for _ in range(k)]
    sums = []

    print("Sample Means", sampleMeans)
    print("Samples", samples)
    for i in range(100):
        summation = float(0)
        for n in irisData:
            intermediateSums = []
            for cluster in samples:
                # intermediateSums.append(pow((float(n[0])-float(cluster[0])), 2) + pow((float(n[1])-float(cluster[1])), 2) + pow((float(n[2])-float(cluster[2])), 2) + pow((float(n[3])-float(cluster[3])), 2))
                intermediateSums.append(sum([abs(xi - yi) ** 2 for xi, yi in zip(n[:4], cluster[:4])]))
            summation += min(intermediateSums)
            n[5] = intermediateSums.index(min(intermediateSums))

            sampleMeans[n[5]][0] = float(sampleMeans[n[5]][0])+float(n[0])
            sampleMeans[n[5]][1] = float(sampleMeans[n[5]][1])+float(n[1])
            sampleMeans[n[5]][2] = float(sampleMeans[n[5]][2])+float(n[2])
            sampleMeans[n[5]][3] = float(sampleMeans[n[5]][3])+float(n[3])
            sampleMeans[n[5]][4] = int(sampleMeans[n[5]][4])+1

        for x in sampleMeans:
            print("prev", x)
            if x[4] != 0:
                x[0] = x[0]/x[4]
                x[1] = x[1]/x[4]
                x[2] = x[2] / x[4]
                x[3] = x[3] / x[4]
            x[4] = 0
            print(x)

        if samples == sampleMeans:
            plt.clf()
            plt.plot(range(len(sums)), sums)
            plt.xlabel("Iterations")
            plt.ylabel("Distortion")
            plt.title("Distortion vs. Iterations")
            plotName = "convergence"
            plt.savefig(plotName)
            break

        plt.clf()

        pL = []
        pW = []
        guess = []

        for flower in irisData:
            pL.append(float(flower[2]))
            pW.append(float(flower[3]))
            guess.append(int(flower[5]))

        pl2 = []
        pw2=[]
        for sample in samples:
            pl2.append(float(sample[2]))
            pw2.append(float(sample[3]))

        slopes = boundaryLines(samples)

        x = range(8)
        for line in slopes:
            y = [(line[1] * (i - line[0][0])) + line[0][1] for i in x]
            plt.plot(x, y, color='k')

        plt.scatter(pL, pW, c=guess, cmap="summer", marker='o', alpha=.65)
        plt.scatter(pl2, pw2, marker='x')
        plt.xlabel('petal length')
        plt.ylabel('petal width')
        plt.title('My Line Plot')
        plotName = f'clusterGraph{i}.png'
        plt.xlim([0.5, 7.5])
        plt.ylim([0, 2.7])

        plt.savefig(plotName)

        sums.append(summation)
        samples = copy.deepcopy(sampleMeans)
        sampleMeans = [[0 for _ in range(5)]for _ in range(k)]


kMeans(2)


