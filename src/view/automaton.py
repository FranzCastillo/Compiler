from graphviz import Digraph
from src.regex.operators import Operator
import os

os.environ["PATH"] += os.pathsep + 'D:\\UVG\\Compiladores\\graphviz\\bin'


class ViewAutomaton:
    def __init__(self, automaton, type):
        self.automaton = automaton
        self.visited = set()
        self.dot = Digraph(comment='Automaton Visualization - ' + type)
        self.dot.attr(rankdir='LR', size='8,5')
        self.dot.attr('node', shape='circle')
        self.typeAutomaton = type

    def view(self, output_name='test'):
        self.dot.node('start', shape='point')

        if self.typeAutomaton == "NFA":
            self.dot.node(str(self.automaton.end.value), shape='doublecircle')
            self.dot.edge('start', str(self.automaton.start.value), label=Operator.EPSILON.value)
        # if self.typeAutomaton == "DFA":
        #     for state in self.automaton.acceptingStates:
        #         self.dot.node(state.getValue(), shape='doublecircle')

        self._visualize(self.automaton.start)
        self.dot.render(output_name, format='pdf', cleanup=True, directory='output')
        print(f"- Automaton saved on 'output/{output_name}.pdf'")

    def _visualize(self, state):
        if state in self.visited:
            return
        self.visited.add(state)
        for transition in state.transitions:
            for next_state in state.transitions[transition]:
                self.dot.edge(str(state.value), str(next_state.value), label=transition)
                self._visualize(next_state)
        for nextState in state.epsilon_transitions:
            self.dot.edge(str(state.value), str(nextState.value), label=Operator.EPSILON.value)
            self._visualize(nextState)

