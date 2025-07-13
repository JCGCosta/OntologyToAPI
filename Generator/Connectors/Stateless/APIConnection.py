import requests as req

class APIConnection:
    def __init__(self, args):
        self.baseURL = args["hasBaseURL"]

    def exec_query(self, endpoint_and_params: str):
        fullURL = self.baseURL + endpoint_and_params
        try:
            return requests.get(fullURL).json()
        except Exception as e:
            return {'error': str(e)}