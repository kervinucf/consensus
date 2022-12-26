from server.gateways.data.resources.providers.twtr.sources.Twitter.api.utils.bearer import bearer_oauth


def create_params(tweet_query=None, tweet_id_list=None, lookup=False, search=False, max_results=10):
    params = {
        'user.fields': 'created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,'
                       'protected,public_metrics,url,username,verified,withheld',
        'poll.fields': 'duration_minutes,end_datetime,id,options,voting_status',
        'place.fields': 'contained_within,country,country_code,full_name,geo,id,name,place_type',
        'media.fields': 'duration_ms,height,media_key,preview_image_url,type,url,width,alt_text,variants',
        'tweet.fields': 'attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,'
                        'in_reply_to_user_id,lang,public_metrics,possibly_sensitive,referenced_tweets,reply_settings,'
                        'source,text,withheld',
        'expansions': 'attachments.poll_ids,attachments.media_keys,author_id,entities.mentions.username,geo.place_id,'
                      'in_reply_to_user_id,referenced_tweets.id,referenced_tweets.id.author_id',
        'max_results': max_results,
    }

    if lookup:
        if type(tweet_id_list) != list:
            tweet_id_list = [tweet_id_list]
        tweet_ids = ",".join(str(tweet_id) for tweet_id in tweet_id_list)
        params['ids'] = tweet_ids
    if search:
        params['query'] = tweet_query

    return params


# *****************************
# lookup tweet by id

def lookup_user_tweets(user_id):
    # 900 request per 15 minutes
    url = f"https://api.twitter.com/2/users/{user_id}/tweets/"
    params = create_params()
    return {
        'url': url,
        'params': params,
        'headers': bearer_oauth,
        "GET": True
    }


def lookup_tweets(id_list):
    # 900 request per 15 minutes
    url = "https://api.twitter.com/2/tweets/"
    params = create_params(tweet_id_list=id_list, lookup=True)
    return {
        'url': url,
        'params': params,
        'headers': bearer_oauth,
        "GET": True
    }


def search_tweets(query, max_results=10):
    # 900 request per 15 minutes
    url = 'https://api.twitter.com/2/tweets/search/recent'
    params = create_params(tweet_query=query, search=True,
                           max_results=max_results)
    return {
        'url': url,
        'params': params,
        'headers': bearer_oauth,
        "GET": True
    }


def search_conversation(conversation_id, max_results=10):
    # 900 request per 15 minutes
    query = f"conversation_id:{conversation_id}"
    url = 'https://api.twitter.com/2/tweets/search/recent'
    params = create_params(tweet_query=query, search=True,
                           max_results=max_results)
    return {
        'url': url,
        'params': params,
        'headers': bearer_oauth,
        "GET": True
    }
# *****************************
