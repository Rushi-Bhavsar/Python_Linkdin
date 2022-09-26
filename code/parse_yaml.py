import yaml
from yaml.loader import SafeLoader

FILE_NAME = '../settings/credential.yaml'


class Credentials:
    def __init__(self):
        with open(FILE_NAME, 'r') as file:
            data = yaml.load(file, SafeLoader)
            self.__login = data['LOGIN']
            self.__logout = data['LOGOUT']
            self.__username = data['USERNAME']
            self.__password = data['PASSWORD']

    @property
    def login(self):
        return self.__login

    @property
    def logout(self):
        return self.__logout

    @property
    def username(self):
        return self.__username

    @property
    def password(self):
        return self.__password


cred_data = Credentials()

