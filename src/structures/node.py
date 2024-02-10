from src.regex.operators_values import EPSILON


class Node:
    def __init__(self, value, left=None, right=None, tag=None):
        self.value = value
        self.left = left
        self.right = right
        self.tag = tag
        self.nullable = False

    def __repr__(self):
        return f"Node({self.value})"

    def __str__(self):
        return f"Node({self.value})"
