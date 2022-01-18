import requests

IMPLEMENTATION_ERROR_MESSAGE = "Must be implemented in child class."


class ApiClient:

    def __init__(self, property_name):
        self.property_name = property_name
        self.cache = {}

    def enhance_user_data(self, user_data, param_value):
        value = self.cache.get(param_value)

        if value:
            user_data[self.property_name] = value
            return

        response = requests.get(self._get_url(), {self._get_param_name(): param_value})
        status_code = response.status_code

        attempt = 0
        while attempt < 3:
            if status_code == 200:
                json = response.json()
                value = self._handle_response(json)
                self.cache[param_value] = value
                user_data[self.property_name] = value
                return

            elif 400 <= status_code < 500:
                self.cache[param_value] = None
                user_data[self.property_name] = None
                return

            elif status_code >= 500:
                attempt += 1

    def _handle_response(self, json):
        raise NotImplementedError(IMPLEMENTATION_ERROR_MESSAGE)

    def _get_url(self):
        raise NotImplementedError(IMPLEMENTATION_ERROR_MESSAGE)

    def _get_param_name(self):
        raise NotImplementedError(IMPLEMENTATION_ERROR_MESSAGE)
