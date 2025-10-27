import requests as req

class APIConnection:
    def __init__(self, args):
        self.baseURL = args["hasRequestURL"]

    def exec_query(self, endpoint_params: str):
        fullURL = self.baseURL + endpoint_params
        try:
            return req.get(fullURL).json()
        except Exception as e:
            return {'error': str(e)}