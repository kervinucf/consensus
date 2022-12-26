from server.gateways.data.resources.providers.twtr.sources.Twitter.api.resolver import TwitterQuery


class SpacesProvider:

    @staticmethod
    def search_for_spaces(search_term):
        if search_term:
            api_spaces = TwitterQuery(space_search=search_term)
            if api_spaces:
                return [space.__dict__ for space in api_spaces]
            else:
                return None

    @staticmethod
    def lookup_space(space_id):
        api_space = TwitterQuery(space_id=space_id)
        if api_space:
            return [space.__dict__ for space in api_space]
        else:
            return None

    def lookup_top_spaces(self):
        def find_top_space(term):
            top_space = None

            for space in self.search_for_spaces(search_term=term):
                if top_space is None and space is not None or space['space']['metrics'][
                    'participant_count'] \
                        > top_space['space']['metrics']['participant_count']:
                    top_space = space
            return top_space

        find_spaces_for = [
            "Bitcoin",
            "Stock",
            "Sports",
            "Music",
            "Politics",
        ]

        top_spaces = {}

        for space_term in find_spaces_for:
            top_spaces[space_term] = find_top_space(space_term)

        return top_spaces
