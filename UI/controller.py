import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def handle_grafo(self, e):

        try:
            anno = int(self._view.txt_anno.value)
        except ValueError:
            self._view.show_alert("Inserisci un numero valido per l'anno.")
            return

        if not (1950 <= anno <= 2024):
            self._view.show_alert("Anno fuori intervallo (1950-2024).")
            return

        self._model.build_weighted_graph(anno)

        self._view.lista_visualizzazione_1.controls.clear()
        n_nodi = self._model.G.number_of_nodes()
        n_archi = self._model.G.number_of_edges()

        self._view.lista_visualizzazione_1.controls.append(
            ft.Text(f"Grafo creato con {n_nodi} nodi e {n_archi} archi")
        )

        if n_archi > 0:
            min_p, max_p = self._model.get_edges_weight_min_max()
            self._view.lista_visualizzazione_1.controls.append(
                ft.Text(f"Peso Min: {min_p:.2f} - Peso Max: {max_p:.2f}")
            )

        self._view.update()

    def handle_conta_archi(self, e):
        if self._model.G.number_of_nodes() == 0:
            self._view.show_alert("Crea prima il grafo!")
            return

        try:
            soglia = float(self._view.txt_soglia.value)
        except ValueError:
            self._view.show_alert("Soglia non valida.")
            return

        min_w, max_w = self._model.get_edges_weight_min_max()
        if not (min_w <= soglia <= max_w):
            self._view.show_alert(f"La soglia deve essere tra {min_w:.2f} e {max_w:.2f}")
            return

        minori, maggiori = self._model.count_edges_by_threshold(soglia)
        self._view.lista_visualizzazione_2.controls.clear()
        self._view.lista_visualizzazione_2.controls.append(
            ft.Text(f"Archi con peso < {soglia}: {minori}")
        )
        self._view.lista_visualizzazione_2.controls.append(
            ft.Text(f"Archi con peso > {soglia}: {maggiori}")
        )
        self._view.update()

    def handle_cammino_minimo(self, e):
        if self._model.G.number_of_nodes() == 0:
            self._view.show_alert("Crea prima il grafo!")
            return

        try:
            soglia = float(self._view.txt_soglia.value)
        except ValueError:
            self._view.show_alert("Inserisci un valore numerico per la soglia.")
            return

        path_edges, total_weight = self._model.get_shortest_path_constrained(soglia)

        self._view.lista_visualizzazione_3.controls.clear()

        if not path_edges:
            self._view.lista_visualizzazione_3.controls.append(
                ft.Text("Nessun cammino trovato che soddisfi i vincoli.")
            )
        else:
            self._view.lista_visualizzazione_3.controls.append(
                ft.Text(f"Cammino minimo trovato! Peso totale: {total_weight:.2f}")
            )
            # Stampiamo la sequenza degli archi
            for u, v, w in path_edges:
                nome_u = self._model.G.nodes[u]['label']
                nome_v = self._model.G.nodes[v]['label']
                self._view.lista_visualizzazione_3.controls.append(
                    ft.Text(f"{nome_u} -> {nome_v} (Peso: {w:.2f})")
                )

        self._view.update()