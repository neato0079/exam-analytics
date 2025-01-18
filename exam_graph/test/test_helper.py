# import unittest
# import os 
# import sys
# print("Current Working Directory:", os.getcwd())
from pathlib import Path
# # sys.path.append(str(Path(__file__).resolve().parent.parent))
# print("Python Path:", sys.path)
# # print(os.environ)
# # import helper
from exam_graph import helper

# # run tests with 'python -m unittest discover'     
# class TestHelp(unittest.TestCase):

#     def test_pickle_copy(self):

#         pickle_fp = Path('/home/data.pickle')
#         new_pickle_fp = helper.pickle_copy(pickle_fp)
#         expected_fp = Path('/home/data(1).pickle')

#         self.assertNotEqual(pickle_fp, new_pickle_fp)
#         self.assertEqual(new_pickle_fp, pickle_fp)


# if __name__ == '__main__':
#     unittest.main()

def test_pickle_copy():
        pickle_fp = Path('/home/data.pickle')
        new_pickle_fp = helper.pickle_copy(pickle_fp)
        pickle_copy_1 = Path('/home/data(1).pickle')
        pickle_copy_2 = Path('/home/data(2).pickle')

        print('pickle gets "(n)" appended')
        assert new_pickle_fp == pickle_copy_1

        print('"(n)" incrememnts by 1 if already present')
        assert helper.pickle_copy(pickle_copy_1) == pickle_copy_2


