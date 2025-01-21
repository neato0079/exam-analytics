from pathlib import Path
from exam_graph import helper
from datetime import datetime
from . import mock_data_gen
import json
import shutil
# Run with 'pytest', 'coverage report', and 'coverage html'

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


# def mock_config_fp(tmp_path_factory):
#     pass
#     # fp = 



# def test_build_usr():
#     pass




def test_build_usr_config(tmp_path):

    # set dir and fp
    dir:Path = tmp_path / 'prop'
    pickle_fn = 'test.pickle'
    fp = dir / 'test_config.json'

    # set content in test json
    expected_content = {
        'user datasets' : [pickle_fn]
    }

    # test in absense of config fp
    helper.build_usr_config('test.pickle', fp)

    # read into fp and check content against expected content
    with open(fp, 'r') as json_file:
        actual_content = json.load(json_file)
    assert actual_content == expected_content, f"Expected {expected_content}, but got {actual_content}"


    # test in absense of fp
    shutil.rmtree(dir)
    dir.mkdir(parents=True, exist_ok=True)
    helper.build_usr_config('test.pickle', fp)

    # read into fp and check content against expected content
    with open(fp, 'r') as json_file:
        actual_content = json.load(json_file)
    assert actual_content == expected_content, f"Expected {expected_content}, but got {actual_content}"


    # test where fp is presesnt. json should be updated rather than created
    shutil.rmtree(dir) # reset path
    print(f'After shutil.rmtree is called, dir is now:{dir.exists()}')
    dir.mkdir(parents=True, exist_ok=True) # create path


    # write file again
    with fp.open("w") as f:
        json.dump(expected_content, f, indent=4) 

    helper.build_usr_config('test(1).pickle', fp)

    # set new content in test json
    expected_new_content = {
        'user datasets' : [pickle_fn, 'test(1).pickle']
    }

    # read json and check for match
    with open(fp, 'r') as json_file:
        actual_content = json.load(json_file)
    assert actual_content == expected_new_content, f"Expected {expected_new_content}, but got {actual_content}"
    # dir.mkdir()
    # fp.write_text(CONTENT, encoding="utf-8")
    # assert fp.read_text(encoding="utf-8") == CONTENT
    # assert len(list(tmp_path.iterdir())) == 1
    # shutil.rmtree(dir)
