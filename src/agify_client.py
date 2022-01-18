from api_client import ApiClient


class AgifyApiClient(ApiClient):
    URL = "https://api.agify.io/"
    PARAM_NAME = "name"
    PROPERTY_NAME = "age"

    def _handle_response(self, json):
        return json.get("age")

    def _get_url(self):
        return self.URL

    def _get_param_name(self):
        return self.PARAM_NAME

    def _get_property_name(self):
        return self.PROPERTY_NAME
