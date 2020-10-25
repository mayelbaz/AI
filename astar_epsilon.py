from .graph_problem_interface import *
from .astar import AStar
from typing import Optional, Callable
import numpy as np
import math


class AStarEpsilon(AStar):
    """
    This class implements the (weighted) A*Epsilon search algorithm.
    A*Epsilon algorithm basically works like the A* algorithm, but with
    another way to choose the next node to expand from the open queue.
    """

    solver_name = 'A*eps'

    def __init__(self,
                 heuristic_function_type: HeuristicFunctionType,
                 within_focal_priority_function: Callable[[SearchNode, GraphProblem, 'AStarEpsilon'], float],
                 heuristic_weight: float = 0.5,
                 max_nr_states_to_expand: Optional[int] = None,
                 focal_epsilon: float = 0.1,
                 max_focal_size: Optional[int] = None):
        # A* is a graph search algorithm. Hence, we use close set.
        super(AStarEpsilon, self).__init__(heuristic_function_type, heuristic_weight,
                                           max_nr_states_to_expand=max_nr_states_to_expand)
        self.focal_epsilon = focal_epsilon
        if focal_epsilon < 0:
            raise ValueError(f'The argument `focal_epsilon` for A*eps should be >= 0; '
                             f'given focal_epsilon={focal_epsilon}.')
        self.within_focal_priority_function = within_focal_priority_function
        self.max_focal_size = max_focal_size

    def _init_solver(self, problem):
        super(AStarEpsilon, self)._init_solver(problem)

    def _extract_next_search_node_to_expand(self, problem: GraphProblem) -> Optional[SearchNode]:
        """
        Extracts the next node to expand from the open queue,
         by focusing on the current FOCAL and choosing the node
         with the best within_focal_priority from it.
        TODO [Ex.38]: Implement this method!
        Find the minimum expanding-priority value in the `open` queue.
        Calculate the maximum expanding-priority of the FOCAL, which is
         the min expanding-priority in open multiplied by (1 + eps) where
         eps is stored under `self.focal_epsilon`.
        Create the FOCAL by popping items from the `open` queue and inserting
         them into a focal list. Don't forget to satisfy the constraint of
         `self.max_focal_size` if it is set (not None).
        Notice: You might want to pop items from the `open` priority queue,
         and then choose an item out of these popped items. Don't forget:
         the other items have to be pushed back into open.
        Inspect the base class `BestFirstSearch` to retrieve the type of
         the field `open`. Then find the definition of this type and find
         the right methods to use (you might want to peek the head node, to
         pop/push nodes and to query whether the queue is empty).
        For each node (candidate) in the created focal, calculate its priority
         by callingthe function `self.within_focal_priority_function` on it.
         This function expects to get 3 values: the node, the problem and the
         solver (self). You can create an array of these priority value. Then,
         use `np.argmin()` to find the index of the item (within this array)
         with the minimal value. After having this index you could pop this
         item from the focal (at this index). This is the node that have to
         be eventually returned.
        Don't forget to handle correctly corner-case like when the open queue
         is empty. In this case a value of `None` has to be returned.
        Note: All the nodes that were in the open queue at the beginning of this
         method should be kept in the open queue at the end of this method, except
         for the extracted (and returned) node.
        """
        if self.open.is_empty():
            return None

        min_exp = self.open.peek_next_node()    # open is heapdisct() => peak returns the min priority
        max_focal_exp = min_exp.expanding_priority * (1 + self.focal_epsilon)
        focal = []
        focal_vals = []
        return_to_open = []     # store all the pop'ed nodes from open in order to push back in at the end of the method

        # check if max_focal_size if set, and initiate indicator
        if self.max_focal_size is not None:
            max_focal_size_is_set = True
        else:
            max_focal_size_is_set = False

        while not self.open.is_empty():
            # check if the focal group has reached capacity
            if max_focal_size_is_set:
                if len(focal) >= self.max_focal_size:
                    break
            node_to_check = self.open.pop_next_node()
            # if current node matches the focal group criteria
            if node_to_check.expanding_priority <= max_focal_exp:
                # insert into focal group
                focal.append(node_to_check)
                # insert the value into the list
                focal_vals.append(self.within_focal_priority_function(node_to_check, problem, self))
            # insert all popped nodes to the kept list
            return_to_open.append(node_to_check)

        min_index = np.array(focal_vals).argmin()
        min_in_focal = np.array(focal)[min_index]
        # extract the min priority node from the list of the nodes that are to be pushed back to open
        return_to_open.remove(min_in_focal)

        # restore the state of open save for our min node, which is to be returned
        for node in return_to_open:
            self.open.push_node(node)

        if self.use_close:
            self.close.add_node(min_in_focal)

        return min_in_focal





