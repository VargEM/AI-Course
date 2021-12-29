import numpy as np
import sys
import random
import argparse as ap
from math import e
from scipy.spatial import distance
delta_E = lambda E1, E2: E1 - E2

def value(current, goal, maze, kn, a, b):
    print('current' , current)
    print('goal' , goal)
    print('woho',current)
    D = distance.euclidean(current, goal)
    print('fucking', D)
    NS = 0
    for i in kn:
        if maze[i[0]][i[1]] == "1":
            
            #NS += distance.euclidean(current, i)-1
            NS += (current[0] - i[0])**2 - 1
        else:
            #NS += (goal[0] - i[0])**2
            NS += distance.euclidean(current, i)
    print("NS BEFORE SURGERY", NS)
    NS = NS / len(kn)
    print("NS AFTER SURGERY", NS)
    O = (a * 1/(D + np.finfo(float).eps)) + (b * NS)
    print("O", O)
    return O
def knn(current, neighbors, k):
    nearest = neighbors[current]

    for i in nearest:
        nearest.extend(neighbors[i])
        if len(set(nearest)) < k + 5 and len(set(nearest))> k:
            break
    
    nearest = set(nearest)
    print('vavaviva', nearest)
    return nearest

def find_neighbours(arr):

    #neighbors = []
    neighbors = {}
    for i in range(len(arr)):
        for j, value in enumerate(arr[i]):

            if i == 0 or i == len(arr) - 1 or j == 0 or j == len(arr[i]) - 1:
                # corners
                new_neighbors = []
                if i != 0:
                    new_neighbors.append((i - 1,j))  # top neighbor
                if j != len(arr[i]) - 1:
                    new_neighbors.append((i, j + 1))  # right neighbor
                if i != len(arr) - 1:
                    new_neighbors.append((i + 1, j))  # bottom neighbor
                if j != 0:
                    new_neighbors.append((i, j - 1))  # left neighbor
    
            else:
                new_neighbors = []
                # add neighbors
                new_neighbors.append((i - 1, j))

                new_neighbors.append((i, j + 1))

                new_neighbors.append((i + 1 ,j))

                new_neighbors.append((i, j - 1))

            neighbors[(i, j)] = new_neighbors

    print("neighbors", neighbors)
    return neighbors
        


def probability(dE, T):
    k = 1e-2
    exp = - (dE / (k * T))
    return e ** exp

def is_better(maze, s1, s2, kn, goal, toprint = True):
    '''function which tells if state s1 if better than state s2'''
    val1 = value(s1, goal, maze, kn, 0.5, 0.5)
    val2 = value(s2, goal, maze, kn, 0.5, 0.5)
    
    if val1 == val2:
        return s1[0] > s2[0]
    if toprint:
        print("{} : {} > {} : {}".format(s1, val1, s2, val2))
    return bool(val1 > val2)


def nextstate(maze, start_state, current_state, goal_state):
    a = []
    '''gives the next states of maze'''
    if current_state[0] != 0:
        if current_state != start_state and maze[current_state[0] - 1][current_state[1]] == "0":
            print("111")
            print("well1", (current_state[0] - 1, current_state[1]))
            #yield (current_state[0] - 1, current_state[1])
            a.append((current_state[0] - 1, current_state[1]))
            
            
            
    if current_state[1] != len(maze) - 1:
        if maze[current_state[0]][current_state[1] + 1] == "0":
            print("well2", (current_state[0], current_state[1] + 1))
            print("222")
            #yield (current_state[0], current_state[1] + 1)
            a.append((current_state[0], current_state[1] + 1))
            
            
    if current_state[0] != len(maze) - 1:
        if current_state != goal_state and maze[current_state[0] + 1][current_state[1]] == "0":
            print("333")
            print("well3", (current_state[0] + 1, current_state[1]))
            
            #yield (current_state[0] + 1, current_state[1])
            a.append((current_state[0] + 1, current_state[1]))
            
            
            
    if current_state[1] != 0:
        if maze[current_state[0]][current_state[1] - 1] == "0":
            print("444")
            print("well4", (current_state[0], current_state[1] - 1))
            #yield (current_state[0], current_state[1] - 1)
            a.append((current_state[0], current_state[1] - 1))
    print("A", a)
    return a


def simulated_annealing(maze, start, current, end):
    neighborrs = find_neighbours(maze)
    kn = knn(current, neighborrs, 7)
    current_state = start
    goal_state = end
    path = [current_state]
    print("path", path)
    test_path = []
    T = 200
    prev = None
    while current_state != goal_state:
        found = False
        E1 = value(current_state, goal_state, maze, kn, 0.5, 0.5)
        P = True
        l = nextstate(maze, start, current_state, goal_state)
        for state in l:
            if P:
                P = False
            if state == prev:
                continue
            E2 = value(state, goal_state, maze, kn, 0.5, 0.5)
            if state == goal_state:
                path.append(state)
                
                return path
            
            if is_better(maze, state, current_state, kn, goal_state):
                path.extend(test_path)
                path.append(state)
                test_path = []
                prev = current_state
                current_state = state
                found = True
                print("path_isbetter", path)
                break
            else:
                p = probability(delta_E(E2, E1), T)
                if p < random.random():
                    found = True
                    test_path.append(state)
                    prev = current_state
                    current_state = state
                    break
            
        if not found:
            print("pathhhhhh", path)
            return path
        
        T = 0.9 * T
    return set(path)
