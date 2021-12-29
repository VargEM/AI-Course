import random
from base import BaseAgent, TurnData, Action
import numpy as np
import operator
from Astar import astar
from scipy.spatial import distance
import time
import matplotlib.pyplot as plt
from uniform_cost import uniform_cost_
diamonds_num = 5
from SA import simulated_annealing
from SDHC import steepest_ascent_hill_climbing
from base import __IS__THIS__GONNA__CONTINUE__
from RL import Field, QLearning_Solver, DQN_Solver
from functools import partial
force_decimal = partial(int, base=10)

#function to return shortest distance between a position and all elements of a list 
def short_distance(a, b):
    ret = min(b, key=lambda c : distance.euclidean(c, a))
    return ret
#function find diamond locations
def diamonds_pos(grid_map):
    _map = np.array(grid_map)
    diamonds = {}
    for i in range(diamonds_num):
        a = list(zip(*np.where(_map == str(i))))
        if len(a) == 0:
            pass
        else:
            
            for j in a:
                diamonds[j] = i

    return diamonds


def agentSD(grid_map, pos, diam):
    for k, v in diam.items():
        print("kkk", k, "vvvv", type(v))
        if v == 0:
            grid_map[k[0]][k[1]] = str(2)
        if v == 1:
            grid_map[k[0]][k[1]] = str(5)
        if v == 2:
            grid_map[k[0]][k[1]] = str(3)
        if v == 3:
            grid_map[k[0]][k[1]] = str(1)
        if v == 4:
            grid_map[k[0]][k[1]] = str(10)
            
            
    grid_map[pos[0]][pos[1]] = 0
    #grid_map[dest[0]][dest[1]] = 50
    for i in grid_map:
        for j in range(len(i)):
            if i[j] == '0':
                i[j] = 0
                
    return grid_map



def agentSD2(grid_map, pos, dest, carry):
    for i in dest:
        grid_map[i[0]][i[1]] = 5
    
    for i in grid_map:
        for j in range(len(i)):
            if i[j] == '0':
                i[j] = 0
                
    return grid_map
        
#function to change diamonds to 0
def delete_diamonds(grid_map ,diam):
    
    for i in diam:
        grid_map[i[0]][i[1]] = 0
    return grid_map
     
#function find destination
def destination_pos(grid_map):
    _map = np.array(grid_map)
    destination = list(zip(*np.where(_map == 'a')))
    
    print("desttttt", destination)
    return destination

#function to delete something
def delete_stars(grid_map):
    _map = np.array(grid_map)
    for i in range(len(_map)):
        _map[i] = np.where(_map[i] == '*', "#", _map[i])
        _map[i] = np.where(_map[i] == 'a', 0, _map[i])
        _map[i] = np.where(_map[i] == '.', 0, _map[i])
    return _map

def walls(grid_map):
    _map = np.array(grid_map)
    wall = np.where(_map == '*')
    wall_list = [(wall[0][i], wall[1][i]) for i in range(len(wall[0]))]
    return wall_list
    
'''
def extract_rl_path(qtable, start, goal):
    path = [start]

    for i in path:
        m = max(qtable.items(), key=operator.itemgetter(1))[0]
        if m == 'left':
            z = (i[0], i[1]-1)
            path.append(z)
            if z == goal:
                break
    
        if m == 'right':
            z = (i[0], i[1]+1)
            path.append(z)
            if z == goal:
                break
        if m == 'up':
            z = (i[0]-1, i[1])
            path.append(z)
            if z == goal:
                break
        if m == "down":
            z = (i[0]+1, i[1])
            path.append(z)
            if z == goal:
                break
    print("ext path:",path)
    return path
'''


    


def action(tup):
    b = []
    for i in range(len(tup) - 1):
        a = tuple(map(operator.sub, tup[i+1], tup[i]))
        if (a == (0, 1)):
            a = 'R'
        elif (a == (0, -1)):
            a = 'L'
        elif (a == (1, 0)):
            a = 'D'
        elif (a == (-1, 0)):
            a = 'U'
        else:pass
        b.append(a)
    return b

    
class Agent(BaseAgent):
    
    def __init__(self):
        BaseAgent.__init__(self)
        print(f"MY NAME: {self.name}")
        print(f"PLAYER COUNT: {self.agent_count}")
        print(f"GRID SIZE: {self.grid_size}")
        print(f"MAX TURNS: {self.max_turns}")
        print(f"DECISION TIME LIMIT: {self.decision_time_limit}")

    
    def do_turn(self, turn_data: TurnData) -> Action:
        t1 =  time.perf_counter() 
        print(f"TURN {self.max_turns - turn_data.turns_left}/{self.max_turns}")
        for agent in turn_data.agent_data:
            print(f"AGENT {agent.name}")
            print(f"POSITION: {agent.position}")
            print(f"CARRYING: {agent.carrying}")
            print(f"COLLECTED: {agent.collected}")
        print(turn_data.map)
        print('-------------')
        #time.sleep(1)
        
        if agent.carrying == None:
            
            #magic happens here
            destination = destination_pos(turn_data.map)
            print('destination',destination)
            diamond = diamonds_pos(turn_data.map)
            print('diamond', diamond)
            #dest = (short_distance(agent.position, diamond))
            wall = walls(turn_data.map)
            new_map = delete_stars(turn_data.map)
            print('new_map', new_map)
            new_map = delete_diamonds(new_map, diamond)
            new_map = new_map.tolist()
            print('new_map', new_map)
            new_map = agentSD(new_map, agent.position, diamond)
            print('new_map', new_map)
            start = [agent.position[0], agent.position[1]]
            #dest = [dest[0], dest[1]]
            "QLEARNING"
            Q = []
            for i in diamond:
                print("sooo", i)
                maze_field = Field(new_map, agent.position, [i[0], i[1]])
                maze_field.display()
                learning_count = 1000
                QL_solver = QLearning_Solver(maze_field, display=True)
                for i in range(learning_count):
                    QL_solver.qlearn()
                QL_solver.dump_Qvalue()
                qpath1 = QL_solver.qlearn(greedy_flg=True)
                Q.extend([qpath1])
            path1 = min(Q, key=len)
                
            "QLEARNING"
            
            
            "DQN"
            #maze_field = Field(new_map, agent.position, dest)
            #maze_field.display()
            #episodes = 20000
            #times = 1000
            #dql_solver = DQN_Solver(maze_field, agent.position, state_size=2, action_size=2, episodes=episodes, times=times)

            #qpath1 = dql_solver.solve()
            
            actions = action(path1)

            
        else:
            
            wall = walls(turn_data.map)
            destination = destination_pos(turn_data.map)
            new_map = delete_stars(turn_data.map)
            dest = short_distance(agent.position, destination)
            print('desttttdest' ,destination)
            new_map = new_map.tolist()
            new_map = agentSD2(new_map, agent.position, destination)
            
            start = [agent.position[0], agent.position[1]]
            dest = [dest[0], dest[1]]
            print("goddman dest", dest)
            maze_field = Field(new_map, agent.position, destination)
            maze_field.display()
            print(maze_field)
            learning_count = 1000

            QL_solver = QLearning_Solver(maze_field, display=True)
            for i in range(learning_count):
                QL_solver.qlearn()
            QL_solver.dump_Qvalue()
            qpath2 = QL_solver.qlearn(greedy_flg=True)
            '''agorithms are here, just uncomment one of them and comment the other'''
            #path2 = steepest_ascent_hill_climbing(new_map, agent.position, agent.position, dest)
            
            #qpath3 = extract_rl_path(qpath3)
            #simulated_path1 = simulated_annealing(new_map, agent.position, agent.position, dest)

            #path2 = astar(new_map, agent.position, dest)
            #path2 = uniform_cost_(self.grid_size, agent.position, dest, new_map, wall)
            actions = action(qpath2)
            print("actions:", actions)
        
        #for row in new_map:
           # print(''.join(row))
        #action_name = input("> ").upper()
        
        #t2 =  time.perf_counter()
        '''
        if ((t2 - t1) > self.decision_time_limit):

            __IS__THIS__GONNA__CONTINUE__ = 0 ;
            return Action.NONE;
        else:
        '''
        acts = []
        for action_name in actions:
            if action_name == "U":
                acts.append(Action.UP)
                #return Action.UP
            if action_name == "D":
                acts.append(Action.DOWN)
                #return Action.DOWN
            if action_name == "L":
                acts.append(Action.LEFT)
                #return Action.LEFT
            if action_name == "R":
                acts.append(Action.RIGHT)
                #return Action.RIGHT
        #print("acts: ", acts)
        return acts
                
                
            #return random.choice(list(Action))


if __name__ == '__main__':
    start_time =  time.perf_counter() 
    winner = Agent().play()
    end_time = time.perf_counter()
    print (end_time - start_time, "seconds")
    print("WINNER: " + winner)
