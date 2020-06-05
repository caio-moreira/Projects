import os
import time
from grids import AnswerGrid


class ValueIteration():
    """
    Description
    -----------
    Class that defines the Value Iteration algorithm.
    It is used to solve a planning problem by updating
    the costs based on the past costs.

    Parameters
    ----------
    test: Test() \\
        -- Test() object, based on which the algorithm will run.

    epsilon: float \\
        -- Used to stop tha algorithm. default = 1.0.

    Attributes
    ----------
    folder_name: str \\
        -- Folder where the test file is stored.

    file_name: str \\
        -- Name of the test file.

    states: StateSpace() \\
        -- StateSpace() object containing all the states.

    init: State() \\
        -- Initial state.

    goal: State() \\
        -- Final state.

    grid: Grid() \\
        -- The grid on which actions are being performed.

    epsilon: float \\
        -- Stopping criteria, when `max_diff` is smaller than this,
        the algorithm has converged.

    time_elapsed: int \\
        -- The time in milliseconds it took for the algorithm to run.

    iterations: int \\
        -- The number of iterations the algorithms took to converge.

    answer_grid: ArrowsGrid() \\
        -- A grid that represents the direction to follow when on each state.

    cost: dict \\
        -- A dict containing (name of the state, cost of the state) tuples.

    policies: dict \\
        -- A dict containing (
            name of the state, direction to follow while on the state
        ) tuples.

    max_diff: float \\
        -- The maximum difference by subtracting the past costs of
        each state from the current costs. Used to stop the algorithm
        along with `epsilon`.
    """

    def __init__(self, test, epsilon=1.0):
        self.folder_name = test.folder_name
        self.file_name = test.file_name

        self.states = test.states

        self.init = test.initial_state
        self.goal = test.goal_state

        self.grid = test.grid

        self.epsilon = epsilon

        self.time_elapsed = 0
        self.iterations = 0
        self.answer_grid = None

        self.costs = {}

        self.policies = {}

        self.max_diff = 1.0

    def __repr__(self):
        return f'ValueIteration({self.Test})'

    def __str__(self):
        return f'''File: {os.path.join(self.folder_name, self.file_name)}
Init: {self.init}
Goal: {self.goal}
Epsi: {self.epsilon}
Time: {self.time_elapsed} ms
Iter: {self.iterations}

Grid: {self.grid}

AnswerGrid: {self.answer_grid}'''

    def calculate_initial_cost(self):
        """
        Description
        -----------
        Computes the initial cost of each state.
        The cost is simply the manhattan distance from
        the state to the goal.
        """

        for name in self.states:
            state = self.states.get_state(name)

            x_dif = abs(state.x - self.goal.x)
            y_dif = abs(state.y - self.goal.y)

            cost = x_dif + y_dif

            self.costs.update({name: float(cost)})

    def update_costs(self):
        """
        Description
        -----------
        Updates the cost of each state using the Value Iteration approach
        takes the minimum cost of all the actions.

        Then computes the difference between each new cost and the old cost.
        """

        old_costs = self.costs.copy()

        for name in self.states:
            state = self.states.get_state(name)

            new_cost, policy = self.get_new_cost(state, old_costs)

            self.costs.update({name: new_cost})
            self.policies.update({name: policy})

        max_diff = 0

        for name in old_costs:
            diff_old_new = self.costs[name] - old_costs[name]

            if diff_old_new > max_diff:
                max_diff = diff_old_new

        self.max_diff = max_diff

    def get_new_cost(self, state, old_costs):
        """
        Description
        -----------
        Computes the cost of taking each action and selects the smallest.

        To compute the cost of an action it sums its cost with all the
        costs of end states multiplied by their probability.

        cost(a) = cost(a) + sum( all(cost(end_state) * probability) )

        Parameters
        -------
        state: State() \\
            -- State where the action begins.

        old_costs: dict \\
            -- Dict containing all the costs from the
            previous iteration for each state.

        Returns
        -------
        min_cost: float \\
            -- The new cost.

        policy: str \\
            -- The direction to follow.
        """

        min_cost = 0
        policy = '-'

        for action in state.actions:
            cost = action.cost

            for end_state, probability in action.end:
                cost = cost + (old_costs[end_state.name] * probability)

            if min_cost == 0 or min_cost > cost:
                min_cost = cost
                policy = action.direction

        return min_cost, policy

    def update_time_elapsed_ms(self):
        """
        Description
        -----------
        Updates `time_elapsed` attribute.

        Used two times, at the start and the end of the algorithm.

        start = current time - 0 \\
        end = current time - start
        """

        self.time_elapsed = int(round(time.time() * 1000)) - self.time_elapsed

    def run(self):
        """
        Description
        -----------
        Runs the algorithm, storing number of iterations and time elapsed.
        """

        self.update_time_elapsed_ms()

        self.calculate_initial_cost()

        while self.max_diff >= self.epsilon:
            self.update_costs()
            self.iterations += 1

        self.update_time_elapsed_ms()

        self.update_answer(AnswerGrid(
            self.states, self.policies, self.grid.shape,
            self.init, self.goal
        ).arrow_grid)

    def update_answer(self, answer):
        """
        Description
        -----------
        Updates the answer grid using the parameter.

        Parameters
        ----------
        answer: ArrowGrid()
        """

        self.answer_grid = answer
