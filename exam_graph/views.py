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
from json2html import *
import json

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

    user = helper.get_user(request)

    return render(request, 'index.html', {'files': files, 'user': user})
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

            return redirect('/')

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

            return redirect('/')

        # set full config path user's new pickle
        pickle_fp = DATASET_DIR / pickle_fn

        # update user_config.json with name of newly uploaded dataset
        helper.build_usr_config(pickle_fp, USER_CONFIG_FP)

        # Store df as pickle on disk
        helper.save_pickle(df, pickle_fp)
        messages.info(request, f'{file_str} uploaded!')
        return redirect('/')
        
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

        # set summary tables:
        summary_tables = []
        
        if shift_view:

            # create shift view graph
            graph_base64 = myplot.plot_shift(axes_data, period)

            # compile summary data
            agg_df:pd.DataFrame = axes_data.aggregate(['mean', 'max', 'sum']).astype(int)           
            agg_df.columns.name = ''
            agg_df.rename(index={'mean':'Avg', 'sum': 'Total'}, inplace=True)
            agg_tb = agg_df.to_html()

            # add to summary tables for html render
            summary_tables.append(agg_tb)

        else:
            # graph without shift view
            graph_base64 = myplot.gen_encoded_graph(axes_data, period, metric, modality_lst)

            # init summary json
            summary_json = {}

            # create analysis series
            # desc = axes_data.describe().astype(int)
            # desc_str = desc.to_json()
            # desc_dict = json.loads(desc_str)
            # summary_json.update(desc_dict)
            agg_sr:pd.Series = axes_data.aggregate(['mean', 'max', 'sum']).astype(int)
            agg_sr.rename(index={'mean':'Avg', 'sum': 'Total'}, inplace=True)
            agg_str = agg_sr.to_json()
            agg_dict = json.loads(agg_str)

            # add data to summary_json
            summary_json.update(agg_dict)

            # convert to html table
            generic_summary = json2html.convert(json = summary_json)

            # add to summary tables for html render
            summary_tables.append(generic_summary)

        stuff_for_html_render = {
            'graph': graph_base64,
            'selected_period': period,
            'selected_modality': modality_lst,
            'selected_metric': metric,
            'start_date': datestr[0],
            'end_date': datestr[1],
            'shift_view': shift_view,
            'summary': summary_tables,
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


def login(request:HttpRequest):
    from django.contrib.auth import authenticate
    user = request.POST["username"]
    password = request.POST["password"]
    is_auth = authenticate(username=user, password=password)
    dic = {
        'user': user,
        'mess': 'mess'
    }
    if is_auth is not None:
        # A backend authenticated the credentials
        dic['mess'] = 'logged in!!!!'
        return render(request, 'login.html', dic)

    else:
    # No backend authenticated the credentials
        dic['mess'] = 'not logged in'
        return render(request, 'login.html', dic)


def login_page(request:HttpRequest):
    return render(request, 'login.html')

def app_login(request:HttpRequest):
    from django.contrib.auth import authenticate, login
    user = request.POST["username"]
    password = request.POST["password"]
    is_auth = authenticate(username=user, password=password)

    if is_auth is not None:
        # A backend authenticated the credentials
        login(request, is_auth)

        return JsonResponse({'Login success': f"user: {user}"}, status=200)

    else:
    # No backend authenticated the credentials

        return JsonResponse({'Login failed': f"user: {user}"}, status=200)




def logout(request:HttpRequest):
    from django.contrib.auth import logout
    print(request.user)
    user = request.user
    logout(request)
    dic = {
        'mess': f'{user} successfully logged out!'
    }
    return render(request, 'login.html', dic)


def wholog(request:HttpRequest):
    user = helper.get_user(request)


    return JsonResponse({'Current logged in user': f"user: {user}"}, status=200)