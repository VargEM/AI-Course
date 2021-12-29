from scipy.spatial import distance
class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1]
#optional (just to have faster power but it was not very effectibe)
def fast_power(base, power):

    result = 1
    while power > 0:
        if power % 2 == 0:

            power = power // 2

            base = base * base
        else:

            power = power - 1
            result = result * base

            power = power // 2
            base = base * base

    return result

def astar(maze, start, end):
    open_list = []
    closed_list = []
    outer_iterations = 0
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0
    open_list.append(start_node)
    max_iterations = (len(maze) // 2) ** 2
    adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0),)

    while len(open_list) > 0:
        outer_iterations += 1

        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
                
        if outer_iterations > max_iterations:
            return return_path(current_node)

        open_list.pop(current_index)
        closed_list.append(current_node)

        if current_node == end_node:
            return return_path(current_node)

        children = []
        for new_position in adjacent_squares:

            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            within_range = [
                node_position[0] > (len(maze) - 1), node_position[0] < 0,
                node_position[1] > (len(maze[len(maze) - 1]) - 1), node_position[1] < 0,]
            
            if any(within_range):
                continue

            if maze[node_position[0]][node_position[1]] != '0':
                continue

            new_node = Node(current_node, node_position)
            children.append(new_node)

        for child in children:
            
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                continue
            child.g = current_node.g + 1
            
            #child.h = fast_power(child.position[0] - end_node.position[0], 8) + fast_power(child.position[1] - end_node.position[1], 8)
            child.h = ((child.position[0] - end_node.position[0]) ** 8) + \
                      ((child.position[1] - end_node.position[1]) ** 8)
            child.f = child.g + child.h

            if len([open_node for open_node in open_list if child == open_node and child.g > open_node.g]) > 0:
                continue

            open_list.append(child)

