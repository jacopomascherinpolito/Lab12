import networkx as nx
from database.dao import DAO


class Model:
    def __init__(self):
        self.G = nx.Graph()
        self.diff_map = {
            "facile": 1,
            "media": 1.5,
            "difficile": 2
        }

    def build_weighted_graph(self, year: int):
            self.G.clear()
            # 1
            rifugi = DAO.get_all_rifugi()
            for r in rifugi:
                self.G.add_node(r.id, label=r.nome)

            # 2
            edges = DAO.get_edges_by_year(year)

            for e in edges:
                id1 = e['id_rifugio1']
                id2 = e['id_rifugio2']
                dist = e['distanza']
                diff = e['difficolta']

                peso = float(dist) * self.diff_map[diff]

                self.G.add_edge(id1, id2, weight=peso)

    def get_edges_weight_min_max(self):
        if not self.G.edges:
            return 0, 0
        weights = [data['weight'] for u, v, data in self.G.edges(data=True)]
        return min(weights), max(weights)

    def count_edges_by_threshold(self, soglia):
        minori = 0
        maggiori = 0
        for u, v, data in self.G.edges(data=True):
            if data['weight'] < soglia:
                minori += 1
            elif data['weight'] > soglia:
                maggiori += 1
        return minori, maggiori

    def get_shortest_path_constrained(self, soglia):
        best_weight = float('inf')
        best_path = []

        for node in self.G.nodes():
            valid_neighbors = []
            for neighbor in self.G.neighbors(node):
                weight = self.G[node][neighbor]['weight']
                if weight > soglia:
                    valid_neighbors.append((neighbor, weight))

            if len(valid_neighbors) >= 2:
                valid_neighbors.sort(key=lambda x: x[1])
                n1, w1 = valid_neighbors[0]
                n2, w2 = valid_neighbors[1]

                current_total_weight = w1 + w2

                if current_total_weight < best_weight:
                    best_weight = current_total_weight
                    best_path = [(n1, node, w1), (node, n2, w2)]

        return best_path, best_weight