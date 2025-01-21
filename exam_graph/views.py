# aka API handler i guess??
# the urls.py from this same directory "handles" the client's url requests by calling functions from this file

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpRequest
import pandas as pd
from . import helper
from . import filters
import traceback
from . import myplot
from pathlib import Path
import pickle
from django.contrib import messages
from decouple import config


# Paths
CONFIG_ROOT = Path(config('CONFIG_ROOT'))
USER_PROP = Path(config('USER_PROP'))
DATASETS = Path(config('DATASETS'))
USER_CONFIG_FN = Path(config('USER_CONFIG_FP'))
USER_PROP_DIR = CONFIG_ROOT / USER_PROP
DATASET_DIR = CONFIG_ROOT / USER_PROP / DATASETS
USER_CONFIG_FP = USER_PROP_DIR / USER_CONFIG_FN

# Create your views here.
def home(request:HttpRequest):

    if DATASET_DIR.exists():
        files = [f.stem for f in DATASET_DIR.iterdir() if f.is_file()]  # List only files without suffix

    else:
        files = ['no datasets uploaded']
    return render(request, 'index.html', {'files': files})
    # return HttpResponse('<h1>asdfasdfasdfasdf</h1>')

def form_page(request):
    return render(request, 'form.html', {'graph': 'graph_file_path'})

def help(request):
    return render(request, 'help.html')

def display_mock_csv(request):
    df = helper.build_test_master_json_df()
    graph = df.to_html()
    return render(request, 'test_template.html', {'graph': graph})

def test(request):
    file_name = request.GET['file'] + '.pickle'
    return JsonResponse({'Your Selection': f"File: {file_name}"}, status=200)

# upload csv file to server disk as pickle
def upload_csv(request):

    try:
        # get user uploaded file form http request
        files = request.FILES.keys()
        file = next(iter(files))

        # check if its a cvs file
        file_prefx = str(request.FILES[file]).split('.')[-1]
        print(f'requested file upload type: .{file_prefx}')
        if file_prefx != 'csv':
            print('not a csv')
            messages.error(request, 'Upload ".csv" files only please! I am still just a baby app!')

            return redirect('/exam_graph')

        file_str = str(request.FILES[file]).split('.')[0]
        pickle_fn = file_str + ".pickle"
        csv_file = request.FILES[file]

        # Read CSV into a DataFrame
        df = pd.read_csv(csv_file)

        # Check if the data is formatted correctly
        try:
            # Format data for filters
            df = helper.format_df(df)
        except Exception as e:
            error_message = f'Unable to format data: {e}'
            stack_trace = traceback.format_exc()  # Capture the full traceback
            print(stack_trace)  # Log the detailed error in the console
            messages.error(request, "Cannot parse file. Check the help page to make sure your .csv file is in the correct format.")

            return redirect('/exam_graph')

        # set full config path user's new pickle
        pickle_fp = DATASET_DIR / pickle_fn

        # update user_config.json with name of newly uploaded dataset
        helper.build_usr_config(pickle_fp, USER_CONFIG_FP)

        # Store df as pickle on disk
        helper.save_pickle(df, pickle_fp)
        messages.info(request, f'{file_str} uploaded!')
        return redirect('/exam_graph')
        
    except Exception as e:
        error_message = f"An error occurred! Try checking the help section! Here is your error!: {e}"
        stack_trace = traceback.format_exc()  # Capture the full traceback
        print(stack_trace)  # Log the detailed error in the console
        return HttpResponse(f"{error_message}<br><pre>{stack_trace}</pre>", content_type="text/html")


def filter_submission_handler(request):

    # parsed_mocked_data = helper.build_test_master_json_df()
    pickle_fp:Path = helper.selected_pickle_fp(USER_CONFIG_FP, DATASET_DIR)
    df = helper.pickle_to_df(pickle_fp)
    print('Filtered from source:')
    print(pickle_fp)
    

    try:

        # parse filter request
        filter_params: dict = helper.parse_filter_request(request) # returns a dictionary containing the necessary arguments for master_filter()

        # df = filter_params['source_dataframe']
        period = filter_params['xfilt']['period']
        modality_lst = filter_params['xfilt']['modalities']
        metric = filter_params['User_selected_metric']
        daterange = filter_params['date_range']
        datestr = filter_params['date_str']
        shift_view = filter_params['shift_view']

        # TESTING SHIFT PLOT. TOTALS ONLY

        axes_data = filters.master_filter(df, filter_params['xfilt'], metric ,daterange, filter_params)
        
        if shift_view:
            graph_base64 = myplot.plot_shift(axes_data, period)
            axes_data = helper.shift_totals(axes_data)
            axes_data = axes_data.to_html()

        else:
            # graph without shift view
            graph_base64 = myplot.gen_encoded_graph(axes_data, period, metric, modality_lst)
            axes_data = axes_data.to_frame().to_html()# convert to df for html view

        stuff_for_html_render = {
            'graph': graph_base64,
            'selected_period': period,
            'selected_modality': modality_lst,
            'selected_metric': metric,
            'start_date': datestr[0],
            'end_date': datestr[1],
            'shift_view': shift_view,
            'summary': axes_data,
            'dataset_name': pickle_fp.stem
        }
  
        return render(request, 'form.html', stuff_for_html_render)


    except Exception as e:
            error_message = f"An error occurred: {e}"
            stack_trace = traceback.format_exc()  # Capture the full traceback
            print(stack_trace)  # Log the detailed error in the console
            return HttpResponse(f"{error_message}<br><pre>{stack_trace}</pre>", content_type="text/html")


def load_data(request:HttpRequest):

    # get file name from form
    file_str = request.GET.get('file')

    # set file name in user config
    pickle_fn = file_str + ".pickle"
    if USER_CONFIG_FP.exists():
        helper.set_selected_dataset(pickle_fn, USER_CONFIG_FP)

    pickle_fp = Path(str(DATASET_DIR) + '/' + pickle_fn)

    # read df to provide form.html with base info about the dataset like daterange
    df = helper.pickle_to_df(pickle_fp)
    earliest, latest = helper.check_date_range(df)

    stuff_for_html_render = {
        'start_date': earliest,
        'end_date': latest,
        'dataset_name': pickle_fp.stem
    }
    return render(request, 'form.html', stuff_for_html_render)