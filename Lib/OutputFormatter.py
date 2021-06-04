from Lib.Token import Token
from dataclasses import dataclass
from pprint import pprint
from typing import List
from Lib.Node import Node, NodeType as NT

@dataclass(unsafe_hash=True)
class PNode(object):
    def __init__(self, name, children):
            self.name = name
            self.children = children

def print_tree(node):
    tree = pre_process_tree(node)
    print_tree_lib(tree)

def pre_process_tree(node: Node):
    if node.value in {NT.INT_LITERAL, NT.BOOL_LITERAL, NT.STRING_LITERAL, NT.IDENTIFIER}:
        return PNode(node.parameters[0], [])
    return PNode(node.value, [pre_process_tree(child) for child in node.parameters])

# https://stackoverflow.com/questions/30893895/how-to-print-a-tree-in-python
def print_tree_lib(current_node, childattr='children', nameattr='name'):
    if hasattr(current_node, nameattr):
        name = lambda node: getattr(node, nameattr)
    else:
        name = lambda node: str(node)

    children = lambda node: getattr(node, childattr)
    nb_children = lambda node: sum(nb_children(child) for child in children(node)) + 1

    def balanced_branches(current_node):
        size_branch = {child: nb_children(child) for child in children(current_node)}

        """ Creation of balanced lists for "a" branch and "b" branch. """
        a = children(current_node)
        b = []
        while a and sum(size_branch[node] for node in b) < sum(size_branch[node] for node in a):
            b.append(a.pop())

        return a, b

    print_tree_horizontally(current_node, balanced_branches, name)


def print_tree_horizontally(current_node, balanced_branches, name_getter, indent='', last='updown'):

    up, down = balanced_branches(current_node)

    """ Printing of "up" branch. """
    for child in up:     
        next_last = 'up' if up.index(child) == 0 else ''
        next_indent = '{0}{1}{2}'.format(indent, ' ' if 'up' in last else '│', ' ' * len(name_getter(current_node)))
        print_tree_horizontally(child, balanced_branches, name_getter, next_indent, next_last)

    """ Printing of current node. """
    if last == 'up': start_shape = '┌'
    elif last == 'down': start_shape = '└'
    elif last == 'updown': start_shape = ' '
    else: start_shape = '├'

    if up: end_shape = '┤'
    elif down: end_shape = '┐'
    else: end_shape = ''

    print('{0}{1}{2}{3}'.format(indent, start_shape, name_getter(current_node), end_shape))

    """ Printing of "down" branch. """
    for child in down:
        next_last = 'down' if down.index(child) is len(down) - 1 else ''
        next_indent = '{0}{1}{2}'.format(indent, ' ' if 'down' in last else '│', ' ' * len(name_getter(current_node)))
        print_tree_horizontally(child, balanced_branches, name_getter, next_indent, next_last)

def display_tokens(tokens: List['Token']):
    print("--"*40)
    print(f"{'Type':<20}{'Line':<10}{'Column':<10}{'Value'}")
    print("--"*50)
    for token in tokens:
        print(f"{token.type or '':20}{token.line or '':<10}{token.column or '':<10}{token.value or ''}")
    print("--"*50)

def display_semantic_symbol_table(symbol_table):
    print()
    print("Semantic Symbol Table")
    print("--"*30)
    print(f"{'Data Type':<20} {'Identifier':<20}")
    print("--"*30)
    for identifier, [data_type, _] in symbol_table.items():
        print(f"{data_type:<20} {identifier:<20}")
    print("--"*30)
    print()

def display_evaluated_symbol_table(symbol_table):
    print()
    print("Evaluated Symbol Table")
    print("--"*40)
    print(f"{'Data Type':<20} {'Identifier':<20} {'Value'}")
    print("--"*40)
    for identifier, value, data_type in symbol_table.table:
        print(f"{data_type:<20} {identifier:<20} {str(value)}")
    print("--"*40)
    print()