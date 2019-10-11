"""
Mostra o cardápio do RU-UFSC baseado na escolha de um campus
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

import os
import requests
import datetime as dt
import webbrowser
import sys
import unidecode
import logging
from urllib.parse import urljoin
from bs4 import BeautifulSoup

# Defining logs !TODO: Have a better study on logs and how to use it
logger = logging.getLogger('menuru')
hdlr = logging.FileHandler('menuru.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

class Menuru(toga.App):

    def startup(self):
        # Define the main box app
        main_box = toga.Box()

        self.main_window = toga.MainWindow(title=self.name)
        self.main_window.content = main_box
        self.main_window.show()

        # Define a intro label for the user
        # NOTE: should I store this inside a box?
        self.intro_label = toga.Label('Escolha um campi', id='intro_text')

        # Creating a selection of campus for the user
        self.campus_selection = toga.Selection(items=['Araranguá', 'Blumenau',
                                                                'Curitibanos', 'Florianópolis',
                                                                'Joinville', 'CCA'])
        # Implement on_press function
        #self.search_menu_button = toga.Button('Ver cardápio', on_press=self.search_menu(self.campus_selection))
        self.search_menu_button = toga.Button('Ver cardápio')

        # Creating some more boxes
        intro_label_box = toga.Box()
        intro_label_box.add(self.intro_label)

        selection_box = toga.Box()
        selection_box.add(self.campus_selection)

        button_box = toga.Box()
        button_box.add(self.search_menu_button)

        # Styling the boxes
        main_box.style.update(direction=COLUMN, padding_top=10)
        intro_label_box.style.update(direction=ROW, padding=5)
        selection_box.style.update(direction=ROW, padding=5)
        button_box.style.update(direction=ROW, padding=5)

        intro_label_box.style.update(flex=1)
        selection_box.style.update(flex=1, padding_left=160)

        intro_label_box.style.update(width=100, padding_left=10)
        selection_box.style.update(width=100, padding_left=10)

        button_box.style.update(padding=15, flex=1)

        main_box.add(intro_label_box)
        main_box.add(selection_box)
        main_box.add(button_box)

        return main_box

    def get_url(campus):
        # formata a string removendo acentos e deixando em letras minusculas
        campus = unidecode.unidecode(campus.lower())

        if campus == 'ararangua':
            url = "https://ru.ufsc.br/campus-ararangua/"
        elif campus == 'joinville':
            url = 'https://ru.ufsc.br/campus-joinville/'
        elif campus == 'cca':
            url = 'https://ru.ufsc.br/cca-2/'
        # cardapio é mostrado no site, implementar para ele depois
        #elif campus == 'florianopolis':
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

    def search_menu(self, campus):
        # caso não existe o diretorio, o script vai criar
        folder_location = os.getcwd() + '/downloaded_pdfs'
        if not os.path.exists(folder_location):os.mkdir(folder_location)

        # web request
        try:
            response = requests.get(url)
        except Exception as e:
            # probably it was a connection issue
            logger.error(e)

        # pega o html da pagina
        soup = BeautifulSoup(response.text, "html.parser")
        # seleciona todos os pdfs no html
        pdfs = soup.select("a[href$='.pdf']")
        '''
        Notas

        Nesta etapa é preciso trabalhar de diferente maneiras para diferentes campus


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

def main():
    return Menuru('MenuRU', 'github.com/regisfaria.MenuRU')
