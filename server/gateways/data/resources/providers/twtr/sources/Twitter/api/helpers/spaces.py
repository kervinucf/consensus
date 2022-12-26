from server.gateways.data.resources.providers.twtr.sources.Twitter.api.utils.bearer import bearer_oauth


def create_params(space_id=None, space_query=None, search=False, lookup=False):
    params = {'user.fields': 'created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,'
                             'protected,public_metrics,url,username,verified,withheld',
              'topic.fields': 'id,name,description',
              'space.fields': 'host_ids,created_at,creator_id,id,lang,invited_user_ids,participant_count,'
                              'speaker_ids,started_at,ended_at,subscriber_count,topic_ids,state,title,'
                              'updated_at,scheduled_start,is_ticketed',
              'expansions': 'invited_user_ids,speaker_ids,creator_id,host_ids'
              }

    if lookup:
        # You can adjust ids to include a single Tweets.
        # Or you can add to up to 100 comma-separated IDs
        params['ids'] = space_id
    if search:
        params['query'] = space_query

    return params


def search_spaces(query):
    url = "https://api.twitter.com/2/spaces/search"
    params = create_params(space_query=query, search=True)

    return {
        'url': url,
        'params': params,
        'headers': bearer_oauth,
        "GET": True
    }


def lookup_spaces(_id):
    url = "https://api.twitter.com/2/spaces/"
    params = create_params(space_id=_id, lookup=True)
    return {
        'url': url,
        'params': params,
        'headers': bearer_oauth,
        "GET": True
    }
