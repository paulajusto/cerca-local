from typing import Generator
from azamon_operators import AzamonOperators
from azamon_state import StateAzamon
from aima.search import Problem


class AzamonProblem(Problem):
    def __init__(self, initial_state: StateAzamon):
        super().__init__(initial_state)

    def actions(self, state: StateAzamon) -> Generator[AzamonOperators, None, None]:
        return state.generate_actions()

    def result(self, state: StateAzamon, action: AzamonOperators) -> StateAzamon:
        return state.apply_action(action)

    def value(self, state: StateAzamon) -> float:
        return -state.heuristic()

    def goal_test(self, state: StateAzamon) -> bool:
        return False
    
    def neighbors(self, state):
        """Devuelve una lista de estados vecinos a partir del estado dado."""
        neighbors = []
        for action in self.actions(state):
            new_state = self.result(state, action)
            neighbors.append(new_state)  # Solo agregamos el nuevo estado
        return neighbors    
    
