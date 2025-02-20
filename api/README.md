# INSTALANDO O BACKEND

## DEPENDÊNCIAS:
1. PYTHON 3.11+

---
## COMANDOS PARA SUBIR AMBIENTE:

#### CRIAR AMBIENTE PYTHON LOCAL
`
python -m venv env
`
#### ACESSAR AMBIENTE PYTHON LOCAL
`
. .\env\Scripts\activate
`

#### INSTALAR PACOTES NECESSÁRIOS
`
pip install -r requirements.txt
`

#### SUBIR SERVIDOR BACKEND
`
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
`

---
## ACESSE A DOCUMENTAÇÃO DA API

##### UTILIZE A URL: [Link do servidor local](http://localhost:8000/api/documentation)

---
## API EM FASE DE DESENVOLVIMENTO

##### Algum erro foi encontrado? Fale com [@CoderGustavo](https://github.com/CoderGustavo)
