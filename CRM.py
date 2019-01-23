import time
import requests
from requests.utils import requote_uri
import configparser

from datetime import datetime

config = configparser.ConfigParser()
config.read('Config.ini')
print(config)

USER_NAME = config['DEFAULT']['USERNAME']
API_KEY = config['DEFAULT']['API_KEY']


class Api:
    def __init__(self, title):
        self.id = ''
        self.base_url = 'http://54.149.103.44'
        self.uri = 'http://54.149.103.44/index.php/api2/'
        self.url = ''
        self.data = ''
        self.query_limit = '9999'
        self.query_order = '-lastUpdated'
        self.title = title
        self.response = ''
        # ---Titles---
        # Account
        # Property
        # Contacts
        # Leads
        # Campaign
        # Actions
        # Opportunity
        # Product
        # Services
        # BugReports
        # X2List
        self.format = '.json'
        #  Account actions index.php/api2/{_class}/{_id}/Actions
        #  Account specific action index.php/api2/{_class}/{_id}/Actions/{_actionId}.json
        #  Account create action index.php/api2/{_class}/{_id}/Actions

    def count(self):
        self.url = self.uri + self.title + '/count'
        self.data = requests.get(self.url, auth=(USER_NAME, API_KEY)).json()
        time.sleep(0.2)
        return self.data

    def search_models(self):
        self.url = self.uri + self.title + '/models' + self.format
        self.data = requests.get(self.url, auth=(USER_NAME, API_KEY)).json()
        time.sleep(0.2)
        return self.data

    def search_model(self):
        self.url = self.uri + 'models' + self.format
        self.data = requests.get(self.url, auth=(USER_NAME, API_KEY)).json()
        for model in self.data:
            this_model = model['modelName']
            if self.title == this_model:
                return model['attributes']

    def create(self, payload):
        self.url = self.uri + self.title + '/'
        json_data = payload
        self.data = requests.post(self.url, auth=(USER_NAME, API_KEY), json=json_data).json()
        time.sleep(0.2)
        return self.data

    def update(self, number, payload):
        self.url = self.uri + self.title + '/' + number + self.format
        json_data = payload
        data = requests.put(self.url, auth=(USER_NAME, API_KEY), json=json_data).text
        self.response = requests.get(self.url, auth=(USER_NAME, API_KEY)).status_code

        time.sleep(0.2)
        return data

    def delete(self, number):
        self.url = self.uri + self.title + '/' + number + self.format
        self.data = requests.delete(self.url, auth=(USER_NAME, API_KEY)).text
        self.response = requests.get(self.url, auth=(USER_NAME, API_KEY)).status_code
        time.sleep(0.2)
        return self.data

    def search(self, number):
        self.url = self.uri + self.title + '/' + number + self.format
        self.data = requests.get(self.url, auth=(USER_NAME, API_KEY)).json()
        self.response = requests.get(self.url, auth=(USER_NAME, API_KEY)).status_code

        time.sleep(0.2)
        return self.data

    def search_all(self):
        url = self.uri + self.title + '?_order=' + self.query_order + '&_limit=' + self.query_limit
        self.data = requests.get(url, auth=(USER_NAME, API_KEY)).json()
        return self.data

    def search_all_by_field(self, field, query):
        q = str('&_' + field + '=' + str(query) + '_useFirst=1')
        url = self.uri + self.title + '?_order=' + self.query_order + '&_limit=' + self.query_limit + q
        url = requote_uri(url)
        self.data = requests.get(url, auth=(USER_NAME, API_KEY)).json()
        time.sleep(0.2)
        return self.data

    def search_all_by(self, field, value):
        try:
            url = self.uri + self.title + '/by:' + field + '=' + value + self.format
            url = requote_uri(url)
            self.data = requests.get(url, auth=(USER_NAME, API_KEY)).json()
            self.response = requests.get(url, auth=(USER_NAME, API_KEY)).status_code
            time.sleep(0.2)
            return self.data
        except IndexError:
            print('Search all error')

    def search_by_uri(self, uri):
        url = self.base_url + uri
        self.data = requests.get(url, auth=(USER_NAME, API_KEY)).json()
        time.sleep(0.2)
        return self.data

    def search_relationship(self, number, relationship_id):
        self.url = self.uri + self.title + '/' + number + '/relationships/' + relationship_id + self.format
        self.data = requests.get(self.url, auth=(USER_NAME, API_KEY)).json()
        self.response = requests.get(self.url, auth=(USER_NAME, API_KEY)).status_code

        time.sleep(0.2)
        return self.data

    def search_relationships(self, number):
        self.url = self.uri + self.title + '/' + str(number) + '/relationships'
        self.data = requests.get(self.url, auth=(USER_NAME, API_KEY)).json()
        self.response = requests.get(self.url, auth=(USER_NAME, API_KEY)).status_code

        time.sleep(0.2)
        return self.data

    def add_relationship(self, number, payload):
        self.url = self.uri + self.title + '/' + number + '/relationships'
        json_data = payload
        self.data = requests.post(self.url, auth=(USER_NAME, API_KEY), json=json_data).text
        time.sleep(0.2)
        return self.data

    def delete_relationship(self, number, relationship_id):
        self.url = self.uri + self.title + '/' + number + '/relationships/' + relationship_id + self.format
        self.data = requests.delete(self.url, auth=(USER_NAME, API_KEY)).text
        self.response = requests.get(self.url, auth=(USER_NAME, API_KEY)).status_code

        time.sleep(0.2)
        return self.data

    def search_tags(self, number):
        self.url = self.uri + self.title + '/' + number + '/tags'
        self.data = requests.get(self.url, auth=(USER_NAME, API_KEY)).json()
        self.response = requests.get(self.url, auth=(USER_NAME, API_KEY)).status_code

        time.sleep(0.2)
        return self.data

    def search_by_tags(self, tags):
        self.url = self.uri + 'tags/' + tags + '/' + self.title
        self.data = requests.get(self.url, auth=(USER_NAME, API_KEY)).json()
        self.response = requests.get(self.url, auth=(USER_NAME, API_KEY)).status_code
        print(self.data)
        time.sleep(0.2)
        return self.data

    def add_tag(self, number, payload):
        self.url = self.uri + self.title + '/' + number + '/tags'
        json_data = payload
        self.data = requests.post(self.url, auth=(USER_NAME, API_KEY), json=json_data).text
        time.sleep(0.2)
        return self.data

    def delete_tag(self, number, payload):
        self.url = self.uri + self.title + '/' + number + '/tags/' + str(payload) + '.json'
        self.data = requests.delete(self.url, auth=(USER_NAME, API_KEY)).text
        self.response = requests.get(self.url, auth=(USER_NAME, API_KEY)).status_code
        time.sleep(0.2)
        return self.data

    def search_actions(self, number):
        self.url = self.uri + self.title + '/' + str(number) + '/Actions'
        self.data = requests.get(self.url, auth=(USER_NAME, API_KEY)).json()
        time.sleep(0.2)
        return self.data

    def search_action(self, number, action_id):
        self.url = self.uri + self.title + '/' + str(number) + '/Actions/' + action_id + self.format
        self.data = requests.get(self.url, auth=(USER_NAME, API_KEY)).json()
        time.sleep(0.2)
        return self.data

    def add_action(self, number, payload):
        self.url = self.uri + self.title + '/' + number + '/Actions'
        json_data = payload
        self.data = requests.post(self.url, auth=(USER_NAME, API_KEY), json=json_data).text
        time.sleep(0.2)
        return self.data

    def delete_action(self, number, action_id):
        self.url = self.uri + self.title + '/' + number + '/Actions/' + action_id + self.format
        self.data = requests.delete(self.url, auth=(USER_NAME, API_KEY)).text
        time.sleep(0.2)
        return self.data
