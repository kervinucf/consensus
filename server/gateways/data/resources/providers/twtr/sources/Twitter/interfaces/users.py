from server.gateways.data.resources.providers.twtr.sources.Twitter.api.resolver import TwitterQuery


class UserProvider:

    @staticmethod
    def lookup_user(user_name):
        return [user.__dict__ for user in TwitterQuery(user_name=user_name)][0]
