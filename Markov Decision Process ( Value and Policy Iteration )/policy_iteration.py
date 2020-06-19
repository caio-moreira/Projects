import os
import time
from grids import AnswerGrid
from value_iteration import ValueIteration


class PolicyIteration(ValueIteration):
    """
    Description
    -----------
    Class that defines the Policy Iteration algorithm.
    It is used to solve a planning problem by updating
    the policies based on the costs of the policies.

    It inherits most of its attributes and methods from
    the `ValueIteration` class.

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
        -- Stopping criteria, when `max_residual` is smaller than this,
        the algorithm has converged.
        -- Not used in Policy Iteration

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
        -- Not used in Policy Iteration

    initial_policy_grid: Grid() \\
        -- The grid representing the initial state, only used if one wants
        to compare it with the `answer_grid`.

    policies_costs: dict \\
        -- A dict with the same structure as the `costs` attribute.
        It is used to store the costs of following the policies
        for each state.
    """

    def __init__(self, test):
        super().__init__(test)

        self.initial_policy_grid = None

        self.policies_costs = {}

        self.get_initial_policy()

    def __repr__(self):
        return f'PolicyIteration({self.Test})'

    def __str__(self):
        return f'''File: {os.path.join(self.folder_name, self.file_name)}
Initial: {self.init}
Goal: {self.goal}

Time: {self.time_elapsed} ms
Iterations: {self.iterations}

Costs: {self.costs}
Policies: {self.policies}

Grid: {self.grid}

InitialPolicyGrid: {self.initial_policy_grid}

AnswerGrid: {self.answer_grid}'''

    def get_initial_policy(self):
        """
        Description
        -----------
        Computes the initial policy for each state.

        Uses a depth-first search approach.
        """

        self.policies.update({self.goal.name: '-'})

        self.goal.update_policy('-')
        self.goal.update_cost(0.0)

        current_state = self.goal

        updated_states = []

        while current_state is not None:
            for state in current_state.predecessors:
                if state.name not in self.policies.keys():
                    self.add_cost_and_policy(state, current_state)

                    updated_states.append(state)

            if not updated_states:
                break

            current_state = updated_states.pop()

        self.initial_policy_grid = AnswerGrid(
            self.states, self.policies, self.grid.shape,
            self.init, self.goal
        ).arrow_grid

    def add_cost_and_policy(self, initial_state, end_state):
        """
        Description
        -----------
        Adds a cost and a policy to the initial state, leading
        to the end state.

        Parameters
        ----------
        initial_state: State() \\
            -- The current state.

        end_state: State() \\
            -- The state to where this one should lead to.

        Returns
        -------
        None \\
            -- If `initial_state` and `end_state` are the same
            returns `None`.
        """

        if initial_state == end_state:
            return None

        name = initial_state.name

        policy = ''
        cost = 0

        number_of_end_states = [
            (action, len(action.end)) for action in initial_state.actions
        ]

        number_of_end_states.sort(key=lambda tup: tup[1])

        for action, n_states in number_of_end_states:
            end_states = [tup[0] for tup in action.end]
            probabilities = [tup[1] for tup in action.end]

            if end_state in end_states:
                policy = action.direction

                cost = action.cost + end_state.cost

                break

        self.policies.update({name: policy})

        initial_state.update_policy(policy)
        initial_state.update_cost(cost)

    def calculate_initial_cost(self):
        """
        Description
        -----------
        Computes the initial cost of each state.
        The cost is the cost of following the initial
        state's policy to get to the goal state.
        """

        for name in self.policies.keys():
            state = self.states.get_state(name)

            cost = state.cost

            self.costs.update({name: float(cost)})

    def evaluate_policies(self):
        """
        Description
        -----------
        Computes the cost of each new policy and then replaces
        the current costs with those.
        """

        for name, policy in self.policies.items():
            if name == self.goal.name:
                self.policies_costs.update({name: 0.0})

                continue

            state = self.states.get_state(name)

            action = state.actions.get_action(str('move-' + policy))

            policy_cost = self.compute_cost(action, self.costs)

            self.policies_costs.update({name: policy_cost})

        self.costs = self.policies_costs.copy()

    def run(self):
        """
        Description
        -----------
        Runs the algorithm, storing number of iterations and time elapsed.
        """

        self.update_time_elapsed_ms()

        self.calculate_initial_cost()

        run = True

        while run:
            old_policies = self.policies.copy()

            self.update_costs_and_policies()

            self.evaluate_policies()

            self.iterations += 1

            if old_policies == self.policies:
                run = False

        self.update_time_elapsed_ms()

        self.update_answer()
