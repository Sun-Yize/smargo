def print_go_tree(node, depth=0, max_depth=3):
    if depth < max_depth:
        length = len(list(node.children))
        for idx, child in enumerate(node.children.items()):
            if idx+1 == length:
                print('│    '*depth+'└──', 'move'+str(child[0])+': '+str(child[1].n_visits))
                print_go_tree(child[1], depth+1)
            else:
                print('│    '*depth+'├──', 'move'+str(child[0])+': '+str(child[1].n_visits))
                print_go_tree(child[1], depth+1)
