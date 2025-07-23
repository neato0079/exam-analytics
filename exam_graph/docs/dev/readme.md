Notes
-----
path to this readme: `exam_graph/docs/dev/readme.md`

Run server with `python manage.py runserver`
- Make sure you are in the correct python environment otherwise `python manage.py runserver` won't work. You can check this by running the command `which python` in the terminal. If you're in the wrong environemt input `deactivate` into the terminal. Then to `source env/bin/activate`

The html template syntax `{{ django_var|safe }}` is an "injection into the djagno server generated html. In this case `safe` tells python to interpret any `html` syntax as such rather than interpreting them as string representations. So if `django_var` = `<h1>Some Heading</h1>` on the serverside, once the `HTML` is generated, the webpage will just display `Some Heading` without the `h1` tags being visible to the user. The `h1` tags would actually just be `HTML` tags. This is because of the `safe` keyword in the template. Without that keyword, the `h1` tags would be displayed on the webpage as strings.

# App Features:
- User can upload exam data files (only `.csv` files for now)
- Dataset saved as `.pickle` on app server file system
- User can select different uploaded datasets to perform analyses on
- Uses Pandas to analyze data
- Uses Matplotlib to plot data
- User can login (no functionality yet though)

# App Enviroment:
- Django server
- Hosted on `Render`
- Serves client requests on `gunicorn` webserver
- CI/CD via `GitHub Actions`

# TODO:
- Refactor to OOP
    - Try to make things more modular to make future refactors easier
- Move to AWS

# How Django Runs the App
- Client sends a request to the `Django` server running on a gunicorn web server
- `Django` sees the request URL
- On the `Django` server, this URL is mapped to a `view`
- The view is called and the server performs whatever logic is in that `view`
- The `view` then sends a response out to the client
- This response is usually a HTTP response that generates some HTML to be displayed on the client's browser

Upload Functionality
--------------------
User uploads local dataßset via client POST request > Django server processes the data with the following actions:
- formats data
    - data is converted to a pandas `df`
    - apply format checks to `df`

- adds dataset name to user profile via `helper.build_usr_config()`
- saves as pickle onto disk

FE:
On the homepage, a file path is entered into an `HTML` form. This form's action is set to send a `POST` request to the `upload/` view with the user's selected file in the body of the request.

BE:
URL path: path('upload/', views.upload_csv, name='mock'),
view functions: upload_csv()

Data Filter Functionality
------------------------- 

### Setting Chosen Dataset:
On the homepage, when the user clicks on "Load Data", a `GET` request is sent to the url `load_data/` which is  called from the the urls module at `exam_graph/urls.py`. This `GET` request contains a file string of the file for the chosen dataset. This url calls the `load_data()` function in the views module `exam_graph/views.py`. 

`load_data()` builds a filepath from the file string from the `GET` request. This filepath points to the location of the dataset in `pickle` format stored on the app server. Then the userconfig is updated to set the selected dataset. This userconfig is a `JSON` file on the app server. Here is an example of a userconfig:

```
{
    "user datasets": [
        "big_mock_one_day",
        "mock_exam_data_v3",
        "mock_exam_data_v3(1)"
    ],
    "selected_dataset": "mock_exam_data_v3(1).pickle"
}
```
Finally, `load_data()` will render `form.html`

### Applying User Selected Filters to Dataset

At the `form.html` page, the user can fill out an `html` form that sends a `POST` request to the `result/` url which calls the view `filter_submission_handler()`. Example of the body of this `POST` request:

```
csrfmiddlewaretoken=1234asdf

start_date=2024-07-10&

end_date=2024-09-14&User_selected_metric=totals&

User_selected_modality=XR&period=week&shift_view=True
```

TESTS
-----
code snippett:
```
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

    html = markdown2.markdown(markdown_text, extras={"fenced-code-blocks":None, "tables":None,"highlightjs-lang": "python"})

    return render(request, 'documentation.html', {
        'doc_name': os.path.basename(md_path),
        'html_content': html
    })
```