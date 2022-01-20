import time
from concurrent.futures.thread import ThreadPoolExecutor
from agify_client import AgifyApiClient
from genderize_client import GenderizeApiClient
from nationalize_client import NationalizeApiClient

NATIONALIZE_API_CLIENT = NationalizeApiClient()
GENDERIZE_API_CLIENT = GenderizeApiClient()
AGIFY_API_CLIENT = AgifyApiClient()


class UserDetailsService:

    def get_user_details(self, user_name):
        start = time.time_ns()
        user_details = self._init_user_details(user_name)
        executor = ThreadPoolExecutor(max_workers=3)

        try:
            first_name = user_details["first_name"]
            futures = []

            if not NATIONALIZE_API_CLIENT.hit_cache(user_details, first_name):
                futures.append(executor.submit(lambda: NATIONALIZE_API_CLIENT.enhance_user_data(user_details, first_name)))

            if not GENDERIZE_API_CLIENT.hit_cache(user_details, first_name):
                futures.append(executor.submit(lambda: GENDERIZE_API_CLIENT.enhance_user_data(user_details, first_name)))

            if not AGIFY_API_CLIENT.hit_cache(user_details, first_name):
                futures.append(executor.submit(lambda: AGIFY_API_CLIENT.enhance_user_data(user_details, first_name)))

            while time.time_ns() - start < 10_000_000:
                finished = len(futures) == 0 or all(map(lambda future: future.done(), futures))
                if finished:
                    return user_details
        finally:
            executor.shutdown(False)

        return user_details

    def _init_user_details(self, user_name):
        parts = user_name.split(" ")

        if len(parts) == 1:
            return {"first_name": parts[0]}

        elif len(parts) > 1:
            return {"first_name": parts[0], "last_name": parts[-1]}

        else:
            return None
