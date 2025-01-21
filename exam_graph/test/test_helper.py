from pathlib import Path
from exam_graph import helper
from datetime import datetime

def test_pickle_copy():
    pickle_fp = Path('/home/data.pickle')
    new_pickle_fp = helper.pickle_copy(pickle_fp)
    pickle_copy_1 = Path('/home/data(1).pickle')
    pickle_copy_2 = Path('/home/data(2).pickle')

    print('pickle gets "(n)" appended')
    assert new_pickle_fp == pickle_copy_1

    print('"(n)" incrememnts by 1 if already present')
    assert helper.pickle_copy(pickle_copy_1) == pickle_copy_2


def test_get_shift():

    # set time to test
    am_sample = datetime.strptime('0930', '%H%M')
    pm_sample = datetime.strptime('1645', '%H%M')
    nc_sample = datetime.strptime('2345', '%H%M')
    nc_sample2 = datetime.strptime('0200', '%H%M')

    assert helper.get_shift(am_sample) == 'AM'
    assert helper.get_shift(pm_sample) == 'PM'
    assert helper.get_shift(nc_sample) == 'NOC'
    assert helper.get_shift(nc_sample2) == 'NOC'


def mock_config_fp(tmp_path_factory):
    pass
    # fp = 



def test_build_usr():
    pass