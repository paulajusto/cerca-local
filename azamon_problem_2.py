from typing import Generator

from aima.search import Problem

from azamon_operators import AzamonOperators
from azamon_state import StateAzamon


class AzamonProblem2(Problem):
    def __init__(self, initial_state: StateAzamon):
        super().__init__(initial_state)

    def actions(self, state: StateAzamon) -> Generator[AzamonOperators, None, None]:
        return state.generate_actions()

    def result(self, state: StateAzamon, action: AzamonOperators) -> StateAzamon:
        return state.apply_action(action)

    def value(self, state: StateAzamon) -> float:
        return -state.heuristic_costes()

    def goal_test(self, state: StateAzamon) -> bool:
        return False
