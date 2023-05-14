import matplotlib.pyplot as plt
from main import h1
from main import h2
from main import beam
from main import maxNodes
from main import randomizeState
from main import printState
import copy


# # Question 1
#
# numH1 = 0
# numH2 = 0
# numB = 0
# h1Arr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# h2Arr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# bArr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#
# for i in range(100):
#     print(i)
#     for j in range(30):
#         maxNodes(150*j)
#         arr, b = randomizeState(i+50)
#
#         q1, bol1 = copy.deepcopy(h1(arr))
#         if str(q1[1]) == "[['b', '1', '2'], ['3', '4', '5'], ['6', '7', '8']]":
#             numH1 += 30-j
#             j2 = j
#             while j2 < 30:
#                 h1Arr[j2] += 1
#                 j2 += 1
#             break
#
#     for j in range(30):
#         maxNodes(150*j)
#         arr, b = randomizeState(i+50)
#
#         q2, bol2 = copy.deepcopy(h2(arr))
#         if str(q2[1]) == "[['b', '1', '2'], ['3', '4', '5'], ['6', '7', '8']]":
#             numH2 += 30 - j
#             j2 = j
#             while j2 < 30:
#                 h2Arr[j2] += 1
#                 j2 += 1
#             break
#
#     for j in range(30):
#         maxNodes(150*j)
#         arr, b = randomizeState(i+50)
#
#         q3, bol3 = copy.deepcopy(beam(arr, 9))
#         if str(q3[1]) == "[['b', '1', '2'], ['3', '4', '5'], ['6', '7', '8']]":
#             numB += 30 - j
#             j2 = j
#             while j2 < 30:
#                 bArr[j2] += 1
#                 j2 += 1
#             break
#         if j == 29:
#             printState(arr)
#
# for i in range(len(h1Arr)):
#     h1Arr[i] = h1Arr[i]/100.0
# for i in range(len(h2Arr)):
#     h2Arr[i] = h2Arr[i]/100.0
# for i in range(len(bArr)):
#     bArr[i] = bArr[i]/100.0
#
# print(h1Arr)
# print(h2Arr)
# print(bArr)
#
# plt.plot(range(150, 4501, 150), h1Arr, label="h1Arr")
# plt.plot(range(150, 4501, 150), h2Arr, label="h2Arr")
# plt.plot(range(150, 4501, 150), bArr, label="bArr")
#
# plt.xlabel('Max Nodes', fontweight='bold', fontsize=15)
# plt.ylabel('Percent solvable', fontweight='bold', fontsize=15)
#
# plt.title('Percentages of solvable h1, h2 and beam searches')
# plt.legend()
#
# # # Question 4
#
# plt.show()
# print("fraction of solvable h1", numH1/3000.0)
# print("fraction of solvable h2", numH2/3000.0)
# print("fraction of solvable beam", numB/3000.0)

# Question 2

# h1Nodes = []
# h2Nodes = []
#
# for i in range(100):
#     print(i)
#     arr, b = randomizeState(i+50)
#     q1, bol1 = h1(arr)
#     q2, bol2 = h2(arr)
#     h1Nodes.append(q1[4])
#     h2Nodes.append(q2[4])
#
# plt.plot(range(1, 101), h1Nodes, label="H1")
# plt.plot(range(1, 101), h2Nodes, label="H2")
#
# plt.xlabel('Random State', fontweight='bold', fontsize=15)
# plt.ylabel('Nodes Generated', fontweight='bold', fontsize=15)
#
# plt.title('Total number of Nodes Generated: A*')
# plt.legend()
#
# plt.show()

# Question 3

# h1Moves = []
# h2Moves = []
# bMoves = []
#
# for i in range(100):
#     print(i)
#     arr, b = randomizeState(i+50)
#     q1, bol1 = h1(arr)
#     q2, bol2 = h2(arr)
#     q3, b3 = beam(arr, 4)
#     h1Moves.append(len(q1[5]))
#     h2Moves.append(len(q2[5]))
#     if str(q3[1]) == "[['b', '1', '2'], ['3', '4', '5'], ['6', '7', '8']]":
#         bMoves.append(len(q3[3]))
#     else:
#         bMoves.append(0)
#
# plt.plot(range(1, 101), h1Moves, label="H1")
# plt.plot(range(1, 101), h2Moves, label="H2", linestyle='dashed')
# plt.plot(range(1, 101), bMoves, label="Beam")
#
# plt.xlabel('Random State', fontweight='bold', fontsize=15)
# plt.ylabel('Moves to Solve', fontweight='bold', fontsize=15)
#
# plt.title('Total Moves to Solve: A* & Beam')
# plt.legend()
#
# plt.show()
