__author__ = 'Jordan Ferreira Saran'
'''
    SemanaTI Tweets Gatherer
    September 2018
'''

import pandas


class LinkWrapper:

    def __init__(self, link: pandas):
        self.url = getattr(link, "url")
        self.date = getattr(link, "date")
