import json
import sys


def text_tree_file_to_dict(filename):
    with open(filename, 'r') as f:
        lines = [line.rstrip('\n') for line in f]
        return text_tree_lines_to_dict(lines)


def text_tree_to_dict(textTree):
    # print(f"textTree = {textTree}")
    return text_tree_lines_to_dict(textTree.split('\n'))


# this code definitely needs rewriting.
def text_tree_lines_to_dict(text_tree_lines: [str]):
    def helper(lines, level=0):
        # print(f"========= helper, lvl = {level} lines = {lines}")
        node = {}
        while lines:
            s = lines[0]
            if not s:
                lines.pop(0)
                continue

            indent = len(s) - len(s.lstrip())
            # print(f"Real line: {s} lvl = {level} indent= {indent}")

            if indent == level:
                lines.pop(0)
                branch = s.lstrip()
                node[branch] = helper(lines, level + 1)
            elif indent > level:
                print(f"Error: Unexpected indent in line '{s}'")
                sys.exit(1)

            elif indent < level:
                break
        return node

    return helper(text_tree_lines)


def process_nodes_from_file(text_tree_filename, root_leaf_func, non_leaf_func, depth=0):
    tree = text_tree_file_to_dict(text_tree_filename)
    process_nodes(tree, root_leaf_func, non_leaf_func)


def process_nodes(tree_dict, root_leaf_func, non_leaf_func, depth=0):
    non_leaf_nodes = []

    def helper(node, depth):
        for key, value in node.items():
            if value:  # if the node has children, i.e., it's a non-leaf node
                non_leaf_nodes.append((depth, key, list(value.keys())))
                helper(value, depth + 1)
            elif depth == 0:  # we only want leaf nodes at top level, rest are covered by the non-leaf
                root_leaf_func(key)

    # traverse the tree and process leaf nodes and collect non-leaf nodes
    helper(tree_dict, depth)

    # process all non-leaf nodes in depth-first order.
    # NOTE don't think it matters what order we do non-leaf nodes in, currently;
    # but if we required sub-reducer files to exist before HOR is made, this would be necessary.
    for _, node_key, children_keys in sorted(non_leaf_nodes, reverse=True):
        non_leaf_func((node_key, children_keys))


# from file test:

# root_leaf_func = lambda x: print(f"Root Leaf: {x}")
# non_leaf_func = lambda x: print(f"Non-leaf: {x}")
#
# process_nodes_from_file("tree.txt", root_leaf_func, non_leaf_func)



# direct string test:

# tree = text_tree_to_dict("""
#
#
# Thermostat
#  TempSensor
#  Heater
# About
#
#
# """)
#
# print(f"Parsed to dict:\n{json.dumps(tree, indent=4)}")
# print()
# print()
#
#
# process_nodes(tree, root_leaf_func, non_leaf_func)



