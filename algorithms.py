from models import cell
import heapq
# from queue import PriorityQueue
import const

class MyPriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, qitem):
        heapq.heappush(self.elements, qitem)
    
    def get(self):
        return heapq.heappop(self.elements)[2]

        
def heuristic(cell, end):
    # Manhattan
    if const.noOfDirections == 4:
        return abs(end.i - cell.i) + abs(end.j - cell.j)

    # Chebyshev
    dx = abs(cell.i - end.i)
    dy = abs(cell.j - end.j)
    return max(dx, dy)
    # return (end.i - cell.i)**2 + (end.j - cell.j)**2

def bfs(grid, start, end, visitedOrder):
    queue = MyPriorityQueue()
    step = 0
    queue.put([0, step, start])
    start.visited = True
    cost = {}
    cost[(start.i, start.j)] = 0
    prev = {}
    prev[(start.i, start.j)] = None
    while not queue.empty():
        current = queue.get()
        if(current == end):
            end.visited = True
            break

        visitedOrder.append(current)

        for new in current.neighbors:
            newCost = cost[(current.i, current.j)] + 1
            if (new.i, new.j) not in cost or newCost < cost[(new.i, new.j)]:
                cost[(new.i, new.j)] = newCost
                step+=1
                queue.put([newCost, step, new])
                prev[(new.i, new.j)] = current
                new.visited = True

    
    node = end
    while (node.i, node.j) in prev and prev[(node.i, node.j)] is not None:
        node.previous = prev[(node.i, node.j)]
        node = prev[(node.i, node.j)]

def dfs(grid, start, end, visitedOrder):
    start.visited = True
    prev = {}
    prev[(start.i, start.j)] = None
    def look(current):
        if(current == end):
            end.visited = True
            return True

        visitedOrder.append(current)

        for new in current.neighbors:
            if (new.i, new.j) not in prev:
                prev[(new.i, new.j)] = current
                if look(new):
                    return True

    look(start)
    node = end
    while (node.i, node.j) in prev and prev[(node.i, node.j)] is not None:
        node.previous = prev[(node.i, node.j)]
        node = prev[(node.i, node.j)]


def astar(grid, start, end, visitedOrder):
    queue = MyPriorityQueue()
    step = 0
    queue.put([0, step, start])
    came_from = {}
    cost_so_far = {}
    came_from[(start.i, start.j)] = None
    cost_so_far[(start.i, start.j)] = 0 

    
    while not queue.empty():
        current = queue.get()
        if current == end:
            end.visited = True
            break

        visitedOrder.append(current)

        for next in reversed(current.neighbors):
            new_cost = cost_so_far[(current.i, current.j)] + heuristic(next, current)
            if (next.i, next.j) not in cost_so_far or new_cost < cost_so_far[(next.i, next.j)]:
                cost_so_far[(next.i, next.j)] = new_cost
                priority = new_cost + heuristic(next, end)
                step -=1
                queue.put([priority, step, next])
                came_from[(next.i, next.j)] = current
    
    node = end
    while (node.i, node.j) in came_from and came_from[(node.i, node.j)] is not None:
        node.previous = came_from[(node.i, node.j)]
        node = came_from[(node.i, node.j)]