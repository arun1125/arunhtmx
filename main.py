from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import markdown2
from nbconvert import HTMLExporter
import os


def notebook_to_html(path):
    exporter = HTMLExporter()
    exporter.exclude_input = False  # You can change this depending on whether you want to include the input cells

    with open(path, 'r', encoding='utf-8') as notebook:
        body, _ = exporter.from_file(notebook)
    return body

def read_markdown_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        return markdown2.markdown(file.read())

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/writing", response_class=HTMLResponse)
async def writings(request: Request):
    folder = './writings'

    categories = []
    for _, subdirList, _ in os.walk(folder):
        for subdir in subdirList:
            categories.append(subdir)

    return templates.TemplateResponse("categories.html", {"request": request, "categories": categories, "category": "writing"})

@app.get("/writing/{category}", response_class=HTMLResponse)
async def load_notebook(request: Request, category: str):
    notebook_folder = f'./writings/{category}'
    notebook_files = [f for f in os.listdir(notebook_folder) if f.endswith('.ipynb')]

    return templates.TemplateResponse("notebooks.html", {"request": request, "category":category, "notebook_files": notebook_files})


@app.get("/writing/{category}/{notebook_file}", response_class=HTMLResponse)
async def load_notebook(request: Request, category:str, notebook_file: str):
    content = notebook_to_html(f'./writings/{category}/{notebook_file}')
    notebook_folder = f'./writings/{category}'
    notebook_files = [f for f in os.listdir(notebook_folder) if f.endswith('.ipynb')]
    # Render the HTML template with the notebook files
    return templates.TemplateResponse("load_notebook.html", {"request": request, "content": content, "notebook_file": notebook_files})

@app.get("/readinglist", response_class=HTMLResponse)
async def readinglist(request: Request):
    folder = './readings'

    categories = []
    for _, subdirList, _ in os.walk(folder):
        for subdir in subdirList:
            categories.append(subdir)

    return templates.TemplateResponse("categories.html", {"request": request, "categories": categories, "category": "readinglist"})

@app.get("/readinglist/{category}", response_class=HTMLResponse)
async def load_notebook(request: Request, category: str):

    with open(f'./readings/{category}/readinglist.txt', 'r') as f:
        links = [line.strip() for line in f.readlines()]

    return templates.TemplateResponse('readinglist.html', {'request': request, 'links': links})