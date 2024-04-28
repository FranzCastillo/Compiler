from graphviz import Digraph

from src.yapar.lr_set import LrSet


class LR0View:
    def draw_LR0(self, sets: list[LrSet], output_path: str):
        """
        Draw the LR(0) automaton
        """
        dot = Digraph(
            comment="LR(0) Automaton",
            format="png",
            graph_attr={"rankdir": "LR"},
            node_attr={"shape": "plaintext"},
        )
        # Draw "nodes"
        for lr_set in sets:
            dot.node(str(lr_set), lr_set.get_dot(), shape="plaintext")

        # Draw "edges"
        for lr_set in sets:
            for symbol, next_set in lr_set.transitions.items():
                dot.edge(str(lr_set), str(next_set), label=str(symbol))

        dot.render(output_path, cleanup=True)