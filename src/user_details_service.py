from nationalize_client import NationalizeApiClient

NATIONALIZE_API_CLIENT = NationalizeApiClient("nationality")


class UserDetailsService:

    def get_user_details(self, user_name):
        user_details = self.init_user_details(user_name)
        NATIONALIZE_API_CLIENT.enhance_user_data(user_details, user_details["first_name"])
        return user_details

    def init_user_details(self, user_name):
        parts = user_name.split(" ")

        if len(parts) == 1:
            return {"first_name": parts[0]}

        elif len(parts) > 1:
            return {"first_name": parts[0], "last_name": parts[-1]}

        else:
            return None
