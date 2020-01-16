# from path_finding import cell

from models import cell

def bfs(grid, noOfColumns, noOfRows, start, end, visitedOrder):
    queue = [start]
    start.visited = True
    while queue:
        current = queue[0]
        queue.pop(0)
        if(current != start):
            visitedOrder.append(current)

        for new in current.neighbors:
            if new == end:
                end.previous = current
                end.visited = True
                return
            if new.isObstacle == False and new.visited == False:
                queue.append(new)
                new.previous = current
                #visitedOrder.append(new)
                new.visited = True

                
