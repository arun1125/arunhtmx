from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import markdown2
from nbconvert import HTMLExporter

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
    notebook_folder = './notebooks'
    notebook_files = [f for f in os.listdir(notebook_folder) if f.endswith('.ipynb')]

    # Render the HTML template with the notebook files
    return templates.TemplateResponse("index.html", {"request": request, "notebook_files": notebook_files})

@app.get("/writings", response_class=HTMLResponse)
async def writings(request: Request):
    notebook_folder = './notebooks'
    notebook_files = [f for f in os.listdir(notebook_folder) if f.endswith('.ipynb')]

    # Render the HTML template with the notebook files
    return templates.TemplateResponse("writings.html", {"request": request, "notebook_files": notebook_files})

@app.get("/readings", response_class=HTMLResponse)
async def readings(request: Request):
    with open('readinglist.txt', 'r') as f:
        links = [line.strip() for line in f.readlines()]
    return templates.TemplateResponse('readings.html', {'request': request, 'links': links})



@app.get("/notebook/{notebook_file}", response_class=HTMLResponse)
async def load_notebook(request: Request, notebook_file: str):
    print(notebook_file)
    content = notebook_to_html(f'./notebooks/{notebook_file}')
    return templates.TemplateResponse("load_notebook.html", {"request": request, "content": content})