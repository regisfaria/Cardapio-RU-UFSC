'''
  I'm not currently implementing in this file anymore, because the intent is for making a
smartphone app and doing this in this .py file isn't possible to deploy on a smartphone OS

  The updated work is going on 'menu_ufsc/menu_ufsc/app.py'

'''

import os
import requests
import datetime as dt
import webbrowser
import sys
import unidecode
from urllib.parse import urljoin
from bs4 import BeautifulSoup

def get_url(campus):
    # formata a string removendo possiveis acentos e deixando em letras minusculas
    campus = unidecode.unidecode(campus.lower())

    if campus == 'ararangua':
        url = "https://ru.ufsc.br/campus-ararangua/"
    elif campus == 'joinville':
        url = 'https://ru.ufsc.br/campus-joinville/'
    elif campus == 'cca':
        url = 'https://ru.ufsc.br/cca-2/'
    # cardapio é mostrado no site, implementar para ele depois
    #elif campus == 'trindade':
    #    url = 'https://ru.ufsc.br/ru/'
    # blumenau também possui um cardapio diferente, implementar depois
    elif campus == 'blumenau':
        url = 'http://ru.blumenau.ufsc.br/cardapios/'
    # curitibanos mostra o cardapio mensal, implementar isso depois
    elif campus == 'curitibanos':
        url = 'https://ru.ufsc.br/campus-curitibanos/'
    else:
        url = None
        print('ERRO!\nO campus escolhido não existe.')

    return url

def download_pdf(url):
    # caso não existe o diretorio, o script vai criar
    folder_location = os.getcwd() + '/downloaded_pdfs'
    if not os.path.exists(folder_location):os.mkdir(folder_location)

    # web request
    response = requests.get(url)
    # pega o html da pagina
    soup = BeautifulSoup(response.text, "html.parser")
    # seleciona todos os pdfs no html
    pdfs = soup.select("a[href$='.pdf']")
    '''
    NOTA:
    Preciso tratar as datas na hora de baixar o pdf, para saber se estou baixando o pdf certo

    -> POSSIVEL PROBLEMA:
    Diferentes campus tem formatações diferentes vou ter que criar casos especificos
    '''
    # pega o pdf mais recente
    pdf = pdfs[0]

    # I need to format the pdf text string to be able to save without problems
    file_name = pdf.text.replace(' ', '_')+ '.pdf'
    file_name = file_name.replace('/', '-')
    file_path = os.path.join(folder_location, file_name)
    # check if there is already a pdf with the same name as the latest pdf in the website
    if not os.path.exists(file_path):
        #print('Baixando o cardapio mais recente...')
        # save the file into the designeted path
        with open(file_path, 'wb') as file:
            file.write(requests.get(urljoin(url, pdf['href'])).content)

    return file_path


if __name__ == '__main__':
    # pega o nome do campus, caso tenha sido passado na execução
    campus = sys.argv[1] if len(sys.argv) > 1 else 'ararangua'
    # busca o url do devido campus
    url = get_url(campus)

    if url:
        webbrowser.open_new(download_pdf(url))
