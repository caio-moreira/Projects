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
        -- Not used in Policy Iteration.

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
        -- Not Used in Policy Iteration.

    initial_policy_grid: Grid() \\
        -- The grid representing the initial state, only used if one wants
        to compare it with the `answer_grid`.

    old_costs: dict \\
        -- A dict with the same structure as the `costs` attribute.
        It is used to store the previous costs.

    evaluation_time_elapsed: int \\
        -- Time in milliseconds spent on evaluation step. \\
        `evaluation_time_elapsed` =
            `evaluation_list_time_elapsed` + `evaluation_cost_time_elapsed`

    evaluation_list_time_elapsed: int \\
        -- Time in milliseconds spent on creating the
        evaluation order list step.

    evaluation_cost_time_elapsed: int \\
        -- Time in milliseconds spent on evaluation function step.

    policy_cost_calculation_time_elapsed: int \\
        -- Time in milliseconds spent on cost calculation step.
        Part of `evaluation_cost_time_elapsed`.
    """

    def __init__(self, test):
        super().__init__(test)

        self.initial_policy_grid = None

        self.old_costs = {}

        self.evaluation_time_elapsed = 0

        self.evaluation_list_time_elapsed = 0
        self.evaluation_cost_time_elapsed = 0
        self.policy_cost_calculation_time_elapsed = 0

        self.get_initial_policy()

    def __repr__(self):
        return f'PolicyIteration({self.Test})'

    def __str__(self):
        return f'''File: {os.path.join(self.folder_name, self.file_name)}
Initial: {self.init}
Goal: {self.goal}

Total Time: {self.time_elapsed + self.evaluation_time_elapsed} ms
    Improvement Time: {self.time_elapsed} ms
    Evaluation Time: {self.evaluation_time_elapsed} ms
        List Creation Time: {self.evaluation_list_time_elapsed} ms
        Evaluation Function Time: {self.evaluation_cost_time_elapsed} ms
            Calculation Time: {self.policy_cost_calculation_time_elapsed} ms
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
        Computes the initial policy and cost for each state.

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

    def run(self):
        """
        Description
        -----------
        Runs the algorithm, storing number of iterations and time elapsed.
        """

        self.calculate_initial_cost()

        run = True

        while run:
            old_policies = self.policies.copy()

            self.old_costs = self.costs.copy()

            self.time_elapsed += self.time_it(
                self.update_costs_and_policies
            )

            self.evaluation_time_elapsed += self.time_it(
                self.evaluate_policies
            )

            self.iterations += 1

            if old_policies == self.policies:
                run = False

        self.update_answer()

    def calculate_initial_cost(self):
        """
        Description
        -----------
        Gets the initial cost from each state.
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

        evaluation_list_time_spent, states_sorted = self.time_it(
            self.get_evaluation_order
        )

        self.evaluation_list_time_elapsed += evaluation_list_time_spent

        evaluation_cost_time_spent, policies_costs = self.time_it(
            self.get_evaluation_costs, states_sorted
        )

        self.evaluation_cost_time_elapsed += evaluation_cost_time_spent

        self.costs = policies_costs

    def get_evaluation_order(self):
        """
        Description
        -----------
        Gets a list of all states sorted by ascending cost.

        It is used to evaluate policy in order.

        Returns
        -------
        list \\
            -- Sorted list of states' names.
        """

        index = 0

        next_states = list({
            name: cost
            for name, cost in sorted(
                self.costs.items(), key=lambda item: item[1]
            )
        }.keys())

        return next_states

    def get_evaluation_costs(self, states_sorted):
        """
        Description
        -----------
        Evaluates the cost of following the policy
        for each state.

        Parameters
        ----------
        states_sorted: list \\
            -- List of states' names sorted by cost.

        Returns
        -------
        dict \\
            -- Dict consisting of {state name: policy cost}.
        """

        new_costs = {}

        while states_sorted != []:
            name = states_sorted.pop(0)

            state = self.states.get_state(name)

            if state == self.goal:
                new_costs.update({self.goal.name: 0.0})

                continue

            policy = self.policies[name]

            action = state.actions.get_action(policy)

            time_spent, policy_cost = self.time_it(
                self.get_policy_cost,
                state, action, new_costs
            )

            self.policy_cost_calculation_time_elapsed += time_spent

            new_costs.update({name: policy_cost})

            state.update_cost(policy_cost)

        return new_costs

    def get_policy_cost(self, state, action, costs):
        """
        Description
        -----------
        Computes the cost of following the policy
        for a given state and respective action.

        This is a diffrent way of approaching the iterative solution.

        The iterative solution takes the old cost and iterates from it.

        So, for each iteration:

        prob = probability
        act = action cost
        cost = end state old cost

        `cost = sum( all( prob * (act + cost) ) )`

        Repeats this for all states and repeats until the
        maximum residual (difference between old and new cost)
        is smaller than a threshold (epsilon).

        This approach executes an infinite loop of the iterative
        evaluation in a single calculation, by following the pattern:

        `cost_corr` is the absolute difference between the cost of the current
        state and the cost of the end state. So, it substitutes the action
        cost should go, since it its the cost of going from the end state
        back to the current one or the other way around.

        `... prob * (cost_corr + prob * (cost_corr  + prob * (cost_corr + cost)))`

        Which is equal to:

        `prob*cost_corr + prob^2*cost_corr + ... + prob^infinity * (cost_corr)))
        + prob^infinity * (act + cost)`

        So, this lead to a infinite geometric series, starting on
        `prob * cost_corr` with ratio `prob` + last term, which is
        `(prob ^ infinity) * (cost_corr + cost)`, which is tends to 0,
        so its ignored.

        The sum of an infinite geometric series is:

        `initial term * / 1 - ratio`

        Since in the code bellow `factor = 1 - probability`
        the sum is equal to `probability * cost_correction / factor`.

        But also, the rest of the cost sum equation must be
        divided by the factor. That's why factor is only used
        when returning the result.

        And since we might have multiple end states that lead
        to an infinite geometric series, `factor` is multiplied
        by the new factor `factor *= 1 - prob`.

        Parameters
        ----------
        state: State() \\
            -- The state to be evaluated.

        action: Action() \\
            -- The action corresponding to the policy
            to evaluate.

        costs: dict \\
            -- Dict of all the states that were already
            evaluated.

        Returns
        -------
        int \\
            -- The cost of following the policy.
        """

        cost = 0

        factor = 1

        for end, probability in action.end:
            if end.name not in costs.keys():
                end_policy = self.policies[end.name]

                end_policy_action = end.actions.get_action(end_policy)

                factor = 1 - probability

                if factor == 0:
                    factor = 1

                cost_correction = abs(
                    self.old_costs[state.name] - self.old_costs[end.name]
                )

                geo_prog_sum = (probability * cost_correction)

                cost += probability * action.cost + geo_prog_sum
            else:
                cost += probability * (action.cost + costs[end.name])

        return round(cost / factor, 5)
