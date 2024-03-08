from src.regex.grammar import Grammar
from src.regex.operators_values import *
from src.regex.shunting_yard import ShuntingYard
from src.regex.state import State
from src.regex.sy_tokens import SyToken
from src.structures.node import Node


def get_postfix(regex):
    """
    Get the postfix notation of the regular expression.
    :param regex:
    :return:
    """
    sy = ShuntingYard()
    sy.set_regex(regex)
    return sy.get_postfix()


def build_syntax_tree(regex):
    """
    Build the syntax tree of the regular expression.
    :param regex:
    :return:
    """
    stack = []
    tag = 1
    for token_obj in regex:
        token = token_obj.value
        if token not in operators:
            if token == EPSILON:
                stack.append(Node(token, tag=EPSILON))
            else:
                stack.append(Node(token, tag=tag))
                tag += 1
        else:
            if token == KLEENE_STAR:
                left = stack.pop()
                node = Node(token, left)
                stack.append(node)
            else:  # Binary operator
                right = stack.pop()
                left = stack.pop()
                node = Node(token, left, right)
                stack.append(node)

    return stack.pop()


def apply_nullable(node: Node):
    """
    Apply the nullable property to the nodes of the tree.
    :param node:
    :return:
    """
    # Recursively get to the leaves
    if node.left:
        apply_nullable(node.left)
    if node.right:
        apply_nullable(node.right)

    if node.value == EPSILON:
        node.nullable = True
    elif node.value == UNION:
        node.nullable = node.left.nullable or node.right.nullable
    elif node.value == CONCAT:
        node.nullable = node.left.nullable and node.right.nullable
    elif node.value == KLEENE_STAR:
        node.nullable = True
    else:
        node.nullable = False


def apply_first_pos(node: Node):
    """
    Apply the first_pos property to the nodes of the tree.
    :param node:
    :return:
    """
    # Recursively get to the leaves
    if node.left:
        apply_first_pos(node.left)
    if node.right:
        apply_first_pos(node.right)

    if node.value == EPSILON:
        node.first_pos = set()
    elif node.value == UNION:
        node.first_pos = node.left.first_pos.union(node.right.first_pos)
    elif node.value == CONCAT:
        if node.left.nullable:
            node.first_pos = node.left.first_pos.union(node.right.first_pos)
        else:
            node.first_pos = node.left.first_pos
    elif node.value == KLEENE_STAR:
        node.first_pos = node.left.first_pos
    else:
        node.first_pos = {node.tag}


def apply_last_pos(node: Node):
    """
    Apply the last_pos property to the nodes of the tree.
    :param node:
    :return:
    """
    # Recursively get to the leaves
    if node.left:
        apply_last_pos(node.left)
    if node.right:
        apply_last_pos(node.right)

    if node.value == EPSILON:
        node.last_pos = set()
    elif node.value == UNION:
        node.last_pos = node.left.last_pos.union(node.right.last_pos)
    elif node.value == CONCAT:
        if node.right.nullable:
            node.last_pos = node.left.last_pos.union(node.right.last_pos)
        else:
            node.last_pos = node.right.last_pos
    elif node.value == KLEENE_STAR:
        node.last_pos = node.left.last_pos
    else:
        node.last_pos = {node.tag}


def get_next_pos_table(node: Node):
    """
    Get the next_pos table of the regular expression.
    :param node:
    :return:
    """
    next_pos_table = []  # tag, symbol, next_pos
    get_next_pos(node, next_pos_table)
    return next_pos_table


def get_next_pos(node: Node, next_pos_table: list):
    """
    Apply the next_pos property to the nodes of the tree.
    :param node:
    :param next_pos_table:
    :return:
    """
    # Recursively get to the leaves
    if node.left:
        get_next_pos(node.left, next_pos_table)
    if node.right:
        get_next_pos(node.right, next_pos_table)

    if node.value == CONCAT:
        for pos in node.left.last_pos:
            next_pos_table[pos - 1]["next_pos"].update(node.right.first_pos)
    elif node.value == KLEENE_STAR:
        for pos in node.left.last_pos:
            next_pos_table[pos - 1]["next_pos"].update(node.left.first_pos)
    else:
        if node.tag and node.value != EPSILON:
            next_pos_table.append({
                "tag": node.tag,
                "symbol": node.value,
                "next_pos": set()
            })


def get_alphabet(regex):
    """
    Get the alphabet of the regular expression.
    :param regex:
    :return:
    """
    alphabet = {AUGMENTED}
    operators = [Operator.KLEENE_STAR.symbol, Operator.CONCAT.symbol, Operator.UNION.symbol]
    for token in regex:
        if token.value not in alphabet and token.value not in operators:
            alphabet.add(token.value)
    return alphabet


def postfix_to_infix(postfix):
    stack = []
    for token in postfix:
        if token.value in unary_operators:
            right = stack.pop()
            temp = [SyToken('OPEN_PAREN', '(')]
            for inside_token in right:
                temp.append(inside_token)
            temp.append(token)
            temp.append(SyToken('CLOSE_PAREN', ')'))
            stack.append(temp)
        elif token.value in operators:
            right = stack.pop()
            left = stack.pop()
            temp = [SyToken('OPEN_PAREN', '(')]
            for inside_token in left:
                temp.append(inside_token)
            temp.append(token)
            for inside_token in right:
                temp.append(inside_token)
            temp.append(SyToken('CLOSE_PAREN', ')'))
            stack.append(temp)
        else:
            stack.append([token])
    return stack.pop()


class DirectDFA:
    def __init__(self, regex):
        if not regex:
            raise Exception("Regex not set")
        self.regex = regex
        self.alphabet = get_alphabet(self.regex)
        self.augmented_regex = self.regex + [SyToken('OP', AUGMENTED), SyToken('OP', CONCAT)]
        self.syntax_tree = build_syntax_tree(self.augmented_regex)
        apply_nullable(self.syntax_tree)
        apply_first_pos(self.syntax_tree)
        apply_last_pos(self.syntax_tree)
        self.next_pos_table = get_next_pos_table(self.syntax_tree)
        self.transition_table = self._build_transition_table()

    def get_grammar(self):
        """
        Get the grammar of the regular expression.
        :return:
        """
        return self._build_grammar()

    def _build_transition_table(self):
        """
        Build the transition table of the regular expression.
        :return:
        """
        transition_table = []

        # To keep track of the states that have been added
        state_positions_map = {}  # state: positions

        # Add the initial row
        initial_next_pos = self.syntax_tree.first_pos

        initial_row = {
            "positions": initial_next_pos,
            "state": State(),
        }
        state_positions_map[initial_row["state"]] = initial_row["positions"]

        initial_transitions = {}
        for char in self.alphabet:
            transition = self._get_transition(initial_row["positions"], char)
            if transition:
                if transition not in state_positions_map.values():
                    initial_transitions[char] = State()
                    state_positions_map[initial_transitions[char]] = transition
                else:
                    for state, positions in state_positions_map.items():
                        if positions == transition:
                            initial_transitions[char] = state
                            break

        initial_row["transitions"] = initial_transitions

        transition_table.append(initial_row)

        # Check if new states were added in the transitions and add them to the table
        states_to_add = {state for state in state_positions_map.keys() if
                         state not in [row["state"] for row in transition_table]}

        while states_to_add:
            current_state = states_to_add.pop()
            new_row = {
                "positions": state_positions_map[current_state],
                "state": current_state,
                "transitions": {}
            }

            new_transitions = {}
            for char in self.alphabet:
                transition = self._get_transition(state_positions_map[current_state], char)
                if transition:
                    if transition not in state_positions_map.values():
                        new_transitions[char] = State()
                        state_positions_map[new_transitions[char]] = transition

                        states_to_add.add(new_transitions[char])
                    else:
                        for state, positions in state_positions_map.items():
                            if positions == transition:
                                new_transitions[char] = state
                                break

            new_row["transitions"] = new_transitions
            transition_table.append(new_row)

        return transition_table

    def _get_transition(self, positions: set, symbol: str):
        """
        Get the transition of the set of positions with the symbol.
        :param positions:
        :param symbol:
        :return:
        """
        transition = set()
        for pos in positions:
            if self.next_pos_table[pos - 1]["symbol"] == symbol:
                transition.update(self.next_pos_table[pos - 1]["next_pos"])
        return transition

    def _build_grammar(self):
        """
        Build the grammar of the regular expression.
        :return:
        """
        states = {row["state"] for row in self.transition_table}
        alphabet = self.alphabet
        start = self.transition_table[0]["state"]

        accepting_tag = self.next_pos_table[-1]["tag"]

        accepting_states = {row["state"] for row in self.transition_table if
                            accepting_tag in row["positions"]}
        transitions = {}
        for row in self.transition_table:
            # Add the rows with no transitions
            if not row["transitions"]:
                transitions[row["state"]] = {}
                row["state"].transitions[char] = {}
                continue
            for char in alphabet:
                if row["transitions"].get(char):  # Gets the state that it transitions to
                    if row["state"] not in transitions:  # If the state is not in the transitions, add it
                        transitions[row["state"]] = {}

                    transitions[row["state"]][char] = {row["transitions"][char]}
                    row["state"].transitions[char] = {row["transitions"][char]}

        return Grammar(states, alphabet, start, accepting_states, transitions)
