import pandas as pd
from exam_graph.utils.exam_data_set import ExamDataFrame
from exam_graph.utils.global_paths import *

def test_ExamDataFrame_empty():
    """
    ExamDataFrame.df shoud have an empty df if nothing is passed on initialization 
    """
    csv = EXAM_GRAPH_ROOT / 'test' / 'mock_exam_data_v3.csv'
    df = ExamDataFrame()
    df = df.df

    assert df.empty 

    full_df = ExamDataFrame(file=csv)
    full_df = full_df.df

    print('Passing a data filled file into ExamDataFrame should not result in an empty df')
    assert not full_df.empty


def test_columns():
    """
    Any created df attribute should have the default columns unless otherwise specified by the hl7_fields optional arg.
    """

    df = ExamDataFrame()
    df = df.df

    default_col = [
        'Exam Complete Date/Tm', 
        'Order Procedure Accession',
        'Exam Order Date/Time', 
        'Final Date/Tm', 
        'Exam Order Name', 
        'Modality']

    assert list(df.columns) == default_col 

def test_read_file():
    """
    ExamDataFrame should be able to read a file and set it to the df attribute on initialization
    """
    csv = EXAM_GRAPH_ROOT / 'test' / 'mock_exam_data_v3.csv'
    exam_data = ExamDataFrame(file=csv)
    assert not exam_data.df.empty
    assert exam_data.df.name == 'mock_exam_data_v3'
    assert pd.read_csv(csv).equals(exam_data.df) 

if __name__ == "__main__":
    exam_data = ExamDataFrame()

    print(exam_data.df.columns)