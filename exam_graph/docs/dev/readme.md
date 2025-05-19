Notes
-----
path to this readme: `exam_graph/docs/dev/readme.md`

Run server with `python manage.py runserver`
- Make sure you are in the correct python environment otherwise `python manage.py runserver` won't work. You can check this by running the command `which python` in the terminal

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
- Client sends a request to the Django server running on a gunicorn web server
- Django sees the request URL
- On the Django server, this URL is mapped to a view
- The view is called and the server performs whatever logic is in that view
- The view then sends a response out to the client
- This response is usually a HTTP response that generates some HTML to be displayed on the client's browser

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