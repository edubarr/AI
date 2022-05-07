class node:
    def __init__(self, id, adjs, stations):
        self.father = None
        self.station = None

        self.cost = 0
        self.weight = 0
        self.id = id

        self.adj = []
        for adj in adjs:
            self.adj.append(adj)

        self.stations = []
        for station in stations:
            self.stations.append(station)

    def check_solution(self, destiny_node):
        if self.id == destiny_node.id:
            return True

        return False

    def check_stations(self, node):
        for station in node.stations:
            if station in self.stations:
                if self.station == None:
                    self.station = station

                node.station = station
                break

        if node.station == self.station:
            return 0

        return 4

    def generate_sons(self, frontier, visiteds, nodes, heuristic):
        for i in range(14):
            if self.adj[i] != 0 and visiteds[i] == 0:
                node = nodes[i]

                node.father = self

                add_station = self.check_stations(node)

                node.cost = self.cost + self.adj[i] + add_station
                node.weight = heuristic[i] + node.cost

                inserted = 0

                for j in range(len(frontier)):
                    if node.weight < frontier[j].weight:
                        frontier.insert(j, node)
                        inserted = 1
                        break

                if inserted == 0:
                    frontier.append(node)


class solve:
    def __init__(self, origin, destiny, nodes, heuristic):
        self.heuristic = []
        for each in heuristic:
            self.heuristic.append(each)

        self.nodes = []
        for each in nodes:
            self.nodes.append(each)

        self.destiny = destiny
        self.frontier = [origin]
        self.visiteds = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.path = []

    def print_path(self):
        print("Melhor caminho:")
        for node in self.path:
            print("Estação: {} Tempo acumulado (minutos): {}".format(node.id + 1, node.cost))

    def run_a_star(self):
        while True:
            node = self.frontier.pop(0)
            if self.visiteds[node.id] == 1:
                continue

            if node.check_solution(self.destiny):
                while node.father != None:
                    self.path.insert(0, node)
                    node = node.father
                break
            else:
                node.generate_sons(
                    self.frontier, self.visiteds, self.nodes, self.heuristic
                )
                self.visiteds[node.id] = 1


def main():
    heuristics = [
        [0, 22, 40, 54, 80, 86, 78, 56, 36, 20, 36, 60, 60, 64],
        [22, 0, 18, 32, 58, 64, 56, 38, 22, 8, 34, 46, 42, 48],
        [40, 18, 0, 14, 40, 44, 38, 30, 20, 22, 42, 42, 26, 36],
        [54, 32, 14, 0, 26, 32, 24, 26, 26, 36, 52, 42, 22, 34],
        [80, 58, 40, 26, 0, 6, 4, 42, 50, 62, 76, 54, 32, 40],
        [86, 64, 44, 32, 6, 0, 8, 46, 56, 66, 82, 60, 34, 40],
        [78, 56, 38, 24, 4, 8, 0, 44, 50, 58, 76, 56, 26, 34],
        [56, 38, 30, 26, 42, 46, 44, 0, 18, 44, 36, 14, 50, 60],
        [36, 22, 20, 26, 50, 56, 50, 18, 0, 26, 24, 24, 46, 56],
        [20, 8, 22, 36, 62, 66, 58, 44, 26, 0, 40, 54, 40, 46],
        [36, 34, 42, 52, 76, 82, 76, 36, 24, 40, 0, 30, 70, 78],
        [60, 46, 42, 42, 54, 60, 56, 14, 24, 54, 30, 0, 62, 74],
        [60, 42, 26, 22, 32, 34, 26, 50, 46, 40, 70, 62, 0, 10],
        [64, 48, 36, 34, 40, 40, 34, 60, 56, 46, 78, 74, 10, 0],
    ]

    costs = [
        [0, 22, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [22, 0, 18, 0, 0, 0, 0, 0, 22, 8, 0, 0, 0, 0],
        [0, 18, 0, 14, 0, 0, 0, 0, 0, 20, 0, 0, 26, 0],
        [0, 0, 14, 0, 26, 0, 0, 26, 0, 0, 0, 0, 22, 0],
        [0, 0, 0, 26, 0, 6, 4, 42, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 26, 42, 0, 0, 0, 18, 0, 0, 14, 0, 0],
        [0, 22, 20, 0, 0, 0, 0, 18, 0, 0, 24, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 24, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 14, 0, 0, 0, 0, 0, 0],
        [0, 0, 26, 22, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0],
    ]

    origin = int(input("Informe a estação de origem (1 - 14): "))
    origin = origin - 1
    destiny = int(input("Informe a estação de destino (0 até 14): "))
    destiny = destiny - 1

    e1 = node(0, costs[0], ["B"])
    e2 = node(1, costs[1], ["B", "Y"])
    e3 = node(2, costs[2], ["B", "R"])
    e4 = node(3, costs[3], ["B", "G"])
    e5 = node(4, costs[4], ["B", "Y"])
    e6 = node(5, costs[5], ["B"])
    e7 = node(6, costs[6], ["Y"])
    e8 = node(7, costs[7], ["Y", "G"])
    e9 = node(8, costs[8], ["Y", "R"])
    e10 = node(9, costs[9], ["Y"])
    e11 = node(10, costs[10], ["R"])
    e12 = node(11, costs[11], ["G"])
    e13 = node(12, costs[12], ["R", "G"])
    e14 = node(13, costs[13], ["G"])

    nodes = [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14]

    origin_node = nodes[origin]
    destiny_node = nodes[destiny]

    solution = solve(origin_node, destiny_node, nodes, heuristics[destiny])

    solution.run_a_star()

    solution.print_path()


main()
