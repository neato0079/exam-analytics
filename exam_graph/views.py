# aka API handler i guess??
# the urls.py from this same directory "handles" the client's url requests by calling functions from this file

from dotenv import load_dotenv
load_dotenv()

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpRequest, HttpResponseNotFound
from django.conf import settings
import pandas as pd
from . import helper
from . import filters
import traceback
from . import myplot
from pathlib import Path
import pickle
from django.contrib import messages
from json2html import *
import json
from exam_graph.utils.data_filter import FilterRequest
from exam_graph.utils.summary import DataSummary
from exam_graph.utils.exam_data_set import ExamDataFrame
from exam_graph.utils.global_paths import *
import os
import markdown2

# Create your views here.
def documentation(request: HttpRequest, doc_path: str):
    # Construct the full path safely
    md_path = Path(settings.BASE_DIR) / 'exam_graph' /'docs' / doc_path
    # md_path = "/Users/mattbot/dev/exam-analytics/exam_graph/docs/dev/readme.md"
    # md_path = "/Users/mattbot/dev/exam-analytics/docs/dev/readme.md"

    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            markdown_text = f.read()
    except FileNotFoundError:
        return HttpResponseNotFound(f'Documentation file at {md_path} not found.')

    html = markdown2.markdown(markdown_text, extras=["fenced-code-blocks", "tables"])

    return render(request, 'documentation.html', {
        'doc_name': os.path.basename(md_path),
        'html_content': html
    })

def home(request:HttpRequest):

    if DATASET_DIR.exists():
        files = [f.stem for f in DATASET_DIR.iterdir() if f.is_file()]  # List only files without suffix

    else:
        files = ['no datasets uploaded']

    user = helper.get_user(request)

    return render(request, 'index.html', {'files': files, 'user': user})
    # return HttpResponse('<h1>asdfasdfasdfasdf</h1>')

def form_page(request:HttpRequest):
    return render(request, 'form.html', {'graph': 'graph_file_path'})

def help(request:HttpRequest):
    return render(request, 'help.html')

def test(request:HttpRequest):
    file_name = request.GET['file'] + '.pickle'
    return JsonResponse({'Your Selection': f"File: {file_name}"}, status=200)

# upload csv file to server disk as pickle
def upload_csv(request:HttpRequest):

    # convert upload file to df
    try:
        # get user uploaded file form http request
        files = request.FILES.keys()

        # ingest file into class
        # check if its a cvs file
        try:
            exam_data_master = ExamDataFrame(upload_req=request.FILES)
            df = exam_data_master.df

        except Exception as e:
            messages.error(request, 'Upload ".csv" files only please! I am still just a baby app!')
            stack_trace = traceback.format_exc()  # Capture the full traceback
            print(stack_trace)  # Log the detailed error in the console
            return redirect('/')

        # TODO:
        # Check if the data is formatted correctly
        # try:
        #   exam_data_master.format_self
        #   df = exam_data_master.df

        # Check if the df is formatted correctly
        try:
            # Format data for filters
            df = helper.format_df(df)
        except Exception as e:
            error_message = f'Unable to format data: {e}'
            stack_trace = traceback.format_exc()  # Capture the full traceback
            print(stack_trace)  
            messages.error(request, "Cannot parse file. Check the help page to make sure your .csv file is in the correct format.")

            return redirect('/')

    # save pickle
        # set full config path user's new pickle
        pickle_fp = DATASET_DIR / exam_data_master.pickle_fn

        # update user_config.json with name of newly uploaded dataset
        helper.build_usr_config(pickle_fp, USER_CONFIG_FP)

        # Store df as pickle on disk
        helper.save_pickle(df, pickle_fp)
        messages.info(request, f'{exam_data_master.file_str} uploaded!')
        return redirect('/')
        
    except Exception as e:
        error_message = f"An error occurred! Try checking the help section! Here is your error!: {e}"
        stack_trace = traceback.format_exc()  # Capture the full traceback
        print(stack_trace)  # Log the detailed error in the console
        return HttpResponse(f"{error_message}<br><pre>{stack_trace}</pre>", content_type="text/html")


def filter_submission_handler(request:HttpRequest):

    # get requested pickel server fp and convert it to a df
    pickle_fp:Path = helper.selected_pickle_fp(USER_CONFIG_FP, DATASET_DIR)
    df = helper.pickle_to_df(pickle_fp)
    print('Filtered from source:')
    print(pickle_fp)
    
    if request.method == 'POST':
        try:

            # set our post request to an instance of FilterRequest for parsing
            filtr:FilterRequest = FilterRequest(request.POST)  

            if filtr.shift_view:
                # TYPE HINT axes_data:pd.DataFrame | pd.Series
                ratio_data, axes_data = filters.master_filter(df, filtr)
                if axes_data.empty:
                    messages.error(request, 'No data was found with those filters!')
                    stack_trace = traceback.format_exc()  # Capture the full traceback
                    print(stack_trace)  # Log the detailed error in the console
                    return redirect('formyayay')

                # create shift view graph
                graph_base64 = [myplot.plot_shift(axes_data,filtr.period)]

                # create ratio graph only on total metric
                if filtr.metric == 'totals':
                    graph_base64.append(myplot.plot_ratios(ratio_data))

                # compile summary data
                summary = DataSummary(axes_data)

                # add to summary tables for html render
                summary_tables = [summary.build_table()]

            else:
                axes_data:pd.Series = filters.master_filter(df, filtr)
                if axes_data.empty:
                    messages.error(request, 'No data was found with those filters!')
                    stack_trace = traceback.format_exc()  # Capture the full traceback
                    print(stack_trace)  # Log the detailed error in the console
                    return redirect('formyayay')
                    
                # graph without shift view
                graph_base64 = [myplot.gen_encoded_graph(axes_data, filtr.period, filtr.metric, filtr.modalities)]

                # build summary
                summary = DataSummary(axes_data)

                # convert to html table and add to summary tables for html render
                summary_tables = [(summary.build_table())]

            stuff_for_html_render = {
                'graphs': graph_base64,
                'selected_period': filtr.period,
                'selected_modality': filtr.modalities,
                'selected_metric': filtr.metric,
                'start_date': filtr.date_range_string[0],
                'end_date': filtr.date_range_string[1],
                'shift_view': filtr.shift_view,
                'summary': summary_tables,
                'dataset_name': pickle_fp.stem
            }
    
            return render(request, 'form.html', stuff_for_html_render)

        except Exception as e:
            error_message = f"An error occurred: {e}"
            stack_trace = traceback.format_exc()  # Capture the full traceback
            print(stack_trace)  # Log the detailed error in the console
            return HttpResponse(f"{error_message}<br><pre>{stack_trace}</pre>", content_type="text/html")
    else:
        return HttpResponse(f'That requires a post request. You sent a {request.method} request!')



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