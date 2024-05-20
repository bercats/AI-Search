class astar_queue():
    def __init__(self):
        self.queue = []
        self.queue.append((
            0,  # f is the cost of the path from the start node to the goal node basically g + h
            0,  # g is for the cost of the path from the start node to n
            0,  # h is the heuristic estimate of the cost from n to the goal
            (0, 0),  # position
            None  # parent
        ))

    def push(self, f, g, h, position, parent):
        self.queue.append((f, g, h, position, parent))
        self.queue.sort()

    def pop(self):
        return self.queue.pop(0)

    def is_empty(self):
        return len(self.queue) == 0

class astar():
    def __init__(self, map):
        self.map = map
        self.queue = astar_queue()
        self.visited = []
        self.path = [] # path from start to goal
        self.width = len(map[0]) # number of columns
        self.height = len(map) # number of rows

    def heuristic_manhattan(self, position, goal):
        return abs(position[0] - goal[0]) + abs(position[1] - goal[1])

    def get_neighbors(self, position):
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Left, Right, Down, Up

        for direction in directions:
            x, y = position[0] + direction[0], position[1] + direction[1]

            if x < 0 or x >= self.height or y < 0 or y >= self.width:  # out of bounds
                continue

            if self.map[x][y] == 1:  # blocked
                continue

            neighbors.append((x, y))  # valid neighbor

        return neighbors

    def reconstruct_path(self, current_node):
        path = []
        while current_node is not None:
            path.append(current_node[3]) # position is the 4th element in the tuple
            current_node = current_node[4] # parent is the 5th element in the tuple
        return path[::-1] # reverse the path as we built it from goal to start

    def run(self, start, goal):
        # Initialize the start node and add it to the queue
        self.queue.push(0 + self.heuristic_manhattan(start, goal), 0, self.heuristic_manhattan(start, goal), start, None)
        self.visited.append(start)

        while not self.queue.is_empty():
            current_f, current_g, current_h, current_position, current_parent = self.queue.pop()

            # Check if we have reached the goal
            if current_position == goal:
                return self.reconstruct_path((current_f, current_g, current_h, current_position, current_parent))

            neighbors = self.get_neighbors(current_position) # Get the neighbors of the current node
            for neighbor in neighbors:
                if neighbor in self.visited:
                    continue

                neighbor_g = current_g + 1 # cost from current to neighbor is 1
                neighbor_h = self.heuristic_manhattan(neighbor, goal)
                neighbor_f = neighbor_g + neighbor_h

                # Add neighbor to the queue if not visited or if we found a shorter path to it
                if neighbor not in self.visited or self.queue[neighbor][1] > neighbor_g:
                    self.queue.push(neighbor_f, neighbor_g, neighbor_h, neighbor, (current_f, current_g, current_h, current_position, current_parent))
                    self.visited.append(neighbor)
        return [] # return an empty path if goal not found

def read_locations(file_path): # Read the locations from a file
    locations = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            name = parts[0]
            coordinates = (int(parts[1]), int(parts[2]))
            locations[name] = coordinates
    return locations

def calculate_distances(locations, map_data): # Calculate the distances between all pairs of locations
    names = sorted(locations.keys())
    distances = []
    for i, name1 in enumerate(names):
        for name2 in names[i+1:]:
            # Create a new instance of astar for each search to ensure a clean state without visited nodes
            astar_instance = astar(map_data)
            path = astar_instance.run(locations[name1], locations[name2])
            if path:  # If a path is found
                distance = len(path) - 1
                distances.append((name1, name2, distance, path))
            else:  # If no path is found, we can indicate it with a message or a special value
                print(f"No path found between {name1} and {name2}")
    return distances

def print_distances(distances, map):
    for name1, name2, distance, path in distances:
        print(f"{name1},{name2},{distance}, \nPath: {path}")

def distances_to_graph(distances): # Convert the distances to a graph data structure
    graph = {}
    for name1, name2, distance, path in distances: # Add the distances to the graph
        if name1 not in graph:
            graph[name1] = {}
        if name2 not in graph:
            graph[name2] = {}
        graph[name1][name2] = distance
        graph[name2][name1] = distance
    return graph

def print_path_on_map(map, path):
    for y, row in enumerate(map):
        for x, cell in enumerate(row):
            if (x, y) in path:
                print('*', end='')
            else:
                print(cell, end='')
        print()

def print_graph(graph):
    print('\nState Graph of Shortest Paths:')
    for node in graph:
        print(f"{node}: {graph[node]}")



class queue():
    #queue class for the depth first and uniform cost search
    def __init__(self):
        self.queue = []

    def push(self, node):
        self.queue.append(node)

    def pop(self):
        return self.queue.pop(0)

    def is_empty(self):
        return len(self.queue) == 0

    def sort(self):
        self.queue.sort(key = lambda x: x[0]) # Sort the queue based on the cost of the path

def depth_first_search(graph, start):
    q = queue()
    q.push(start)
    visited = []
    while not q.is_empty():
        node = q.pop()
        if node in visited:
            continue
        visited.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                q.push(neighbor)
    return visited

def uniform_cost_search(graph, start):
    q = queue()
    q.push((0, [start]))  # Push the initial state to the queue

    while not q.is_empty():
        q.sort()  # Sort the queue by cost
        cost, path = q.pop()  # Remove the first path from the queue

        last_node = path[-1] # Get the last node in the path
        if len(path) > 1 and last_node == start:
            if len(path[:-1]) == len(graph): # Check if all nodes are visited except the start node
                return path, cost

        for neighbor, distance in graph[last_node].items(): # Get the neighbors of the last node
            if neighbor not in path or (len(path) == len(graph) and neighbor == start):  # Check if the neighbor is not visited to prevent loops
                new_path = path + [neighbor] # Add the neighbor to the path
                new_cost = cost + distance # Add the distance to the cost
                q.push((new_cost, new_path))  # Add new paths to the queue

    return None  # Return None if no complete path is found


def read_map(file_path):
    with open(file_path, 'r') as file:
        map = []
        for line in file:
            row = [int(cell) for cell in line.strip().split(',')]
            map.append(row)
        return map

def print_map(map):
    print("\nMap:")
    for row in map:
        print(row)

def main():
    locations = "nodes.txt"
    map = "map.txt"
    while True:
        print("\nMenu:")
        print("1. Read Locations and map from Files")
        print("2. Calculate Distances")
        print("3. Print Distances")
        print("4. Perform Depth First Search")
        print("5. Perform Uniform Cost Search")
        print("6. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            locations = read_locations("nodes.txt")
            map_data = read_map("map.txt")
            print_map(map_data)
        elif choice == '2':
            distances = calculate_distances(locations, map_data)
            graph = distances_to_graph(distances)
        elif choice == '3':
            print_distances(distances, map_data)
            print_graph(graph)
        elif choice == '4':
            start = input("Enter the start node: ")
            visited = depth_first_search(graph, start)
            print(f"Path: {visited}")
        elif choice == '5':
            start = input("Enter the start node: ")
            path, cost = uniform_cost_search(graph, start)
            if path:
                print(f"Path: {path}")
                print(f"Cost: {cost}")
            else:
                print("No path found")
        elif choice == '6':
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()