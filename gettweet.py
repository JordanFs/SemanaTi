__author__ = 'Jordan Ferreira Saran'
'''
    SemanaTI Tweets Gatherer
    September 2018
'''

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json


class StdOutListener(StreamListener):

    def on_data(self, data):
        with open('tweets.json', 'a') as file:
            parsed_data = json.loads(data)
            json.dump(parsed_data, file, indent=2)

        return True

    def on_error(self, status):
        print(status)
        if status == 420:
            # Os clientes excedem o número limitado de tentativas para se conectar à API de fluxo.
            # A quantidade de tempo que um cliente tem que esperar aumenta exponencialmente
            return False

        else:
            return True


if __name__ == '__main__':

    # Definir credenciais
    CONSUMER_KEY = 'SUA_CONSUMER_KEY'
    CONSUMER_SECRET = 'SUA_CONSUMER_SECRET'
    ACCESS_TOKEN_KEY = 'SUA_TOKEN_KEY'
    ACCESS_TOKEN_SECRET = 'SUA_ACCESS_TOKEN_SECRET'

    # Pegar API de acesso com minhas credenciais
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)

    # Definir a região que deseja coletar os tweets
    # As informações logo abaixo são da cidade de São Paulo
    # ([longitude_min, latitude_min, longitude_max, latitude_max])
    boundbox = [-46.8254, -24.0084, -46.3648, -23.3576]

    # Isso lida com a autenticação do Twitter e a conexão com a Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
    stream = Stream(auth, l)
    # languages: As linguagens que desejo filtrar do tweet
    # track: Defini as palavras chaves que desejo filtrar dos tweets
    stream.filter(locations=boundbox, track=["roubo", "#roubo"], languages=["pt"])
