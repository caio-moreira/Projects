from actions import ActionSet


class StateSpace():
    """
    Description
    -----------
    Class that acts as a storage for all the states available.
    It uses a dictionary to access the states.

    Attributes
    ----------
    states: dict \\
        -- a dictionary containing all the states available.
        It uses strings as keys and a State() objects as values.
    """

    def __init__(self):
        self.states = {}

    def __iter__(self):
        return iter(self.states)

    def load_states_list(self, states_list):
        """
        Description
        -----------
        Function used to update the `states` attribute.
        It instantiates a new State() object by getting the coordinates from
        the string using its standard (robot-at-x1y1) and updating the
        dictionary using the name of the state as the key.

        Parameters
        ----------
        states_list: list \\
            -- List containing all the names of the states.
        """

        for state_str in states_list:
            coordinates = state_str.split('x')[1]

            coordinates = coordinates.split('y')

            self.states.update({state_str: State(state_str, coordinates)})

    def update_coordinates(self, grid):
        """
        Description
        -----------
        Function used to update the coordinates for each state.

        Coordinates come in this format: \\
            (1, 2), (2,2) \\
            (1, 1), (2,1)

        They are converted to: \\
            (0, 0), (0,1) \\
            (1, 0), (1,1)

        Parameters
        ----------
        grid: Grid() \\
            -- Grid object that has the information needed to compute
            the new coordinates.
        """

        max_coordinate = grid.shape[0]

        for name, state in self.states.items():
            state.update_coordinates(max_coordinate)

    def get_state(self, name):
        """
        Description
        -----------
        Function used to get a state from the dictionary.

        Parameters
        ----------
        name: str \\
            -- String representing the name of the state.

        Returns
        -------
        State() \\
            -- The corresponding object requested.
        """

        return self.states[name]


class State():
    """
    Description
    -----------
    Class that acts as a storage for all the states available.
    It uses a dictionary to access the states.

    Parameters
    ----------
    state_str: str \\
        -- name of the state, folows a pattern (robot-at-x1y1).

    coordinates: list \\
        -- values of x and y.

    Attributes
    ----------
    name: str \\
        -- name of the state, folows a pattern (robot-at-x1y1).

    x: int \\
        -- value of x, 1 in the pattern above.
        Not yet converted.

    y: int \\
        -- value of x, 1 in the pattern above.
        Not yet converted.

    actions: ActionSet() \\
        -- ActionSet() containing the actions that are
        possible from this state.

    policy: str \\
        -- direction to which this state must go in order
        to get to the goal state.

    cost: int \\
        -- cost of getting from the state to the goal.

    predecessors: list \\
        -- list of states that lead to the current state.

    policy_predecessors: list \\
        -- list of states that lead to the current state
        when their policy is followed.
    """

    def __init__(self, state_str, coordinates):
        self.name = state_str

        self.x = int(coordinates[0])
        self.y = int(coordinates[1])

        self.actions = ActionSet(self)

        self.policy = None
        self.cost = None

        self.predecessors = []
        self.policy_predecessors = []

    def __repr__(self):
        return f'State({self.name}, [{self.x}, {self.y}])'

    def __str__(self):
        return f'Name: {self.name}, Coordinates: ({self.y}, {self.x})'

    def __eq__(self, other):
        return self.name == other.name

    def update_coordinates(self, max_coordinate):
        """
        Description
        -----------
        Function used to update the coordinates for the state.

        Parameters
        ----------
        max_coordinate: int \\
            -- Edge size of the Grid() object.
        """

        self.x = self.x - 1
        self.y = max_coordinate - self.y

    def update_policy(self, direction):
        """
        Description
        -----------
        Function used to update the `policy` attribute.

        Parameters
        ----------
        direction: str \\
            -- New direction to which the state should move.
        """

        self.policy = direction

    def update_cost(self, cost):
        """
        Description
        -----------
        Function used to update the `cost` attribute.

        Parameters
        ----------
        cost: int \\
            -- New cost.
        """

        self.cost = cost

    def add_predecessor(self, state):
        """
        Description
        -----------
        Function used to append a new state to the `predecessors` attribute.

        Parameters
        ----------
        state: State() \\
            -- State to be appended.
        """

        if state not in self.predecessors and state != self:
            self.predecessors.append(state)

    def add_policy_predecessor(self, state):
        """
        Description
        -----------
        Function used to append a new state to the
        `policy_predecessors` attribute.

        Parameters
        ----------
        state: State() \\
            -- State to be appended.
        """

        if state != self:
            self.policy_predecessors.append(state)

    def clean_policy_predecessors(self):
        """
        Description
        -----------
        Function used to clean the `policy_predecessors` attribute.
        For each new iteration, new policies, so, new predecessors.
        """

        self.policy_predecessors = []

    def update_action(self, direction, end_state, probability):
        """
        Description
        -----------
        Function used to update an action for the state.
        It has a probability because some states hava multiple
        end states, meaning each one has a probability of being
        the destination, they all add to 1.

        It also updates the `end_state.predecessors` attribute
        by adding the current state to  it.

        An action can lead to the same place that it has started from.

        Parameters
        ----------
        direction: str \\
            -- Direction to where the action points on the grid.

        end_state: State() \\
            -- State to which the action leads.

        probability: float \\
            -- Probability of, if using this action,
            winding up on `end_state`.
        """

        action = self.actions.get_action(direction)

        action.add_end_state(end_state, probability)

        end_state.add_predecessor(self)

    def update_action_cost(self, direction, cost):
        """
        Description
        -----------
        Function used to update the cost of an action.

        Parameters
        ----------
        direction: str \\
            -- Direction to where the action points on the grid.

        cost: float \\
            -- Cost of taking this action.
        """

        action = self.actions.get_action(direction)

        action.add_cost(cost)
