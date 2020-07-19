ROW = 9
COL = 10


class cell:
    def __init__(self, parent=None, position=None):
        self.position = position
        self.parent = parent
        self.f = 0.0
        self.g = 0.0
        self.h = 0.0

    def __eq__(self, other):
        return self.position == other.position


def isValid(pos):
    i = pos[0]
    j = pos[1]
    return (i >= 0 and j >= 0) and (i < ROW and j < COL)


def calHeuristic(cell_now, dest):
    return (cell_now.position[0] - dest[0]) ** 2 + (cell_now.position[1] - dest[1]) ** 2


def Astar(grid, start, dest):
    if not isValid(start) or grid[start[0]][start[1]] == 0:
        print("INVALID START")
        return None
    if not isValid(dest) or grid[dest[0]][dest[1]] == 0:
        print("INVALID DESTINATION")
        return None
    start_cell = cell(None, start)
    start_cell.f = start_cell.g = start_cell.h = 0
    dest_cell = cell(None, dest)
    dest_cell.f = dest_cell.g = dest_cell.h = 0

    open_list = []
    closed_list = []

    open_list.append(start_cell)

    while len(open_list) > 0:
        cur_cell = open_list[0]
        cur_idx = 0
        for index, item in enumerate(open_list):
            if item.f < cur_cell.f:
                cur_cell = item
                cur_idx = index

        open_list.pop(cur_idx)
        closed_list.append(cur_cell)

        if cur_cell == dest_cell:
            path = []
            cur = cur_cell
            while cur is not None:
                path.append(cur.position)
                cur = cur.parent
            return path[::-1]

        children = []

        for new_pos in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            cell_pos = (cur_cell.position[0] + new_pos[0], cur_cell.position[1] + new_pos[1])

            if not isValid(cell_pos):
                continue

            if grid[cell_pos[0]][cell_pos[1]] == 0:
                continue

            new_cell = cell(cur_cell, cell_pos)
            children.append(new_cell)

        for child in children:
            flag = True
            for closed_child in closed_list:
                if child == closed_child:
                    flag = False
                    continue
            if flag:
                child.g = cur_cell.g + 1.0
                child.h = calHeuristic(child, dest)
                child.f = child.g + child.h
                for open_cell in open_list:
                    if child == open_cell:
                        if child.f < open_cell.f:
                            open_cell.f = child.f
                            open_cell.parent = child.parent
                        flag = False
                if flag:
                    open_list.append(child)

    return None


def main():
    grid = [
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 1],  # 0
        [1, 1, 1, 0, 1, 1, 1, 0, 1, 1],  # 1
        [1, 1, 1, 0, 1, 1, 0, 1, 0, 1],  # 2
        [0, 0, 1, 0, 1, 0, 0, 0, 0, 1],  # 3
        [1, 1, 1, 0, 1, 1, 1, 0, 1, 0],  # 4
        [1, 0, 1, 1, 1, 1, 0, 1, 0, 0],  # 5
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],  # 6
        [1, 0, 1, 1, 1, 1, 0, 1, 0, 0],  # 7
        [1, 1, 1, 0, 0, 0, 1, 0, 0, 1]  # 8
        # 0 1  2  3  4  5  6  7  8  9
    ]

    start = (8, 0)
    dest = (4, 4)  # 8 9
    path = Astar(grid, start, dest)
    if path:
        print("PATH is", end=" ")
        for i in path:
            print("->", end="")
            print(i, end=" ")
    else:
        print("Path does not exist")


main()
