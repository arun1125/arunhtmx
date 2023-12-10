from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
import markdown2
from nbconvert import HTMLExporter
import requests
import pandas as pd
from database.db import supabase


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

@app.get("/nba", response_class=HTMLResponse)
async def home(request: Request):
    team_data = {'Washington Wizards': 'WAS',
 'Utah Jazz': 'UTA',
 'Toronto Raptors': 'TOR',
 'San Antonio Spurs': 'SAS',
 'Sacramento Kings': 'SAC',
 'Portland Trail Blazers': 'POR',
 'Phoenix Suns': 'PHO',
 'Philadelphia 76ers': 'PHI',
 'Orlando Magic': 'ORL',
 'Oklahoma City Thunder': 'OKC',
 'New York Knicks': 'NYK',
 'New Orleans Pelicans': 'NOH',
 'Minnesota Timberwolves': 'MIN',
 'Milwaukee Bucks': 'MIL',
 'Miami Heat': 'MIA',
 'Memphis Grizzlies': 'MEM',
 'Los Angeles Lakers': 'LAL',
 'Los Angeles Clippers': 'LAC',
 'Indiana Pacers': 'IND',
 'Houston Rockets': 'HOU',
 'Golden State Warriors': 'GSW',
 'Detroit Pistons': 'DET',
 'Denver Nuggets': 'DEN',
 'Dallas Mavericks': 'DAL',
 'Cleveland Cavaliers': 'CLE',
 'Chicago Bulls': 'CHI',
 'Charlotte Hornets': 'CHA',
 'Brooklyn Nets': 'BRK',
 'Boston Celtics': 'BOS',
 'Atlanta Hawks': 'ATL'}
    
    html_options = ''
    for name, abbrev in team_data.items():
        html_options += f'<option value="{abbrev}">{name}</option>\n'

    return templates.TemplateResponse("nba_home.html", {"request": request, "html_options": html_options})

@app.get("/nba/team", response_class=HTMLResponse)
async def home(request: Request, team: str = Query(...), year: int = Query(...)):
    resp = requests.get(f'https://www.basketball-reference.com/teams/{team}/{year}.html')
    dfs = pd.read_html(resp.text)
    content = dfs[1].to_html()
    return f'<div id="team_table" style="font-family: monospace">{content}</div>'


@app.get("/auth", response_class=HTMLResponse)
async def auth(request: Request):
    return templates.TemplateResponse(
        "auth.html", {"request": request, "title": "Please Sign In or Sign Up"}
    )