import json
import re

import requests


class UNotion:
    TOKEN = ''
    RESULTS_ALREADY_SEARCHED = []

    def __init__(self, token):
        self.TOKEN = token

    def get_databases_linked(self):
        if not self.RESULTS_ALREADY_SEARCHED or len(self.RESULTS_ALREADY_SEARCHED) == 0:
            response = requests.post("https://api.notion.com/v1/search", headers={
                "Authorization": "Bearer %s" % self.TOKEN,
                "Notion-Version": "2021-08-16"
            })
            self.RESULTS_ALREADY_SEARCHED = response.json()['results']

        return self.RESULTS_ALREADY_SEARCHED

    def upload_to_notion(self, database_id, note):
        tags = self.extract_tags(note)
        titles = self.extract_title(note)

        url = 'https://api.notion.com/v1/pages'
        headers = {
            "Authorization": "Bearer %s" % self.TOKEN,
            "Content-type": "application/json",
            "Notion-Version": "2021-08-16"
        }
        data = {
            "parent": {"database_id": database_id},
            "properties": {
                "Name": self.build_name(titles),
                "Tags": self.build_tags(tags)
            }
        }

        requests.post(url, headers=headers, data=json.dumps(data))

    def extract_tags(self, note):
        return re.compile("#(\w+)").findall(note)

    def extract_title(self, note):
        return re.compile("(?<=\[).*?(?=\])").findall(note)

    def build_name(self, titles):
        if not titles or len(titles) == 0:
            return
        return {
            "title": [{"text": {"content": titles[0]}}]
        }

    def build_tags(self, tags):
        multi_select = []
        print(tags)
        for tag in tags:
            multi_select.append({"name": tag})
        return {
            "multi_select": multi_select
        }
