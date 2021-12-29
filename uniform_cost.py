from queue import PriorityQueue

def uniform_cost_(size, start, goal, values, walls):
    frontiers = PriorityQueue()
    path = []
    visited_cell = []
    sum_cost = 0
    frontiers.put((sum_cost, [start]))

    while frontiers.empty() == False:
        frontier_expand = tuple(frontiers.get(-1))
        sum_cost = frontier_expand[0]
        path = list(frontier_expand[1])
        frontier_location = path[-1]
        visited_cell.append(frontier_location)
        
        if frontier_location == goal:
            return path
        if frontier_location in walls:
            continue

        else:
            row_idx = frontier_location[0]
            col_idx = frontier_location[1]

            if row_idx != 0 and (int(row_idx) - 1, int(col_idx)) not in visited_cell:
                cost = sum_cost + int(values[int(row_idx) - 2][int(col_idx) - 1]) + 1
                frontier_path = list(path)
                frontier_path.append((int(row_idx) - 1, int(col_idx)))
                frontier = (cost, frontier_path)
                frontiers.put(frontier)

            if col_idx != 0 and (int(row_idx), col_idx - 1) not in visited_cell:
                cost = sum_cost + int(values[int(row_idx) - 1][int(col_idx) - 2]) + 1
                frontier_path = list(path)
                frontier_path.append((int(row_idx), int(col_idx) - 1))
                frontier = (cost, frontier_path)
                frontiers.put(frontier)

            if row_idx != size and (int(row_idx) + 1, int(col_idx)) not in visited_cell:
                cost = sum_cost + int(values[int(row_idx)][int(col_idx) - 1]) + 1
                frontier_path = list(path)
                frontier_path.append((int(row_idx) + 1, int(col_idx)))
                frontier = (cost, frontier_path)
                frontiers.put(frontier)

            if col_idx != size and (int(row_idx), int(col_idx) + 1) not in visited_cell:
                cost = sum_cost + int(values[int(row_idx) - 1][int(col_idx)]) + 1
                frontier_path = list(path)
                frontier_path.append((int(row_idx), int(col_idx) + 1))
                frontier = (cost, frontier_path)
                frontiers.put(frontier)