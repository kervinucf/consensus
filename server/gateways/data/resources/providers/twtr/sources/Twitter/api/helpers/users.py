from server.gateways.data.resources.providers.twtr.sources.Twitter.api.utils.bearer import bearer_oauth


def create_params(user_query=None, user_id_list=None, lookup=False, search=False):
    params = {
        'user.fields': 'created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,'
                       'protected,public_metrics,url,username,verified,withheld'
    }

    if lookup:
        if type(user_id_list) != list:
            user_id_list = [user_id_list]
        user_ids = ",".join(str(user_id) for user_id in user_id_list)
        params['usernames'] = user_ids

    return params


# *****************************
# lookup tweet by id

def lookup_users(id_list):
    # 900 request per 15 minutes
    url = "https://api.twitter.com/2/users/by?"
    params = create_params(user_id_list=id_list, lookup=True)
    return {
        'url': url,
        'params': params,
        'headers': bearer_oauth,
        "GET": True
    }
# *****************************
