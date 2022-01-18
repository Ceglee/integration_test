from api_client import ApiClient


class GenderizeApiClient(ApiClient):
    URL = "https://api.genderize.io/"
    PARAM_NAME = "name"
    PROPERTY_NAME = "gender"

    def _handle_response(self, json):
        return json.get("gender")

    def _get_url(self):
        return self.URL

    def _get_param_name(self):
        return self.PARAM_NAME

    def _get_property_name(self):
        return self.PROPERTY_NAME
