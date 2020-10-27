from .graph_problem_interface import *
from .best_first_search import BestFirstSearch
from typing import Optional, Callable


class AStar(BestFirstSearch):
    """
    This class implements the Weighted-A* search algorithm.
    A* algorithm is in the Best First Search algorithms family.
    """

    solver_name = 'A*'

    def __init__(self, heuristic_function_type: HeuristicFunctionType, heuristic_weight: float = 0.5,
                 max_nr_states_to_expand: Optional[int] = None,
                 open_criterion: Optional[Callable[[SearchNode], bool]] = None):
 
        # A* is a graph search algorithm. Hence, we use close set.
        super(AStar, self).__init__(
            use_close=True, max_nr_states_to_expand=max_nr_states_to_expand, open_criterion=open_criterion)
        self.heuristic_function_type = heuristic_function_type
        self.heuristic_function = None
        self.heuristic_weight = heuristic_weight

    def _init_solver(self, problem):
        
        super(AStar, self)._init_solver(problem)
        self.heuristic_function = self.heuristic_function_type(problem)
        self.solver_name = f'{self.__class__.solver_name} (h={self.heuristic_function.heuristic_name}, w={self.heuristic_weight:.3f})'

    def _calc_node_expanding_priority(self, search_node: SearchNode) -> float:
  
        return (((1 - self.heuristic_weight) * search_node.g_cost) + (
                    self.heuristic_weight * self.heuristic_function.estimate(search_node.state)))

    def _open_successor_node(self, problem: GraphProblem, successor_node: SearchNode):
       
        if self.open.has_state(successor_node.state):
            old_node = self.open.get_node_by_state(successor_node.state)
            if successor_node.g_cost < old_node.g_cost:
                self.open.extract_node(old_node)
                self.open.push_node(successor_node)
        elif self.close.has_state(successor_node.state):
            old_node = self.close.get_node_by_state(successor_node.state)
            if successor_node.g_cost < old_node.g_cost:
                # remove old path- only if new one is better
                self.close.remove_node(old_node)
                # goes into the open queue
                self.open.push_node(successor_node)
        else:
            self.open.push_node(successor_node)


