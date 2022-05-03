def print_go_tree(node, max_depth=3, _depth=0):
    if _depth < max_depth:
        length = len(list(node.children))
        for idx, child in enumerate(node.children.items()):
            if idx + 1 == length:
                print(
                    "│    " * _depth + "└──",
                    "move" + str(child[0]) + ": " + str(child[1].n_visits),
                )
                print_go_tree(child[1], _depth=_depth + 1)
            else:
                print(
                    "│    " * _depth + "├──",
                    "move" + str(child[0]) + ": " + str(child[1].n_visits),
                )
                print_go_tree(child[1], _depth=_depth + 1)
