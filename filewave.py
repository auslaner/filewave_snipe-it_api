import requests


class FilewaveConnection:
    def __init__(self, api_key, base_url, port=20445):
        self.api_key = api_key
        self.base_url = base_url
        self.port = int(port)

    def get_all_queries(self):
        headers = {"Authorization": self.api_key}
        resp = requests.request("GET", self.base_url + ":" + str(self.port) + "/inv/api/v1/query/", headers=headers)
        return resp

    def get_query_results_by_id(self, query_id):
        headers = {"Authorization": self.api_key}
        query_url = f"{self.base_url}:{str(self.port)}/inv/api/v1/query_result/{query_id}"
        resp = requests.request("GET", query_url, headers=headers)
        return resp


def id_from_query_name(list_results, query_name):
    for query in list_results:
        if query_name in query['name']:
            return query['id']
