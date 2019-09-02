import os
import requests
import datetime as dt
import webbrowser
from urllib.parse import urljoin
from bs4 import BeautifulSoup

url = "https://ru.ufsc.br/campus-ararangua/"
# If there is no such folder, the script will create one automatically
folder_location = '/home/regisf/Documents/dev/python/cardapio_ru/downloaded_pdfs'
if not os.path.exists(folder_location):os.mkdir(folder_location)

# make a web request
response = requests.get(url)
# trying to find a pdf file in ufsc website
soup = BeautifulSoup(response.text, "html.parser")
# select all pdfs from ufsc website
pdfs = soup.select("a[href$='.pdf']")
# get the latest pdf in the website
pdf = pdfs[0]

# I need to format the pdf text string to be able to save without problems
file_name = pdf.text.replace(' ', '_')+ '.pdf'
file_name = file_name.replace('/', '-')
file_path = os.path.join(folder_location, file_name)
# check if there is already a pdf with the same name as the latest pdf in the website
if not os.path.exists(file_path):
    print('Baixando o cárdapio mais recente...')
    # save the file into the designeted path
    with open(file_path, 'wb') as file:
        file.write(requests.get(urljoin(url, pdf['href'])).content)
else:
    print('O cárdapio mais recente já foi baixado.')

print('Abrindo o cárdapio da semana...')
webbrowser.open_new(file_path)
