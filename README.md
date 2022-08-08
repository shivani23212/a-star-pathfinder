# A* Path-finding Visualisation Algorithm

## A* Path-Finding Algorithm

The A* Path-finding algorithm (herefrom referenced to as the A* Algorithm) is a searching algorithm which looks for and determines the
shortest possible path between two nodes. Since this is an informed search algorithm, it uses externaly calculated data (in this case, its
heuristic function) to approximate the distance between the current and end node - allowing it to significantly reduce the space searched and
considered, in comparison to a more uninformed 'brute force' approach. This factor makes the A* Algorithm quicker to find a path compared to 
uninformed search algorithms such as Depth and Breadth-First Search.

The algorithm runs using three functions; which can be defined as **f(x)**, **g(x)** and **h(x)**.

* **g(x)** is a function which calculates the cost of the path from the start node to the current node, x.

* **h(x)** is the estimated cost of the path from the current node, x, to the end node. It is calculated using a heuristic. There are different
         heuristic functions we can use to calculate the estimated cost.
         
* **f(x)** is the function described by **g(x) + h(x)** and is used to describe the total estimated distance of the path to the end node.

The algorithm 'decides' which node to take next by calculating **f(x)** for each of the current node's neighbours, then selects the 
neighbour with the smallest **f(x)** value and stores the previous node visited throughout its path. Once the end node has been visited,
the algorithm uses its list of visited nodes to backtrack to the start node, thus creating a path between the start and end nodes.

<p align="center">
<img src = "https://user-images.githubusercontent.com/65727348/183499115-7368ea32-9dd8-4e1b-9f06-1ce416edc119.png" width="400"/>
</p>




