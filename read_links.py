__author__ = 'Jordan Ferreira Saran'
'''
    SemanaTI Tweets Gatherer
    September 2018
'''

import time
import pandas
import os

from LinkWrapper import LinkWrapper


# remove o arquivo __init__.py da lista de arquivos encontrada na pasta output
def remove__init__(dataset_files=None):
    if dataset_files is not None:
        dataset_files.pop(dataset_files.index("__init__.py"))


# Cria o diretório para a pasta output
path = "".join([os.getcwd(), "/output/"])
check_folder = False
while not check_folder:
    # Coleta os nomes do arquivos dentro da psta output
    list_files_links = os.listdir(path)
    remove__init__(list_files_links)

    # Verifico se não esta vazio a pasta outpup que contém os arquivos gerados.
    if list_files_links is not None:
        for file in list_files_links:
            # Ler arquivos de links criados pela coleta de links do site G1
            dataset_link = pandas.read_csv("".join([path, file]), delimiter=";", low_memory=False)
            for link in dataset_link.itertuples(index=True, name='Pandas'):
                # Encapsulamento do dict link
                object_link = LinkWrapper(link=link)
                # Agora consigo acessar com mais facilidade as variavéis que estavam dentro do arquivo CSV
                print(object_link.url)
                print(object_link.date)
                print("------")
            os.remove("".join([path, file]))
    time.sleep(60)
