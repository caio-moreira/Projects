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
    name: str \\
        -- Name of the algorithm, used as folder name to store the results.

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
        -- Stopping criteria, when `max_residual` is smaller than this,
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

    max_residual: float \\
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

        self.max_residual = 1.0

    def __repr__(self):
        return f'ValueIteration({self.Test})'

    def __str__(self):
        return f'''File: {os.path.join(self.folder_name, self.file_name)}
Initial: {self.init}
Goal: {self.goal}
Epsilon: {self.epsilon}

Time: {self.time_elapsed} ms
Iterations: {self.iterations}

Costs: {self.costs}
Policies: {self.policies}

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

    def update_costs_and_policies(self):
        """
        Description
        -----------
        Updates the cost and the repective policy for each state
        taking the minimum cost of all the actions and the action
        itself as the policy.

        Then computes the difference between each new cost and the old cost.
        """

        old_costs = self.costs.copy()

        for name in self.states:
            state = self.states.get_state(name)

            new_cost, policy = self.get_min_cost(state, old_costs)

            self.costs.update({name: new_cost})
            self.policies.update({name: policy})

            state.update_policy(policy)

        max_residual = 0

        for name in old_costs:
            residual = abs(self.costs[name] - old_costs[name])

            if residual > max_residual:
                max_residual = residual

        self.max_residual = max_residual

    def get_min_cost(self, state, old_costs):
        """
        Description
        -----------
        Computes the cost of taking each action and selects the
        least costly one.

        To compute the cost of an action it sums its cost with all the
        costs of end states multiplied by their probability.

        cost(a) = sum( all(cost(a) + cost(end_state) * probability) )

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
            cost = 0

            cost += self.compute_cost(action, old_costs)

            if min_cost == 0 or min_cost > cost:
                min_cost = cost
                policy = action.direction

        return min_cost, policy

    def compute_cost(self, action, states_costs):
        """
        Description
        -----------
        Computes the cost of taking each action and selects the smallest.

        To compute the cost of an action it sums its cost with all the
        costs of end states multiplied by their probability.

        cost(a) = sum( all( probability * (cost(a) + cost(end_state)) ) )

        Parameters
        -------
        action: Action() \\
            -- Action to compute the cost.

        states_costs: dict \\
            -- Dict containing all the costs from the
            previous iteration for each state.

        Returns
        -------
        cost: float \\
            -- The new cost.
        """
        cost = 0

        for end_state, probability in action.end:
            cost += probability * (action.cost + states_costs[end_state.name])

        return round(cost, 2)

    def update_time_elapsed_ms(self):
        """
        Description
        -----------
        Updates `time_elapsed` attribute.

        Used two times, at the start and the end of the algorithm.

        start = current time - 0 \\
        end = current time - start
        """

        self.time_elapsed = round((time.time() * 1000) - self.time_elapsed, 2)

    def run(self):
        """
        Description
        -----------
        Runs the algorithm, storing number of iterations and time elapsed.
        """

        self.update_time_elapsed_ms()

        self.calculate_initial_cost()

        while self.max_residual >= self.epsilon:
            self.update_costs_and_policies()
            self.iterations += 1

        self.update_time_elapsed_ms()

        self.update_answer()

    def update_answer(self):
        """
        Description
        -----------
        Updates the answer grid using the parameter.
        """

        self.answer_grid = AnswerGrid(
            self.states, self.policies, self.grid.shape,
            self.init, self.goal
        ).arrow_grid
