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

        self.improvement_time_elapsed = 0
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

Total Time: {self.time_elapsed} ms
    Improvement Time: {self.improvement_time_elapsed} ms
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

        Uses a breadth-first search approach.
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

            self.improvement_time_elapsed += self.time_it(
                self.update_costs_and_policies
            )

            self.evaluation_time_elapsed += self.time_it(
                self.evaluate_policies
            )

            self.iterations += 1

            if old_policies == self.policies:
                run = False

        self.time_elapsed = (
            self.improvement_time_elapsed + self.evaluation_time_elapsed
        )

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

        So, let's take an example action that might be here for us to
        evaluate.

        On state X, action A leads to (Y and X), each with 0.5 probabilty and
        action cost = 1.
        In this scenario Y is the ultimate goal state, so its cost is 0.

        In order to evaluate the cost of X, the equation is the following:

        `X.cost = 0.5 * (A.cost + Y.cost) + 0.5 * (A.cost + X.cost)`

        We know the cost of Y is 0 and the cost of A is 1, so:

        `X.cost = 0.5 * (1 + 0) + 0.5 * (1 + X.cost)` \\
        `X.cost = 0.5 + 0.5*1 + 0.5 * X.cost` \\
        `X.cost = 1 + 0.5 * X.cost` (Minimized equation of X.cost)

        Right here, the value of the cost of X is unknown, because that's
        what the equation is trying to figure out. In order to solve this
        just like a common high school equation we just subtract
        `0.5 * X.cost` from both sides, like so:

        `X.cost - 0.5 * X.cost = 1 + 0.5 * X.cost - 0.5 * X.cost` \\
        `0.5 * X.cost = 1`

        Then, we divide both sides by `0.5`:

        `0.5 * X.cost / 0.5 = 1 / 0.5` \\
        `X.cost = 2`

        Easy right? But the problem here is how to do that in a
        computationally unexpensive way.

        So, the first step was done already, suppose a state depends on X,
        let's call it state W. So in order to compute W's cost we need to
        know X's cost. How do we ensure that X's cost is computed before
        W's?

        Easy, W's cost is always higher than X's, because it is some sort of
        sum of W's action cost and X's own cost, so we create a list of all
        states sorted by their ascending previous cost, which we already did,
        then we compute each value starting from the first state (goal state,
        cost = 0), that way, we make sure all of the states like our
        exemplified X are calculated first.

        So after all of that is cleared, how to do the math in code?

        Well, let's take our own X again, same X, same action A.
        Here's the minimized equation for X.cost:

        `X.cost = 1 + 0.5 * X.cost`

        We already know it's value is 2. we want to eliminate X.cost
        from the right and divide everything by 0.5, that would give us 2.

        But we can't simply say that the right X.cost is 0 and the left one
        is 2, that's wrong, but we can replace the right X.cost for something.

        What? You'd ask me. Well, we can substitute that value for its
        absolute distance to the one we are trying to find. But we don't
        know them, how to get the absolute distance? Simple, we use the
        past distance, from the values in `self.old_costs`. Let me show why.

        Let's take new states, A, B and C. C is the goal. This is their
        structure:

        A has an action (Y) that leads to both C and B, cost = 2 and
        respective probabilities are 0.6 and 0.4.

        B has an action (Z) that leads only to A with cost 1.

        So we have a loop. How does this work? B's cost depends on A's,
        so A's cost will be calculated first. Here it goes:

        `A.cost = 0.6 * (Y.cost + C.cost) + 0.4 * (Y.cost + B.cost)` \\
        `A.cost = 0.6 * (2 + 0) + 0.4 * (2 + B.cost)` \\
        `A.cost = 1.2 + 0.8 + 0.4 * B.cost`

        Having `B.cost = Z.cost + A.cost` and substituting that.
        Following the same mathematical logic used to get X's cost.

        `A.cost = 2 + 0.4 * (Z.cost + A.cost)` \\
        `A.cost = 2 + 0.4 * (1 + A.cost)` \\
        `A.cost = 2.4 + 0.4 * A.cost` \\
        `0.6 * A.cost = 2.4` (Subtracting 0.4 * A.cost on both sides) \\
        `A.cost = 4` (Dividing both sides by 0.6)

        What if, from the beginning, we had subtracted A and B cost's? What
        would we have left? 1, because that is the cost of the action that
        leads from B to A. So, applying the cost difference approach.

        `A.cost = 1.2 + 0.8 + 0.4 * abs(A.old_cost - B.old_cost)`\\
        `A.cost = 2 + 0.4 * 1` \\
        `A.cost = 2.4`

        That's wrong, but it's almost right, its missing something, the
        division by a number, number which is represented by 1 minus the
        probability that we used to multiply our cost difference (0.4), so
        `1 - 0.4 = 0.6` then we have an answer:

        `A.cost = 2.4 / 0.6` \\
        `A.cost = 4`

        But would it work for our first example? Let's try.

        `X.cost = 1 + 0.5 * abs(X.old_cost - X.old_cost)` \\
        `X.cost = 1 + 0.5 * 0` \\
        `X.cost = 1` (Let's not forget to divide by `1 - probability`) \\
        `X.cost = 1 / 0.5`
        `X.cost = 2`

        This is the best way to explain I could think of, hope it's clear.

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

                factor *= 1 - probability

                if factor == 0:
                    factor = 1

                cost_correction = abs(
                    self.old_costs[state.name] - self.old_costs[end.name]
                )

                cost += probability * (action.cost + cost_correction)
            else:
                cost += probability * (action.cost + costs[end.name])

        return round(cost / factor, 5)
