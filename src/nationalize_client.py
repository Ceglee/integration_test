from functools import cmp_to_key
from api_client import ApiClient


class NationalizeApiClient(ApiClient):
    URL = "https://api.nationalize.io/"
    PARAM_NAME = "name"

    def _handle_response(self, json):
        countries = json.get("country")
        if countries and isinstance(countries, list) and len(countries) > 0:
            countries.sort(key=cmp_to_key(NationalizeApiClient._compare_countries))
            return countries[0].get("country_id")
        return None

    def _get_url(self):
        return self.URL

    def _get_param_name(self):
        return self.PARAM_NAME

    @staticmethod
    def _compare_countries(country_1, country_2):
        return country_2.get("probability", 0) - country_1.get("probability", 0)

