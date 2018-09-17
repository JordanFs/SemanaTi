__author__ = 'Jordan Ferreira Saran'
'''
    SemanaTI Tweets Gatherer
    September 2018
'''

import csv
import datetime
import os
import time
import requests

from bs4 import BeautifulSoup


def __many_times_to_end(any_times: int = None):
    """
    Repeti 3 vezes caso o site requisitado esteja offline
    :param any_times: int
    :return: boolean
    """
    if any_times is not None:
        any_times += 1
        if any_times == 3:
            return True
        else:
            return False


def cleaning_links(link: str = None):
    """
    Limpa links com javascript incorporado em seu conteúdo
    :param link: str
    :return: link sem javascript
    """
    if link is not None:
        if 'javascript' in link:
            link = link[(link.find("'") + 1):]
            link = link[:(link.find("'"))]

    return link


def normalization_link(replace_link: str = None):
    """
    Subistitui a palavra "http" por "https"
    Esse procedimento é necessário para o G1
    mas em alguns sites isso não é necessário
    :param replace_link: str
    :return: link com https
    """
    return replace_link.replace("http", "https")


def create_dict_link(data: str = None):
    """
    Cria um dicionário contendo o link e a data do mesmo
    :param data: str
    :return: dict
    """
    return dict([("url", data), ("date", datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S"))])


def crete_list_like_dict_link(list_links: list = None):
    """
    Cria uma lista com seus itens em formato dict
    :param list_links: list
    :return: list com seus respectivos em formato dict
    """
    list_dicts_from_links = []
    for link in list_links:
        list_dicts_from_links.append(create_dict_link(link))
    return list_dicts_from_links


def export_data_format_csv(name_file: str = None,
                           list_links: list = None):
    """
    Exporta um arquivo CSV com os links coletados da URL
    :param name_file: str
    :param list_links: list
    :return: None
    """
    __dir_path = "".join([os.getcwd(), "/", "output", "/"])
    with open("".join([__dir_path, name_file, ".csv"]), "w", newline="\n") as output_file:
        csv_writer = csv.DictWriter(output_file, fieldnames=list_links[0].keys(), delimiter=";")
        csv_writer.writeheader()
        csv_writer.writerows(list_links)


def remove_link_duplicate_in_array(list_links: list = None):
    """
    Remove todos os links duplicados dentro da lista de links
    :param list_links:
    :return: list sem links duplicados
    """
    new_list_links = []
    for link in list_links:
        if link not in new_list_links:
            new_list_links.append(link)

    return new_list_links


check_status_page = False
many_times = 0
host = "http://g1.globo.com/sp/bauru-marilia/"
notice = normalization_link("".join([host, "noticia"]))
list_links = []

while not check_status_page:
    date_today = str(datetime.datetime.now().date()).replace("-", "")
    hour_now = datetime.datetime.now().time().strftime("%H%M%S")
    name_file = "".join(["links_", date_today, "_", hour_now])

    try:
        # Requisita URL's usando o protocolo HTTP GET
        url = requests.get(host)
        # Converte o HTML para um objeto BeautifulSoup
        # para failitar a manipuçlnao
        object_html = BeautifulSoup(url.content, "html.parser")
        # Coletando os links do G1 - Marília/Bauru
        dataset_links = object_html.find_all("a", href=True)
        if dataset_links is not None:
            list_links = []
            for link in dataset_links:
                # Verifica se existe a palavara noticia dentro de uma string
                if notice in link['href']:
                    list_links.append(link['href'])

            export_data_format_csv(name_file=name_file,
                                   list_links=crete_list_like_dict_link(remove_link_duplicate_in_array(list_links)))

    # Caso as tentativas de requisitar a URL tenha ultrapasso o tempo de 30s
    except requests.exceptions.Timeout:
        time.sleep(930)
        print('Tem esgotado, será tentado novamente.')
        check_status_page = __many_times_to_end(any_times=many_times)

    # Caso não tenha internet para realizar a conexão
    except requests.exceptions.ConnectionError:
        print('Erro de conexão, será tentando novamente em 60 segundos.')
        time.sleep(60)
        check_status_page = __many_times_to_end(any_times=many_times)

    # Caso ocorra um erro interno no código
    except requests.exceptions.RequestException as e:
        check_status_page = True
        print(e)
    time.sleep(10)
