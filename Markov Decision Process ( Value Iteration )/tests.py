import os
from states import StateSpace
from grids import Grid


class LoadTests():
    """
    Description
    -----------
    Class used to load and store tests.
    When instantiated, it will call the function
    responsible for loading the tests.

    Attributes
    ----------
    fixed_goal_tests: TestSet() \\
        -- A TestSet() object, containing all of the FixedGoal
        tests for the GridWorld problem that will be solved.

    random_goal_tests: TestSet() \\
        -- A TestSet() object, containing all of the RandomGoal
        tests for the GridWorld problem that will be solved.

    current_file_folder: str \\
        -- A string containing the full path to the folder
        where this file is stored.
    """

    def __init__(self):
        self.fixed_goal_tests = TestSet()
        self.random_goal_tests = TestSet()

        self.current_file_folder = os.path.dirname(os.path.abspath(__file__))

        self.load_tests()

    def load_tests(self):
        """
        Description
        -----------
        Function used to add tests to both TestSet() instances of the class.
        """
        self.fixed_goal_tests.add_testset_list(self.read_tests('FixedGoal'))
        # self.random_goal_tests.add_testset_list(self.read_tests('RandomGoal'))

    def read_tests(self, test_type):
        """
        Description
        -----------
        Function used to open and read the test files.
        It instantiates Test() objects using the files
        as parameters and appends them to a list.

        Parameters
        ----------
        test_type: str \\
            -- A str that is used to get the type of the test,
            this information will be used to find the folder.

        Returns
        -------
        list \\
            -- A list of Test() objects.
        """

        tests_folder = os.path.join(
            self.current_file_folder, 'TestesGrid', f'{test_type}InitialState'
        )

        tests = []

        for test in sorted(os.listdir(tests_folder)):
            test_file = open(os.path.join(tests_folder, test), 'r+')

            tests.append(Test(test_file))

            break

        return tests


class TestSet():
    """
    Description
    -----------
    Class used to store tests.

    Attributes
    ----------
    tests: list \\
        -- A list containing all the tests loaded.
    """

    def __init__(self):
        self.tests = []

    def __iter__(self):
        return iter(self.tests)

    def add_testset_list(self, test_set_list):
        """
        Description
        -----------
        Function used to update the `tests` attribute.

        Parameters
        ----------
        test_set_list: list \\
            -- A list containing the Test() objects.
        """

        self.tests = test_set_list


class Test():
    """
    Description
    -----------
    Class that defines a Test.
    It is used as an input to the solver algorithms.

    Parameters
    ----------
    test_file: file \\
        -- The file conataining the test info.

    Attributes
    ----------
    file: file \\
        -- The file conataining the test info.

    file_name: str \\
        -- The name of the file.

    full_folder: str \\
        -- Full path to the file, except for the actual name of the file.

    folder_name: str \\
        -- Name of the folder where the test file is stored.

    current_line: str \\
        -- The current line that was read from the file.

    states: StateSpace() \\
        -- A StateSpace() instance that has the states read from the file.

    initial_state: State() \\
        -- The initial state read from the file.

    goal_state: State() \\
        -- The goal state read from the file.

    grid: Grid() \\
        -- A Grid() instance that stores the grid read form the file.
    """

    def __init__(self, test_file):
        self.file = test_file
        self.file_name = os.path.basename(self.file.name)
        self.full_folder = os.path.dirname(self.file.name)
        self.folder_name = os.path.basename(self.full_folder)
        self.current_line = None

        self.states = StateSpace()
        self.initial_state = None
        self.goal_state = None
        self.grid = Grid()

        self.load_attributes()

        self.update_coordinates()

    def __repr__(self):
        return f'Test({self.file_name})'

    def __str__(self):
        return f'''
File: {os.path.join(self.folder, self.file_name)}
Init: {self.initial_state}
Goal: {self.goal_state}
Grid: {self.grid}'''

    def read_file_line(self):
        """
        Description
        -----------
        Function used to update the `current_line` attribute.
        """

        self.current_line = self.file.readline().strip()

    def load_attributes(self):
        """
        Description
        -----------
        Function used to update most of the attributes.
        It follows the standard found on all of the test files.
        """

        while self.current_line != 'states':
            self.read_file_line()

        self.load_states()

        # Will run for all directions
        # North, South, East and West
        for i in range(0, 4):
            while not self.current_line.startswith('action'):
                self.read_file_line()

            # line should be 'action move-direction'
            move_direction = str.split(self.current_line)[1]

            self.load_actions(move_direction)

        while self.current_line != 'cost':
            self.read_file_line()

        self.load_costs()

        while self.current_line != 'initialstate':
            self.read_file_line()

        self.read_file_line()
        self.initial_state = self.states.get_state(self.current_line)

        while self.current_line != 'goalstate':
            self.read_file_line()

        self.read_file_line()
        self.goal_state = self.states.get_state(self.current_line)

        while self.current_line != 'Grid:':
            self.read_file_line()

        self.load_grid()

    def load_states(self):
        """
        Description
        -----------
        Function used to load all the states from the line containing them.
        It then stores them into a list and updates the `states` attribute.
        """

        self.read_file_line()

        states_list = self.current_line.split(', ')

        self.states.load_states_list(states_list)

    def load_actions(self, move_direction):
        """
        Description
        -----------
        Function used to load all the actions for a specific direction.
        It reads all of the lines using their pattern, discarding the last
        item, which won't be used, and getting the respective states and
        updating the action for the initial state.
        """

        self.read_file_line()

        while self.current_line != 'endaction':
            init_state, end_state, prob, discard = self.current_line.split()

            del discard

            init_state = self.states.get_state(init_state)

            end_state = self.states.get_state(end_state)

            init_state.update_action(move_direction, end_state, prob)

            self.read_file_line()

    def load_costs(self):
        """
        Description
        -----------
        Function used to load all the costs for all the actions and
        updating the actions with their respective cost.
        """

        self.read_file_line()

        while self.current_line != 'endcost':
            cost_list = self.current_line.split()

            state = self.states.get_state(cost_list[0])

            state.update_action_cost(cost_list[1], cost_list[2])

            self.read_file_line()

    def load_grid(self):
        """
        Description
        -----------
        Function used to load the grid from the file,
        updating the `grid` attribute.
        """

        self.read_file_line()

        while self.current_line != '':
            self.grid.add_row(self.current_line.split())

            self.read_file_line()

    def update_coordinates(self):
        """
        Description
        -----------
        Function used to update the `shape` attribute from
        the `grid` attribute and using that info to update
        the coordinates for each state.
        """

        self.grid.update_shape()

        self.states.update_coordinates(self.grid)
