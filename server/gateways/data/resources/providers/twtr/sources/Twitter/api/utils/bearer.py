from dotenv import load_dotenv
load_dotenv()

# Access the API key from the environment variable
import os
bearer_token = os.environ["BEARER_TOKEN"]

# 2,000,000 conversation

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"

    return r


def bearer_oauth_spaces():
    """
    Method required by bearer token authentication.
    """

    headers = {
        "Authorization": "Bearer {}".format(bearer_token),
        "User-Agent": "v2SpacesSearchPython"
    }
    return headers
