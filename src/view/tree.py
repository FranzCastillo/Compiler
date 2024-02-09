from graphviz import Digraph
import os

os.environ["PATH"] += os.pathsep + 'D:\\UVG\\Compiladores\\graphviz\\bin'


class ViewTree:
    def __init__(self):
        self.tree = None
        self.dot = None

    def set_tree(self, tree):
        self.tree = tree
        self.dot = Digraph(comment='Tree Visualization')
        self.dot.attr(rankdir='TB', size='8,5')
        self.dot.attr('node', shape='circle')

    def view(self, output_name='test'):
        self._visualize(self.tree)
        self.dot.render(output_name, format='pdf', cleanup=True, directory='output')
        print(f"- Tree saved on 'output/{output_name}.pdf'")

    def _visualize(self, node):
        if node.left:
            self.dot.edge(str(id(node)), str(id(node.left)))
            self._visualize(node.left)
        if node.right:
            self.dot.edge(str(id(node)), str(id(node.right)))
            self._visualize(node.right)

        if node.tag:
            self.dot.node(str(id(node)),
                          label=f"Valor: {node.value}\n"
                                f"Tag: {node.tag}\n"
                                f"Nullable: {node.nullable}")
        else:
            self.dot.node(str(id(node)),
                          label=f"Valor: {node.value}\n"
                                f"Nullable: {node.nullable}")
