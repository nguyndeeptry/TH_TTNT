from collections import deque
import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self, adjac_lis):
        self.adjac_lis = adjac_lis

    def get_neighbors(self, v):
        return self.adjac_lis[v]

    # Hàm heuristic (giá trị bằng nhau cho tất cả các nút)
    def h(self, n):
        H = { 'A': 1, 'B': 1, 'C': 1, 'D': 1, 'E': 1, 'Z': 1 }
        return H[n]

    def heuristic_alg(self, start, stop):
        open_set = set([start])
        closed_set = set([])
        g = {}
        g[start] = 0
        parents = {}
        parents[start] = start

        while len(open_set) > 0:
            n = None
            for v in open_set:
                if n is None or g[v] + self.h(v) < g[n] + self.h(n):
                    n = v
            if n is None:
                print("Path does not exist!")
                return None

            if n == stop:
                reconst_path = []
                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]
                reconst_path.append(start)
                reconst_path.reverse()
                print("Path found:", reconst_path)
                return reconst_path

            for (m, weight) in self.get_neighbors(n):
                if m not in open_set and m not in closed_set:
                    open_set.add(m)
                    parents[m] = n
                    g[m] = g[n] + weight
                else:
                    if g[m] > g[n] + weight:
                        g[m] = g[n] + weight
                        parents[m] = n
                        if m in closed_set:
                            closed_set.remove(m)
                            open_set.add(m)

            open_set.remove(n)
            closed_set.add(n)

        print("Path does not exist!")
        return None


if __name__ == "__main__":
    adjac_lis = {
        'A': [('B', 4), ('C', 2)],
        'B': [('A', 4), ('D', 10), ('E', 12)],
        'C': [('A', 2), ('E', 7)],
        'D': [('B', 10), ('E', 6), ('Z', 15)],
        'E': [('B', 12), ('C', 7), ('D', 6), ('Z', 9)],
        'Z': [('D', 15), ('E', 9)]
    }

    g = Graph(adjac_lis)
    start_node = input("Enter the start node: ")
    stop_node = input("Enter the stop node: ")
    path = g.heuristic_alg(start_node, stop_node)

    # Vẽ đồ thị
    G = nx.Graph()
    for node, neighbors in adjac_lis.items():
        for neighbor, weight in neighbors:
            G.add_edge(node, neighbor, weight=weight)

    pos = nx.spring_layout(G)  # bố trí các nút
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=12)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # Highlight đường đi tìm được
    if path:
        edges_in_path = [(path[i], path[i+1]) for i in range(len(path)-1)]
        nx.draw_networkx_edges(G, pos, edgelist=edges_in_path, edge_color='red', width=3)

    plt.title("Đồ thị Heuristic Algorithm - TH5")
    plt.show()
