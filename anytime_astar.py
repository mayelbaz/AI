from .graph_problem_interface import *
from .astar import AStar
from .utils.timer import Timer


class AnytimeAStar(GraphProblemSolver):

    solver_name = 'Anytime-A*'

    def __init__(self,
                 heuristic_function_type: HeuristicFunctionType,
                 max_nr_states_to_expand_per_iteration: int,
                 initial_high_heuristic_weight_bound: float = 0.9):
        self.heuristic_function_type = heuristic_function_type
        self.max_nr_states_to_expand_per_iteration = max_nr_states_to_expand_per_iteration
        self.initial_high_heuristic_weight_bound = initial_high_heuristic_weight_bound

    def solve_problem(self, problem: GraphProblem) -> SearchResult:
        with Timer(print_title=False) as timer:
            total_nr_expanded_states = 0
            max_nr_stored_states = 0

            acceptable_astar = AStar(heuristic_function_type=self.heuristic_function_type, heuristic_weight=0.5,
                                     max_nr_states_to_expand=self.max_nr_states_to_expand_per_iteration)
            acceptable_astar_res = acceptable_astar.solve_problem(problem)
            total_nr_expanded_states += acceptable_astar_res.nr_expanded_states
            max_nr_stored_states = max(max_nr_stored_states, acceptable_astar_res.max_nr_stored_states)
            if acceptable_astar_res.is_solution_found:
                return acceptable_astar_res._replace(
                    solver=self, nr_expanded_states=total_nr_expanded_states, solving_time=timer.elapsed)

            greedy = AStar(heuristic_function_type=self.heuristic_function_type,
                           heuristic_weight=self.initial_high_heuristic_weight_bound,
                           max_nr_states_to_expand=self.max_nr_states_to_expand_per_iteration)
            greedy_res = greedy.solve_problem(problem)
            total_nr_expanded_states += greedy_res.nr_expanded_states
            max_nr_stored_states = max(max_nr_stored_states, greedy_res.max_nr_stored_states)
            if not greedy_res.is_solution_found:
                return greedy_res._replace(
                    solver=self, nr_expanded_states=total_nr_expanded_states, solving_time=timer.elapsed)
            best_solution = greedy_res
            best_heuristic_weight = self.initial_high_heuristic_weight_bound

            # Invariant being hold during the loop:
            #   There is a solution using `high_heuristic_weight`,
            #   but there is no solution using `low_heuristic_weight`.
            low_heuristic_weight = 0.5
            high_heuristic_weight = self.initial_high_heuristic_weight_bound
            while (high_heuristic_weight - low_heuristic_weight) > 0.01:
               
                mid = ((low_heuristic_weight + high_heuristic_weight)/2)
                # create an Astar solver with;
                Astar_solver = AStar(heuristic_function_type=self.heuristic_function_type,
                                     heuristic_weight=mid,
                                     max_nr_states_to_expand=self.max_nr_states_to_expand_per_iteration)
                tmp_sol = Astar_solver.solve_problem(problem)

                # Don't forget to update `total_nr_expanded_states` and `max_nr_stored_states
                total_nr_expanded_states += tmp_sol.nr_expanded_states
                max_nr_stored_states = max(max_nr_stored_states, tmp_sol.max_nr_stored_states)

                #  You might need to use the field `is_solution_found` of the search result obtained from the AStar.
                if tmp_sol.is_solution_found:
                    #  Update iff the current inspected solution cost < the cost of the best found solution so far.
                    if tmp_sol.solution_g_cost < best_solution.solution_g_cost:
                        best_solution = tmp_sol
                        best_heuristic_weight = mid
                    high_heuristic_weight = mid
                else:
                    low_heuristic_weight = mid

        self.solver_name = f'{self.__class__.solver_name} ' \
                           f'(h={best_solution.solver.heuristic_function.heuristic_name}, ' \
                           f'w={best_heuristic_weight:.3f})'
        return best_solution._replace(
            solver=self, nr_expanded_states=total_nr_expanded_states, max_nr_stored_states=max_nr_stored_states,
            solving_time=timer.elapsed)
