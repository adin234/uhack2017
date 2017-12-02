import os
import unittest
from colour_runner import runner
from app import init_app

app = init_app()
app.config['TESTING'] = True

def main_test():
    cwd = os.path.dirname(os.path.realpath(__file__))

    folder_exclusions = ['__pycache__']

    loader = unittest.TestLoader()

    test_suites = []

    for item in os.listdir(cwd):
        if os.path.isdir(os.path.join(cwd, item)) and item not in folder_exclusions:
            md = __import__('tests.{}.tests'.format(item), fromlist=['UnitTest', 'APITest'])

            # Test cases for unit testing
            # Adds it to the test suite if existing
            if hasattr(md, 'UnitTest'):
                cl = getattr(md, 'UnitTest')
                test_suites.append(loader.loadTestsFromTestCase(cl))

            # Test cases for API Testing
            # Adds it to the test suite if existing
            if hasattr(md, 'APITest'):
                cl = getattr(md, 'APITest')
                test_suites.append(loader.loadTestsFromTestCase(cl))

    all_suite = unittest.TestSuite(test_suites)

    # Use colour_runner instead of the normal
    # unittest for the amazing colors :)
    test_runner = runner.ColourTextTestRunner(verbosity=2)
    result = test_runner.run(all_suite)


if __name__ == '__main__':
    main_test()
