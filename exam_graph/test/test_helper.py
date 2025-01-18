import unittest
import os 
import sys
print("Current Working Directory:", os.getcwd())
from pathlib import Path
# sys.path.append(str(Path(__file__).resolve().parent.parent))
print("Python Path:", sys.path)
# print(os.environ)
# import helper
from exam_graph import helper

# run tests with 'python -m unittest discover'     
class TestHelp(unittest.TestCase):

    def test_pickle_copy(self):

        pickle_fp = Path('/home/data.pickle')
        new_pickle_fp = helper.pickle_copy(pickle_fp)
        expected_fp = Path('/home/data(1).pickle')

        self.assertNotEqual(pickle_fp, new_pickle_fp)
        self.assertEqual(new_pickle_fp, expected_fp)


if __name__ == '__main__':
    unittest.main()