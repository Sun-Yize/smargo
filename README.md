# Smargo: An efficient and highly accurate solver for tsumego

> Smargo：围棋死活棋求解器
>
> Sun. Yize -- Shandong University

<table>
    <td>
        <img src="pics\sample_pic1.gif" style="zoom:10%" />
    </td>
    <td>
        <img src="pics\sample_pic2.gif" style="zoom:10%" />
    </td>
</table>


Smargo is a python-based tsumego problems solver. It apply the Monte Carlo tree search algorithm to solve tsumego games in Go, and improve the traditional Monte Carlo tree search structure to make it more suitable for determining and solving tsumego games. 

Smargo also has its own dataset: Smargo dataset, which solves the problems of insufficient amount of tsumego data and inconsistent standards. 



Smargo 是一个基于 python 的围棋死活棋求解器。 它将蒙特卡洛树搜索算法应用于围棋死活棋博弈中，并且对传统的蒙特卡洛树搜索结构进行了改进，使其更适合于确定和求解围棋死活棋。
Smargo也有自己的数据集：Smargo 数据集，解决了围棋死活棋数据量不足、标准不一致的问题。



## Install

```shell
$ python setup.py sdist
$ python -m pip install dist/*
```

## Datasets

Smargo Datasets contains two subsets: Smarge_30 and Smarge_50.

Download the datasets from Google Drive:

+ Smarge_30 Dataset: [download link](https://drive.google.com/file/d/1CiU7mu1qBz-msiSqy5UaCItTYYNbwP49/view?usp=sharing)

+ Smarge_50 Dataset: [download link](https://drive.google.com/file/d/1AsqK1F97d4r9Dil9GDOs3YrUUBqNbz7E/view?usp=sharing)

## Usage

+ load go game file:	

  ```python
  from smargo.loader import go_board_init, go_info_init
  
  # prepare go board data
  file_path = "smargo_30/json/tsumego_000000.json"
  state = go_board_init(file_path)
  ground_truth, size = go_info_init(file_path)
  ```

+ train mcts trees:

  ```python
  from smargo.model import MCTS
  
  # train monte carlo search tree
  num_moves = len(ground_truth)
  mcts = MCTS(c_puct=5)
  mcts.train(state, init_playout=200, num_moves=num_moves)
  ```

+ visualize results:

  ```python
  from smargo.visualize import plot_go_board, print_go_tree
  
  # print mcts tree
  print_go_tree(mcts.root, max_depth=2)
  
  # visualize all moves
  moves = mcts.result_moves(num_moves=num_moves)
  print(moves)
  plot_go_board(state, moves)
  ```