from .graph_problem_interface import *
from .astar import AStar
from typing import Optional, Callable
import numpy as np
import math


class AStarEpsilon(AStar):

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





