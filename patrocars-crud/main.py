from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import asyncpg
import asyncio

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory='templates')

bd = None

@app.on_event("startup")
async def startup():
    global bd
    bd = await asyncpg.connect(
        user='postgres',
        password='1234',
        database='patrocars',
        host='localhost'
    )

@app.get('/listar', response_class=HTMLResponse)
async def list_montadoras(request: Request):
  montadoras = await bd.fetch('SELECT * FROM MONTADORA')

  return templates.TemplateResponse(
    request, 'list_montadoras.html', context={'montadoras': montadoras}
  )

@app.get('/adicionar')
async def adicionar_montadora(request: Request):
  return templates.TemplateResponse(
    request, 'add_montadora.html'
  )

@app.post('/salvar')
async def adicionar_montadora(nome: str = Form(...), pais: str = Form(...), ano_fundacao: int = Form(...)):
  insercao = 'INSERT INTO MONTADORA (NOME, PAIS, ANO_FUNDACAO) VALUES ($1, $2, $3)'
  await bd.execute(insercao, nome, pais, ano_fundacao)

@app.get('/editar/{montadora_id}')
async def editar_form(request: Request, montadora_id: str):
    montadora_a_editar = None
    montadoras = await bd.fetch('SELECT * FROM MONTADORA')

    for montadora in montadoras: 
        if montadora['mont_id'] == int(montadora_id):
            montadora_a_editar = montadora

    if montadora_a_editar is None:
        return templates.TemplateResponse(
            request, '404.html'
        )
    
    return templates.TemplateResponse(
        request, 'editar_montadora.html', context={'montadora': montadora_a_editar}
    )

@app.post('/editar_salvar/{montadora_id}')
async def editar_montadora(montadora_id: int, nome: str = Form(...), pais: str = Form(...), ano_fundacao: int = Form(...)):
  atualizacao = 'UPDATE MONTADORA SET NOME = $1, PAIS = $2, ANO_FUNDACAO = $3 WHERE MONT_ID = $4'
  await bd.execute(atualizacao, nome, pais, ano_fundacao, montadora_id)


@app.get('/detalhar/{montadora_id}')
async def detalhar_montadora(request: Request, montadora_id: str):
    montadora_a_detalhar = None
    montadoras = await bd.fetch('SELECT * FROM MONTADORA')

    for montadora in montadoras: 
        if montadora['mont_id'] == int(montadora_id):
            montadora_a_detalhar = montadora

    if montadora_a_detalhar is None:
        return templates.TemplateResponse(
            request, '404.html'
        )
    
    return templates.TemplateResponse(
        request, 'detalhar_montadora.html', context={'montadora': montadora_a_detalhar}
    )

@app.get('/remover/{montadora_id}')
async def remover_form(request: Request, montadora_id: str):
    montadora_a_remover = None
    montadoras = await bd.fetch('SELECT * FROM MONTADORA')

    for montadora in montadoras: 
        if montadora['mont_id'] == int(montadora_id):
            montadora_a_remover = montadora

    if montadora_a_remover is None:
        return templates.TemplateResponse(
            request, '404.html'
        )
    
    return templates.TemplateResponse(
        request, 'remover_montadora.html', context={'montadora': montadora_a_remover}
    )

@app.post('/remover_salvar/{montadora_id}')
async def remover_montadora(montadora_id: int):
  delecao = 'DELETE FROM MONTADORA WHERE MONT_ID = $1'
  await bd.execute(delecao, montadora_id)