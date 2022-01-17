from user_details import UserDetails


class UserDetailsService:

    def get_user_details(self, user_name):
        return self.init_user_details(user_name)

    def init_user_details(self, user_name):
        parts = user_name.split(" ")

        if len(parts) == 1:
            return UserDetails(parts[0], None)

        else:
            return UserDetails(parts[0], parts[-1])



