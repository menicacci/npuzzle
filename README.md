# n-Puzzle Solver

The 15-Puzzle is a sliding puzzle that consists of a 4x4 grid with 15 numbered tiles and one empty space. The goal is to rearrange the tiles from their initial configuration to a target configuration by sliding the tiles into the empty space.

<p align="center">
  <img src="https://github.com/menicacci/npuzzle/assets/105044910/5d445163-21f8-4c77-8cc4-124af1a9af35" alt="Image" style="width: 30%; height: auto;">
</p>

This project solve the 15-Puzzle problem in a generic way, meaning it can handle puzzles of various dimensions (not limited to 4x4).

The initial approach was to rely on the Manhattan distance heuristic, solving the problem optimally using the A* algorithm. The problem with this approach concerns the computational complexity, in fact the number of states that is generated to find a solution is considerable. Therefore, the A* algorithm is not advantageous as it creates a tree with a considerable number of nodes, without forgetting the size of the queue necessary for choosing the next node to expand.

A neural network has been introduced with the aim of advancing towards solutions that are more efficient in terms of computational complexity. Given that our objective is to address the 15-puzzle in its general form, the configuration of the neural network will need to be contingent upon the specific puzzle size we intend to solve. Specifically, the network's architecture will be influenced by the length of the side (n).
<p align="center">
  <img src="https://github.com/menicacci/npuzzle/assets/105044910/8791c033-ba36-4c26-bcfa-fe65712359c4" alt="Image" style="width: 50%; height: auto;">
</p>

The figure on the right shows an example of how the state of the puzzle is encoded (n = 3). The left figure shows instead the output of the neural network (underlined in orange). For the target configuration, we expect [0, 0, 0, 0] as output.

<table>
  <tr>
    <td><img src="https://github.com/menicacci/npuzzle/assets/105044910/d4c503ac-02e4-4eb5-ad7a-6bbc2ac121e3" alt="Image 1"></td>
    <td><img src="https://github.com/menicacci/npuzzle/assets/105044910/8b048a45-7d70-48d9-9885-310e82307a9e" alt="Image 2"></td>
  </tr>
</table>

The network training process involved utilizing data generated through the A* algorithm. A set of simulations was conducted on randomized boards to generate datasets, categorized based on the table's side size.

For each dataset entry, we have two arrays, one representing the state of the table, another associated with the sequence of moves to be performed to solve the table in question. From this dataset we have therefore obtained the set of data on which the model was trained.
