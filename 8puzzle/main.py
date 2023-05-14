import random
from queue import PriorityQueue
from numpy import *
import copy
import sys

# read the text file
with open("/Users/grant/PycharmProjects/8puzzle/8puz.txt", "r") as f:
    text = f.readlines()
arr = []    # create an arr var
b = (0, 0)  # create a b var
maxN = sys.maxsize      # set initial maxN to the largest possible int


def findB(arr):
    b = (0, 0)      # initialize b to (0, 0)    (in case b is not in the puzzle)
    for i in range(len(arr)):       # iterate through the arr and if b is found, b location = (i, j)
        for j in range(len(arr[i])):
            if arr[i][j] == 'b':
                b = (i, j)
                break
        else:
            continue
        break

    return b


def legalMoves(b):
    moves = []      # given a b value, find which moves are legal
    if b[0] != 0:   # if b is not in row 0, it can move up
        moves.append("up")
    if b[0] != 2:   # if b is not in row 2, it can move down
        moves.append("down")
    if b[1] != 0:   # if b is col in row 0, it can move left
        moves.append("left")
    if b[1] != 2:   # if b is not in col 2, it can move right
        moves.append("right")
    return moves    # return all legal moves


def setState(state):
    state = state.replace(" ", "")      # remove the inner spaces from the state: "b12 345 678" -> "b12345678"
    rows, cols = (3, 3)         # create an array of arrays 3x3 in size (one array that holds three arrays of len 3)
    arr = [[state[i * cols + j] for j in range(cols)] for i in range(rows)]     # fill the array with the chars of state
    b = findB(arr)      # find b val for arr
    return arr, b       # return arr, b


def printState(arr):
    for i in arr:   # print each row in arr
        print(i)
    print()


def move(array, dir, bval):

    arr = copy.deepcopy(array)      # create a modifiable copy of array
    b = copy.deepcopy(bval)         # create a modifiable copy of bval

    if dir == "up":                 # if dir is "up"
        if b[0] == 0:               # check if you can't go up
            return arr, b
        elif b[0] == 1:             # if b is in row 1, switch arr[1][b[1]] and arr[0][b[1]]
            arr[1][b[1]] = arr[0][b[1]]
            arr[0][b[1]] = 'b'
            b = (0, b[1])           # set new b location

            return arr, b           # return new arr, b
        elif b[0] == 2:             # if b is in row 2, switch arr[2][b[1]] and arr[1][b[1]]
            arr[2][b[1]] = arr[1][b[1]]
            arr[1][b[1]] = 'b'
            b = (1, b[1])           # set new b location
            return arr, b           # return new arr, b
        else:
            print("Error")          # theoretically impossible

    elif dir == "down":             # copy up, but reverse the direction of swaps and check for ability to move
        if b[0] == 2:
            return arr, b
        elif b[0] == 1:
            arr[1][b[1]] = arr[2][b[1]]
            arr[2][b[1]] = 'b'
            b = (2, b[1])
            return arr, b
        elif b[0] == 0:
            arr[0][b[1]] = arr[1][b[1]]
            arr[1][b[1]] = 'b'
            b = (1, b[1])
            return arr, b
        else:
            print("Error")

    elif dir == "left":            # very similar to up and down, but we are using the opposite indexes for b
        if b[1] == 0:
            return arr, b
        elif b[1] == 1:
            arr[b[0]][1] = arr[b[0]][0]
            arr[b[0]][0] = 'b'
            b = (b[0], 0)
            return arr, b
        elif b[1] == 2:
            arr[b[0]][2] = arr[b[0]][1]
            arr[b[0]][1] = 'b'
            b = (b[0], 1)
            return arr, b
    elif dir == "right":           # copy left, but reverse as needed
        if b[1] == 2:
            return arr, b
        elif b[1] == 1:
            arr[b[0]][1] = arr[b[0]][2]
            arr[b[0]][2] = 'b'
            b = (b[0], 2)
            return arr, b
        elif b[1] == 0:
            arr[b[0]][0] = arr[b[0]][1]
            arr[b[0]][1] = 'b'
            b = (b[0], 1)
            return arr, b
    else:
        print("error2")

    return arr, b


def randomizeState(k):
    arr, b = setState("b12345678")      # set the state to the solved state
    random.seed(int(k))    # set the random seed (so randomizeState k will always be the same for the same k)
    for n in range(int(k)):     # repeat k times
        moves = legalMoves(b)   # find the legal moves at the current state
        arr, b = move(arr, random.choice(moves), b)     # pick one of them and move in that dir (update arr,b)

    return arr, b       # return the array and b location at the end


def h1Err(arr):
    err = -1    # set err to -1 (will go to 0 when arr[0][0] != 0)
    count = 0   # initialize count to 0
    for i in range(len(arr)):   # loop through integer rows of arr
        for j in range(len(arr[i])):    # loop through integer cols of arr
            if arr[i][j] != str(count):     # if the index at arr[i][j] != count: err+=1
                err += 1
            count += 1  # add to count

    return err      # return the total error


def h2Err(arr):
    err = 0     # initialize error to zero
    for i in range(len(arr)):       # loop through the rows
        for j in range(len(arr[i])):        # loop through the cols
            if arr[i][j] == '1' or arr[i][j] == '2':    # for each item belonging to row 0, add the row to the error
                err += i                                # e.g. an element in row 2, belonging in row 0, adds error 2
            if arr[i][j] == '3' or arr[i][j] == '4' or arr[i][j] == '5':    # if it belongs in row 1
                err += abs(i - 1)             # err += abs(row-1)    e.g. an element in row 0 has err abs(0-1) = 1
            if arr[i][j] == '6' or arr[i][j] == '7' or arr[i][j] == '8':    # if it belongs to row 2
                err += 2 - i                  # err += 2 - i         e.g. an element in row 1 has err 2-1 = 1
            if arr[i][j] == '3' or arr[i][j] == '6':    # for each item belonging to col 0, add the col to the error
                err += j                                # e.g. an element in col 2, belonging in col 0, adds error 2
            if arr[i][j] == '1' or arr[i][j] == '4' or arr[i][j] == '7':    # if it belongs in col 1
                err += abs(j - 1)             # err += abs(col-1)    e.g. an element in col 0 has err abs(0-1) = 1
            if arr[i][j] == '2' or arr[i][j] == '5' or arr[i][j] == '8':    # if it belongs to row 2
                err += 2 - j                  # err += 2 - i         e.g. an element in col 1 has err 2-1 = 1
    return err      # return the sum of the error


def h1(array):
    global maxN  # load in global val maxN
    arr = copy.deepcopy(array)  # create a modifiable copy of array
    pQueue = PriorityQueue()  # create a priority queue
    explored = set()  # create an explored set
    count = 1  # initialize the number of nodes expanded to 1

    pQueue.put((0 + h1Err(arr), arr, h1Err(arr), 0, count, []))  # add the initial tuple to the pQueue
    while not pQueue.empty():  # while pQueue has elements (hopefully always if truly complete)
        if count < maxN:  # check if max node have not been expanded
            if pQueue.queue[0][2] == 0:  # check if puzzle is finished
                return pQueue.get(), True  # return puzzle, true, if so
            else:
                # otherwise keep going
                while True:  # remove elements from pQueue until you find a state not in explored
                    curNode = pQueue.get()  # set the element to curNode and remove from pQueue
                    if str(curNode[1]) not in explored:  # if not in explored, add the state to explored & break
                        explored.add(str(curNode[1]))
                        break

                arr = curNode[1]  # set arr to the state of curNode
                movs = copy.deepcopy(curNode[5])  # create a copy of the moves up to this state
                b = copy.deepcopy(findB(arr))  # find the b val for this state
                moves = legalMoves(b)  # find the legal moves
                for m in moves:  # do the following for each legal move
                    arr2, b2 = copy.deepcopy(move(arr, m, b))  # set arr2, b2 to copy arr moved in dir m

                    boolean = False  # check if this state exists in pQueue with a similar g
                    for queue in pQueue.queue:
                        if queue[1] == arr2 and queue[3] <= curNode[3] + 1:
                            boolean = True

                    if not boolean:  # if not
                        movs2 = copy.deepcopy(movs)  # add the new move to an array and add the tuple to pQueue
                        movs2.append(m)
                        pQueue.put((curNode[3] + 1 + h1Err(arr2), arr2, h1Err(arr2), curNode[3] + 1, count, movs2))
                        if h1Err(arr2) == 0:
                            return (curNode[3] + 1 + h1Err(arr2), arr2, h1Err(arr2), curNode[3] + 1, count, movs2), True
                        count += 1  # one more node has now been generated

                    if pQueue.queue[0][2] == 0:  # check if solved and return if so
                        return pQueue.get(), True
        else:
            return pQueue.get(), False  # return the tuple, false if the max nodes have been generated

    return pQueue.get(), True  # return a tuple and true if there are no new nodes to be expanded (impossible)


def h2(array):
    global maxN     # load in global val maxN
    arr = copy.deepcopy(array)      # create a modifiable copy of array
    pQueue = PriorityQueue()    # create a priority queue
    explored = set()    # create an explored set
    count = 1   # initialize the number of nodes expanded to 1

    pQueue.put((0 + h2Err(arr), arr, h2Err(arr), 0, count, []))     # add the initial tuple to the pQueue
    while not pQueue.empty():   # while pQueue has elements (hopefully always if truly complete)
        if count < maxN:    # check if max node have not been expanded
            if pQueue.queue[0][2] == 0:     # check if puzzle is finished
                return pQueue.get(), True   # return puzzle, true, if so
            else:
                # otherwise keep going
                while True:     # remove elements from pQueue until you find a state not in explored
                    curNode = pQueue.get()      # set the element to curNode and remove from pQueue
                    if str(curNode[1]) not in explored:     # if not in explored, add the state to explored & break
                        explored.add(str(curNode[1]))
                        break

                arr = curNode[1]    # set arr to the state of curNode
                movs = copy.deepcopy(curNode[5])       # create a copy of the moves up to this state
                b = copy.deepcopy(findB(arr))       # find the b val for this state
                moves = legalMoves(b)       # find the legal moves
                for m in moves:     # do the following for each legal move
                    arr2, b2 = copy.deepcopy(move(arr, m, b))       # set arr2, b2 to copy arr moved in dir m

                    boolean = False     # check if this state exists in pQueue with a similar g
                    for queue in pQueue.queue:
                        if queue[1] == arr2 and queue[3] <= curNode[3] + 1:
                            boolean = True

                    if not boolean:     # if not
                        movs2 = copy.deepcopy(movs)     # add the new move to an array and add the tuple to pQueue
                        movs2.append(m)
                        pQueue.put((curNode[3] + 1 + h2Err(arr2), arr2, h2Err(arr2), curNode[3]+1, count, movs2))
                        if h2Err(arr2) == 0:        # if the node you added is the solution, return that
                            return (curNode[3] + 1 + h2Err(arr2), arr2, h2Err(arr2), curNode[3]+1, count, movs2), True
                        count += 1      # one more node has now been generated

                    if pQueue.queue[0][2] == 0:     # check if solved and return if so
                        return pQueue.get(), True
        else:
            return pQueue.get(), False      # return the tuple, false if the max nodes have been generated

    return pQueue.get(), True       # return a tuple and true if there are no new nodes to be expanded (impossible)


def aStar(heuristic, arr):
    b = findB(arr)      # find b for printing the moves later
    arr2 = copy.deepcopy(arr)       # create a modifiable copy of arr
    if heuristic == "h1":       # run h1 if applicable
        queue, boolean = h1(arr2)
    elif heuristic == "h2":     # run h2 if applicable
        queue, boolean = h2(arr2)
    else:     # if neither heuristics are inputted, return the original array (run an error later)
        queue, boolean = arr, True

    if str(queue[1]) == "[['b', '1', '2'], ['3', '4', '5'], ['6', '7', '8']]":      # check if solved (should be)
        print(queue[0])     # print the number of moves to solve
        printState(arr)     # print the states after each move (starting with the initial state)
        for i in queue[5]:
            arr, b = move(arr, i, b)
            printState(arr)
    elif not boolean:       # print if you expanded the maximum number of nodes
        print("You have generated the maximum number of nodes")
        return arr, b       # return original arr, b if not solved
    else:       # print if the puzzle was not solved and max nodes were not expanded
        print("Puzzle Failed? Perhaps Illegal heuristic.")
        return arr, b   # return original arr, b if not solved

    return queue[1], findB(queue[1])    # return queue, b if solved


def maxNodes(k):
    global maxN     # set global var maxN to k
    maxN = k


def beam(array, k):
    global maxN     # Use the global maxN var to stop generating new nodes based off of the designated cut-off
    arr = copy.deepcopy(array)      # make a deep copy of array, so we aren't changing the array that was inputted
    explored = set()       # Create a set that tracks the nodes that have already been explored

    pQueue = PriorityQueue()        # Create a priority queue to store the nodes in the frontier
    count = 1       # Start with the initial state as node 1
    pQueue.put((h2Err(arr), arr, count, []))        # Put the first tuple into the priority queue

    # Tuple Contents:
    #   h2Err(arr): the heuristic that I'm using for beam search
    #   arr: the state that the puzzle is in for any given node
    #   count: the number of nodes generated
    #   []: the moves taken to get to the current state from the initial state

    kStates = []       # kStates is an array that has up to k elements where each is a node that will be explored

    while len(pQueue.queue) > 0:   # loop until broken or pQueue is empty
        k2 = copy.deepcopy(k)      # create a k2 that we can change without changing k
        while 0 < k2:      # loop from 0->k2 filling kStates with the first item in the priority queue

            if not pQueue.empty():       # Only do this if priority queue is not empty

                if str(pQueue.queue[0][1]) not in explored:     # check if the array is in explored
                    kStates.append(pQueue.get())        # if not, append tuple to kStates
                    explored.add(str(kStates[0][1]))    # add state to explored
                    k2 -= 1     # decrement k2
                else:
                    lQueue = pQueue.get()   # random tuple that we return if there is no correct answer (not important)
                    k2 -= 1     # decrement k2

            else:   # if we get to the end of pQueue, before k2=0, set k2=0
                k2 = 0

        if len(kStates) == 0:   # if there are no legal moves that are new, return the random queue tuple
            return lQueue, True

        pQueue.queue.clear()    # Clear the pQueue

        for p in range(len(kStates)):   # loop through each element in kStates
            arr = copy.deepcopy(kStates[p][1])     # set the current array to a deep copy of that element's array
            movs = copy.deepcopy(kStates[p][3])    # set the list of moves (to reach the state) to the previous list
            b = copy.deepcopy(findB(arr))       # find b
            moves = legalMoves(b)       # find legal moves for that b
            for m in moves:
                arr2, b2 = copy.deepcopy(move(arr, m, b))      # create a copies of arr,b that we moved in dir m

                boolean = False     # check if arr2 is already in pQueue
                for q in pQueue.queue:
                    if q[1] == arr2:
                        boolean = True

                if not boolean:     # if arr2 is not in pQueue
                    movs2 = copy.deepcopy(movs)     #create a copy of the pervious moves
                    movs2.append(m)     # append new move m
                    pQueue.put((h2Err(arr2), arr2, count, movs2))      # add the new tuple to the pQueue
                    if h2Err(arr2) == 0:
                        return (h2Err(arr2), arr2, count, movs2), True
                    if h2Err(arr2) != 0 and count >= maxN:      # if the puzzle isn't solved, and count > maxN
                        return pQueue.get(), False      # return the first tuple, bool false
                    count += 1      # count += 1, means there has been one more node generated

                if pQueue.queue[0][0] == 0:     # check if puzzle s solved
                    return pQueue.get(), True      # return puzzle
        kStates = []        # empty kStates for the next iteration
    return pQueue.get(), True       # if there are no nodes to be expanded (impossible) return the first node and a bool

def doBeam(arr, k):
    b = findB(arr)      # find b location
    arr2 = copy.deepcopy(arr)   # create a modifiable copy of arr
    queue, boolean = beam(arr2, k)    # run beam search with the new arr

    if str(queue[1]) == "[['b', '1', '2'], ['3', '4', '5'], ['6', '7', '8']]":      # check if the puzzle was solved
        print(len(queue[3]))    # if so, print the number of moves to solve
        printState(arr)     # Print the original state
        for i in queue[3]:      # loop through the moves taken and print the state after each move
            arr, b = move(arr, i, b)
            printState(arr)
    elif not boolean:  # if boolean is false, the max number of nodes were expanded
        print("The maximum number of nodes were generated")
    else:  # if the puzzle was not solved, and the max nodes weren't expanded, the puzzle wasn't solvable (with my beam)
        print("The puzzle was not solved.")
        return arr, b   # return the original array and b val for future use

    return queue[1], findB(queue[1])    # return the array and b val for future use


for line in text:
    if line[0:8] == "setState":
        arr, b = setState(line[9:].strip())
    elif line[0:10] == "printState":
        printState(arr)
    elif line[0:4] == "move":
        arr, b = move(arr, line[5:].strip(), b)
    elif line[0:14] == "randomizeState":
        arr, b = randomizeState(line[15:].strip())
    elif line[0:11] == "solveA-star":
        arr, b = aStar(line[12:].strip(), arr)
    elif line[0:9] == "solvebeam":
        arr, b = doBeam(arr, int(line[10:].strip()))
    elif line[0:8] == "maxNodes":
        maxNodes(int(line[9:].strip()))
    else:
        print("Unrecognized Function. Sorry")
