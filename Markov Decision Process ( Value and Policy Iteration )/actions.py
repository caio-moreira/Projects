

class ActionSet():
    """
    Description
    -----------
    Class that acts as a storage for all the actions available.
    It returns a list containing all non-empty action when called
    as an iterable.

    Parameters
    ----------
    state: State() \\
        -- State where the action begins.

    Attributes
    ----------
    start: State() \\
        -- State where the action begins.

    north: Action() \\
        -- Action when one follows up on the grid.

    south: Action() \\
        -- Action when one follows down on the grid.

    east: Action() \\
        -- Action when one follows left on the grid.

    west: Action() \\
        -- Action when one follows right on the grid.
    """

    def __init__(self, state):
        self.start = state

        self.north = Action(state, 'north')
        self.south = Action(state, 'south')
        self.east = Action(state, 'east')
        self.west = Action(state, 'west')

    def __iter__(self):
        action_list = [self.north, self.south, self.east, self.west]

        action_list = [i for i in action_list if i.end != []]

        return iter(action_list)

    def __repr__(self):
        return f'ActionSet({self.start})'

    def __str__(self):
        return f'''
            {self.north}
            {self.south}
            {self.east}
            {self.west}
        '''

    def get_action(self, direction):
        """
        Description
        -----------
        Returns an action based on a string.

        Parameters
        -------
        direction: str \\
            -- String used to retrieve the action.

        Returns
        -------
        Action() \\
            -- The action requested.
        """

        if direction == 'move-north':
            return self.north
        elif direction == 'move-south':
            return self.south
        elif direction == 'move-east':
            return self.east
        elif direction == 'move-west':
            return self.west


class Action():
    """
    Description
    -----------
    Class that stores the information relevant for an action.

    Attributes
    ----------
    start: State() \\
        -- State where the action begins.

    direction: string \\
        -- Direction to where the action points.

    Attributes
    ----------
    start: State() \\
        -- State where the action begins.

    end: list \\
        -- A list containing tuples like (State(), probability).

    cost: float \\
        -- Cost of taking this action.

    direction: string \\
        -- Direction to where the action points.
    """

    def __init__(self, state, direction):
        self.start = state
        self.end = []
        self.cost = 0.0

        self.direction = direction

    def __repr__(self):
        return f'Action({self.start}, {self.direction})'

    def __str__(self):
        return f'''{self.start.name}
    {self.direction}: {self.end}
    Cost: {self.cost}
        '''

    def add_end_state(self, end_state, probability):
        """
        Description
        -----------
        Appends an end state to the action.

        Parameters
        ----------
        end_state: State() \\
            -- One of the states where the action leads to.

        probability: float \\
            -- The chance of winding up on that state by taking this action.
        """

        self.end.append((end_state, float(probability)))

    def add_cost(self, cost):
        """
        Description
        -----------
        Updates the cost of taking the action.

        Parameters
        ----------
        cost: float \\
            -- The cost of taking this action.
        """

        self.cost = float(cost)
