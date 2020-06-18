

class Grid():
    """
    Description
    -----------
    Class that acts as a grid, a place where the actions take effect
    and where the states are mirrored via coordinates.

    Attributes
    ----------
    start: list \\
        -- Two element array, has the grid's edge's sizes,
        they are most likely the same, since the grids are squares.

    grid: list \\
        -- A list containing all the list that represent
        the rows of the grid.
    """

    def __init__(self):
        self.shape = [0, 0]
        self.grid = []

    def __repr__(self):
        return 'Grid()'

    def __str__(self):
        grid_str = ''

        for row in self.grid:
            for item in row:
                grid_str = grid_str + str(item) + ' '

            grid_str = grid_str + '\n'

        return f'Shape: {self.shape}\n\n{grid_str}'

    def add_row(self, row):
        """
        Description
        -----------
        Adds a row to the grid, converting each position
        to a GridPosition() object.

        Parameters
        -------
        row: list \\
            -- String used to retrieve the action.
        """

        aux_row = []

        for value in row:
            aux_row.append(GridPosition(value))

        self.grid.append(aux_row)

    def update_shape(self):
        """
        Description
        -----------
        Updates the `shape` attribute by computing its values.
        """

        x = len(self.grid[0])
        y = len(self.grid)

        self.shape = [x, y]


class GridPosition():
    """
    Description
    -----------
    Class that acts as a grid position, it nhas the information
    needed to print the grid and used to build the object.

    Code \\
        0 - free \\
        1 - wall \\
        2 - initial state \\
        3 - goal state \\
        4 - near a wall

    Parameters
    ----------
    value: int \\
        -- The code used for the position.

    Attributes
    ----------
    value: int \\
        -- The code used for the position.

    pos_type: str \\
        -- Meaning of the code.

    pos_char: str \\
        -- First leter of the type.
    """

    def __init__(self, value):
        self.value = int(value)
        self.pos_type = None
        self.pos_char = None

        self.update_pos_type()

    def __repr__(self):
        return f'GridPosition({self.value})'

    def __str__(self):
        return f'{self.pos_char}'

    def update_pos_type(self):
        """
        Description
        -----------
        Updates a position type by using a code,
        which is represented in the if chain below.

        Init and Goal start with uppercase letters so that they
        are easily spotted on the grid when printed
        """

        if self.value == 1:
            self.pos_type = 'wall'
        elif self.value == 2:
            self.pos_type = 'Init'
        elif self.value == 3:
            self.pos_type = 'Goal'
        else:
            self.pos_type = 'free'

        self.pos_char = self.pos_type[0]


class AnswerGrid():
    """
    Description
    -----------
    Class that acts as the first answer to the problem.
    it has a policy for each position on the grid represented
    by a letter n, s, e and w for each respective direction
    north, south, east and west.

    Parameters
    ----------
    states: StateSpace() \\
        -- All the states possible.

    policies: dict \\
        -- The policies to follow for each state.

    shape: list \\
        -- Shape of the list of list.

    initial_state: State() \\
        -- The initial state.

    goal_state: State() \\
        -- The goal state.

    Attributes
    ----------
    states: StateSpace() \\
        -- All the states possible.

    policies: dict \\
        -- The policies to follow for each state.

    initial_state: State() \\
        -- The initial state.

    goal_state: State() \\
        -- The goal state.

    shape: list \\
        -- Shape of the list of list.

    grid: list \\
        -- The answer grid as a list of lists.

    arrow_grid: str \\
        -- Same grid, but instead of letters, uses arrows as
        the representation of the policies.
    """

    def __init__(self, states, policies, shape, initial_state, goal_state):
        self.states = states
        self.policies = policies

        self.initial_state = initial_state
        self.goal_state = goal_state

        self.shape = shape

        self.grid = []
        self.arrow_grid = None

        self.init_grid()
        self.update_grid()

        self.highlight_special_states()

        self.create_arrow_grid()

    def __repr__(self):
        return 'AnswerGrid()'

    def __str__(self):
        grid_str = ''

        for row in self.grid:
            for item in row:
                grid_str = grid_str + str(item) + ' '

            grid_str = grid_str + '\n'

        return f'Shape: {self.shape}\n\n{grid_str}'

    def init_grid(self):
        """
        Description
        -----------
        Starts the grid in the shape specified filled with empty squares.
        """

        for i in range(0, self.shape[0]):
            aux_row = []

            for j in range(0, self.shape[1]):
                aux_row.append('□')

            self.grid.append(aux_row)

    def update_grid(self):
        """
        Description
        -----------
        Updates the grid by taking the first letter of the policy
        for each state and placing it on its coordinate.
        """

        for name in self.policies:
            state = self.states.get_state(name)

            self.grid[state.y][state.x] = self.policies[name][0]

    def highlight_special_states(self):
        """
        Description
        -----------
        Highlights the initial and goal states' policies, by converting the
        initial state to uppercase and exchanging the goal state with G.
        """

        self.grid[self.initial_state.y][self.initial_state.x] = str.upper(
            self.grid[self.initial_state.y][self.initial_state.x]
        )
        self.grid[self.goal_state.y][self.goal_state.x] = 'G'

    def create_arrow_grid(self):
        """
        Description
        -----------
        Instantiates and ArrowGrid() object and updates
        the `arrow_grid` attribute.
        """

        self.arrow_grid = ArrowGrid(self.grid, self.shape)


class ArrowGrid():
    """
    Description
    -----------
    Class that acts as the first answer to the problem.
    it has a policy for each position on the grid represented
    by a letter n, s, e and w for each respective direction
    north, south, east and west.

    Parameters
    ----------
    grid: list \\
        -- List of lists representing an AnswerGrid().

    shape: list \\
        -- Shape of the list of lists.

    Attributes
    ----------
    grid: list \\
        -- List of lists containing the arrows as policies.

    shape: list \\
        -- Shape of the list of lists.
    """

    def __init__(self, grid, shape):
        self.grid = self.convert_grid_to_arrow_grid(grid)
        self.shape = shape

    def __repr__(self):
        return 'ArrowGrid()'

    def __str__(self):
        grid_str = ''

        for row in self.grid:
            for item in row:
                grid_str = grid_str + str(item) + ' '

            grid_str = grid_str + '\n'

        return f'Shape: {self.shape}\n\n{grid_str}'

    def convert_grid_to_arrow_grid(self, grid):
        """
        Description
        -----------
        Converts an representation of an AnswerGrid() into a
        representation of an ArrowGrid().

        Replaces the letter for the direction into and arrow ponting
        to that direction. Except from the initial state, which is
        replaced by an tringle ponting to that direction, so that it
        is highlighted in the grid.

        Parameters
        -----------
        grid: list \\
            -- List of lists representing an AnswerGrid().

        Returns
        -------
        arrow_grid: list \\
            -- List of lists representing an ArrowGrid().
        """

        arrow_grid = []

        for row in grid:
            aux_row = []

            for item in row:
                if item == 'n':
                    aux_row.append('↑')
                elif item == 's':
                    aux_row.append('↓')
                elif item == 'e':
                    aux_row.append('→')
                elif item == 'w':
                    aux_row.append('←')
                elif item == 'N':
                    aux_row.append('▲')
                elif item == 'S':
                    aux_row.append('▼')
                elif item == 'E':
                    aux_row.append('▶')
                elif item == 'W':
                    aux_row.append('◀')
                else:
                    aux_row.append(item)

            arrow_grid.append(aux_row)

        return arrow_grid
