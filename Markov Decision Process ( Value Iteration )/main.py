import os
import json
from tests import LoadTests
from value_iteration import ValueIteration


def execute_value_iteration_test(test, epsilon, output='console'):
    """
    Description
    -----------
    Function used to run the algorithm for
    the given test, it also handles the standard
    output.

    Parameters
    ----------
    test: Test() \\
        -- A Test() instance with the information
        needed to run the algorithm.

    epsilon: float \\
        -- A floating point number, used to set
        the algorithm's stopping decision.

    output: str \\
        -- A string that tells the function where
        its output is expected.

    Returns
    -------
    ValueIteration() \\
        -- If no recognizable outputs is informed,
        returns the instance of the algorithm used.
    """

    value_iteration = ValueIteration(test, epsilon=epsilon)

    value_iteration.run()

    if output == 'file':
        folder = os.path.join(os.path.dirname(__file__), 'outputs')
        folder = os.path.join(folder, test.folder_name)

        file_name = test.file_name + '_value_iteration.txt'

        output_file = open(
            f'{os.path.join(folder, file_name)}', 'a+', encoding='utf-8'
        )

        # Truncating files, so that it doesn't append on existing content
        output_file.truncate(0)

        output_file.write(str(value_iteration))

        output_file.close()

    elif output == 'console':
        print(value_iteration)

    else:
        return value_iteration


tests = LoadTests()

fixed_goal = tests.fixed_goal_tests
random_goal = tests.random_goal_tests

del tests

epsilon = 0.1

# file or console
output = 'file'

for test in fixed_goal:
    execute_value_iteration_test(test, epsilon, output=output)

for test in random_goal:
    execute_value_iteration_test(test, epsilon, output=output)
