from src.regex.operators_values import EPSILON


class Node:
    def __init__(self, value, left=None, right=None, tag=None):
        self.value = value
        self.left = left
        self.right = right
        self.tag = tag
        if tag == EPSILON:
            self.nullable = True
            self.first_pos = set()
            self.last_pos = set()
        else:
            self.nullable = False
            self.first_pos = {tag}
            self.last_pos = {tag}

    def __repr__(self):
        return f"Node({self.value})"

    def __str__(self):
        return f"Node({self.value})"
