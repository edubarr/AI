import random

def valid_state(path, distances):
    for i in range(len(path) - 1):
        if(distances[path[i]][path[i + 1]] != -1):
            i = i + 1
        else:
            return 0
        
    return 1

def random_path(distances):
    cities = list(range(len(distances)))

    path = []

    for i in range(len(distances)):
        random_city = cities[random.randint(0, len(cities) - 1)]

        path.append(random_city)
        cities.remove(random_city)

    if(valid_state(path, distances)):
        return path
    else:
        return random_path(distances)

def path_distance(path, distances):
    path_distance = 0
    for i in range(len(path)):
        path_distance += distances[path[i - 1]][path[i]]
    
    return path_distance

def generate_neighbours(path, distances):
    neighbours = []

    for i in range(len(path)):
        for j in range(i + 1, len(path)):
            neighbour = path.copy()

            neighbour[i] = path[j]
            neighbour[j] = path[i]

            if(valid_state(neighbour, distances)):
                neighbours.append(neighbour)
            else:
                i = i + 1
    
    return neighbours

def get_shortest_neighbour(neighbours, distances):
    shortest_path_distance = path_distance(neighbours[0], distances)
    shortest_neighbour = neighbours[0]

    for neighbour in neighbours:
        current_path_distance = path_distance(neighbour, distances)

        if current_path_distance < shortest_path_distance:
            shortest_path_distance = current_path_distance
            shortest_neighbour = neighbour
    return shortest_neighbour, shortest_path_distance

def hill_climbing(distances):
    current_path = random_path(distances)
    current_path_distance = path_distance(current_path, distances)

    neighbours = generate_neighbours(current_path, distances)

    shortest_neighbour, shortest_neighbour_distance = get_shortest_neighbour(neighbours, distances)

    while shortest_neighbour_distance < current_path_distance:
        current_path = shortest_neighbour
        current_path_distance = shortest_neighbour_distance

        neighbours = generate_neighbours(current_path, distances)
        shortest_neighbour, shortest_neighbour_distance = get_shortest_neighbour(neighbours, distances)

    for i in range(len(current_path)):
        print("- C", current_path[i] + 1, " ", end='', sep='')

    print("-\nTotal percorrido = ", current_path_distance)

    return

def main():

    distances = [[0, 30, 84, 56, -1, -1, -1, 75, -1, 80],
              [30, 0, 65, -1, -1, -1, 70, -1, -1, 40],
              [84, 65, 0, 74, 52, 55, -1, 60, 143, 48],
              [56, -1, 74, 0, 135, -1, -1, 20, -1, -1],
              [-1,  -1, 52, 135, 0, 70, -1, 122, 98, 80],
              [70, -1, 55, -1, 70, 0, 63, -1, 82, 35],
              [-1, 70, -1, -1, -1, 63, 0, -1, 120, 57],
              [75, -1, 135, 20, 122, -1, -1, 0, -1, -1],
              [-1, -1, 143, -1, 98, 82, 120, -1, 0, -1],
              [80, 40, 48, -1, 80, 35, 57, -1, -1, 0]]

    hill_climbing(distances)

if __name__ == "__main__":
    main()
