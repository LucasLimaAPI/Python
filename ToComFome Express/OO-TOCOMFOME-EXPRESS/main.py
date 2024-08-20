from fastapi import FastAPI,Query
import requests

#Forma de visualizar todos os endpoints.


app = FastAPI()

@app.get('/api/hello') #Decorator do fastAPI, podemos criar um incando que queremos disponivilizar um recurso atráves do "get"
def hello_world():
    return{'Hello':'World'}
    '''
    EndPoint que exibe uma mensagem muito utíl para a programação!!
    '''


@app.get('/api/restaurantes/')
def get_restaurantes(restaurantes: str = Query(None)): #Vamos usar Query e portanto importar o Modulo Query do fastAPI
    '''EndPoint para ver os cardápios dos restaurantes'''
    url ='https://guilhermeonrails.github.io/api-restaurantes/restaurantes.json'
    response = requests.get(url)#Chmando a resposta do 'servidor' com o requests.get 


    if response.status_code == 200:
        dados_json  = response.json()
        if restaurantes is None:
            return{'Dados':dados_json}

        dados_restaurante = []
        for item in dados_json:
            if item['Company'] == restaurantes:        
                dados_restaurante.append({
                    "item": item['Item'],
                    "price": item['price'],
                    "description": item['description']
            })
        return{'Restaurantes':restaurantes,'Cardapio':dados_restaurante}
    else:
        return{'Erro'f'{response.status_code} - {response.text}'}

