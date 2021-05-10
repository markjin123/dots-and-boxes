# Dots and Boxes AI

This AI is implement with Monte Carlo Tree Search algothirm with predetermined initial moves based on certain well studied board positions.

# Required Library

  - numpy
  - tkinter


Important Notes:

 If there is trouble installing tkinter module. 
  Install the future module:
  ```sh
  Pip install feature
  ```
   Then replace "import tkinter" with "from feature.move import tkinter".

### Running

Run the program with:
```sh
python3 main.py
```

### Program Stucture

main.py is responsible for the main UI and user events.
node.py is a tree node that also stores game states.
ai.py is where each AI move is processed along with the heuristic function. Each move is currently set to 20 seconds but that can be changed.
mcts.py implement the different aspect of the Monte Carlo Tree Search algothirm

### MCTS

The MCTS is currently implemented with default reward being +1 per win and 0 per loss. It is also using random rollout during simulation. It is certainly using UCT 1 as the value of each node and the highest valued UTC value is being choosen during the MCTS section process and during the final move section process. It was determined during our testing that the best exploration parameter was sqrt(2).


### Todos

 - Units tests
 - Storing flipped game state as the same node which will reduce the total memory by 1/4.

License
----

MIT
