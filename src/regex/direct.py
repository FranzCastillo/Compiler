from src.regex.operators_values import *
from src.regex.shunting_yard import ShuntingYard
from src.structures.node import Node
from src.regex.state import State


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
    next_pos_table = []  # tag, symbol, next_pos
    for char in regex:
        if char not in operators:
            if char == EPSILON:
                stack.append(Node(char, tag=EPSILON))
            else:
                stack.append(Node(char, tag=tag))
                next_pos_table.append({"tag": tag, "symbol": char, "next_pos": set()})
                tag += 1
        else:
            if char in unary_operators:
                left = stack.pop()
                if char == KLEENE_STAR:
                    node = Node(char, left)
                    node.nullable = True
                    node.first_pos = left.first_pos
                    node.last_pos = left.last_pos
                    stack.append(node)

                    # Fill the next_pos_table
                    for pos in left.last_pos:
                        next_pos_table[pos - 1]["next_pos"].update(left.first_pos)
                else:
                    stack.append(Node(char, left, tag=tag))
                    tag += 1
            else:  # Binary operator
                right = stack.pop()
                left = stack.pop()

                node = Node(char, left, right)
                if char == UNION:
                    node.nullable = left.nullable or right.nullable
                    node.first_pos = left.first_pos.union(right.first_pos)
                    node.last_pos = left.last_pos.union(right.last_pos)
                elif char == CONCAT:
                    node.nullable = left.nullable and right.nullable
                    if left.nullable:
                        node.first_pos = left.first_pos.union(right.first_pos)
                    else:
                        node.first_pos = left.first_pos

                    if right.nullable:
                        node.last_pos = left.last_pos.union(right.last_pos)
                    else:
                        node.last_pos = right.last_pos

                    # Fill the next_pos_table
                    for pos in left.last_pos:
                        next_pos_table[pos - 1]["next_pos"].update(right.first_pos)

                stack.append(node)

    return stack.pop(), next_pos_table


def get_alphabet(regex):
    """
    Get the alphabet of the regular expression.
    :param regex:
    :return:
    """
    alphabet = {AUGMENTED}
    for char in regex:
        if (
                char not in operators and
                char not in unary_operators and
                char != EPSILON and
                char != OPEN_PAREN and
                char != CLOSE_PAREN
        ):
            alphabet.add(char)
    return alphabet


class DirectDFA:
    def __init__(self, regex):
        self.alphabet = get_alphabet(regex)
        self.regex = regex
        self.postfix_regex = get_postfix(regex)
        self.augmented_regex = self.postfix_regex + Operator.AUGMENTED.symbol + CONCAT
        self.syntax_tree, self.next_pos_table = build_syntax_tree(self.augmented_regex)
        self.transition_table = self._build_transition_table()

    def _build_transition_table(self):
        """
        Build the transition table of the regular expression.
        :return:
        """
        transition_table = []

        # To keep track of the states that have been added
        state_positions_map = {}  # state: positions

        # Add the initial row
        initial_next_pos = self.next_pos_table[0]

        initial_row = {
            "positions": initial_next_pos["next_pos"],
            "state": State(),
        }
        state_positions_map[initial_row["state"]] = initial_row["positions"]

        initial_transitions = {}
        for char in self.alphabet:
            transition = self._get_transition(initial_next_pos["next_pos"], char)
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
