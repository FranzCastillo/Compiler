from graphviz import Digraph
from src.regex.operators import Operator
import os

os.environ["PATH"] += os.pathsep + 'D:\\UVG\\Compiladores\\graphviz\\bin'


class YalexResult:
    def __init__(self, rules: dict = None, print_console: callable = None):
        self.print_console = print_console
        self.rules = rules
        self.visited = set()
        self.dot = Digraph(comment='YALex Visualization')
        self.dot.attr(rankdir='LR', size='8,5')
        self.dot.attr('node', shape='circle')

    def view(self):
        self.dot.node('start_point', shape='point')
        self.dot.node('-1', shape='circle')
        self.dot.edge('start_point', '-1')

        for rule in self.rules:
            for grammar in self.rules[rule]:
                for state in grammar.accepting_states:
                    self.dot.node(str(state.value), shape='doublecircle')

            # Add an epsilon transition to the start of each grammar
            for grammar in self.rules[rule]:
                self.dot.edge('-1', str(grammar.start.value), label=Operator.EPSILON.symbol)
                self._visualize(grammar.start)

            self.dot.render(rule, format='pdf', cleanup=True, directory='output')
            print(f"- Automaton saved on 'output/{rule}.pdf'")

    def _visualize(self, state):
        if state in self.visited:
            return
        self.visited.add(state)
        for transition in state.transitions:
            for next_state in state.transitions[transition]:
                self.dot.edge(str(state.value), str(next_state.value), label=transition)
                self._visualize(next_state)
        for nextState in state.epsilon_transitions:
            self.dot.edge(str(state.value), str(nextState.value), label=Operator.EPSILON.symbol)
            self._visualize(nextState)
