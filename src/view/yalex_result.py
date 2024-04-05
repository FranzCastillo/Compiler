from graphviz import Digraph
from src.regex.operators import Operator
import os

os.environ["PATH"] += os.pathsep + 'D:\\UVG\\Compiladores\\graphviz\\bin'


class YalexResult:
    def __init__(self, rules: dict = None, print_console: callable = None):
        self.print_console = print_console
        self.rules = rules  # {rule: [grammar]}
        self.visited = set()
        self.dot = Digraph(comment='YALex Visualization')
        self.dot.attr(rankdir='LR', size='8,5')
        self.dot.attr('node', shape='circle')

    def view(self, output_path: str = 'output'):
        for rule in self.rules:
            # Reset visited set and dot object for each rule
            self.visited = set()
            self.dot = Digraph(comment='YALex Visualization')
            self.dot.attr(rankdir='LR', size='8,5')
            self.dot.attr('node', shape='circle')

            self.dot.node('start_point', shape='point')
            self.dot.node('-1', shape='circle')
            self.dot.edge('start_point', '-1')

            for grammar_dict in self.rules[rule]:
                grammar = grammar_dict['grammar']
                for state in grammar.accepting_states:
                    self.dot.node(str(state.value), shape='doublecircle', xlabel=grammar_dict['return'])

            # Add an epsilon transition to the start of each grammar
            for grammar_dict in self.rules[rule]:
                grammar = grammar_dict['grammar']
                self.dot.edge('-1', str(grammar.start.value), label=Operator.EPSILON.symbol)
                self._visualize(grammar.start)

            self.dot.render(rule, format='pdf', cleanup=True, directory=output_path)
            self.print_console(f"- Automaton saved on '{output_path}/{rule}.pdf'")

    def _visualize(self, state):
        if state in self.visited:
            return
        self.visited.add(state)
        for transition in state.transitions:
            for next_state in state.transitions[transition]:
                temp_transition = transition
                if transition[0] == '\\':
                    temp_transition = f'\\{transition}'

                self.dot.edge(str(state.value), str(next_state.value), label=temp_transition)
                self._visualize(next_state)
        for nextState in state.epsilon_transitions:
            self.dot.edge(str(state.value), str(nextState.value), label=Operator.EPSILON.symbol)
            self._visualize(nextState)
