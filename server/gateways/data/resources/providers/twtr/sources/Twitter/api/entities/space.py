from cleantext import clean
import json
from server.gateways.data.resources.providers.twtr.sources.Twitter.api.entities.user import UserEntity
from dataclasses import dataclass
from server.gateways.data.resources.providers.geo.sources.Nominatim.helpers import find_coordinates


def extract_content(data):
    ################################################################################
    ################################ FIX ###########################################
    ################################################################################
    # find space types from included
    _type = 'text'
    ################################################################################
    ################################################################################
    ################################################################################

    try:
        geo = data['geo']
    except KeyError:
        geo = None

    try:
        topic_ids = data['topic_ids']
    except KeyError:
        topic_ids = None

    try:
        scheduled_start = data['scheduled_start']
    except KeyError:
        scheduled_start = None

    try:
        speaker_ids = data['speaker_ids']
    except KeyError:
        speaker_ids = None

    try:
        title = data['title']
    except KeyError:
        title = None

    return {
        'id': data['id'],
        'owner_id': data['creator_id'],

        'created_at': data['created_at'],
        'scheduled_start': scheduled_start,
        'state': data['state'],
        'content': {
            "title": title,
            'topic_ids': topic_ids,
            "lang": data['lang'],
        },
        'speaker_ids': speaker_ids,
        'host_ids': data['host_ids'],
        'is_ticketed': data['is_ticketed'],
        'metrics': {
            'subscriber_count': data['subscriber_count'],
            'participant_count': data['participant_count'],
        },
        "geo": geo
    }


def create_meta(owner, data):
    if data['geo']:
        location = data['geo']
        location_derived = 'geo'
    else:
        location = owner['coordinates']
        location_derived = 'profile'

    sentiment = None

    matching_rule = ''

    return {
        'geo': location,
        'location_derived': location_derived,
        'sentiment': '',
        'tag': matching_rule
    }


@dataclass
class SpaceEntity:

    def __init__(self, res_data):

        self.owner = None
        self.hosts = {}
        self.speakers = {}
        self.participants = {}

        self.meta = None

        self.space = extract_content(res_data)

    def streamable(self):
        # hash of geo - sentiment - space types -
        return json.dumps()

    def assign_roles(self, users_included):

        if users_included:

            for user_dict in users_included:
                user_found = UserEntity(res_data=user_dict)
                if user_found.id == self.space['owner_id']:
                    self.owner = user_found.__dict__
                    # todo: update to look for city vs country
                    self.owner['coordinates'] = find_coordinates(
                        location=self.owner['location'])

                if self.space['host_ids'] and user_found.id in self.space['host_ids']:
                    self.hosts[user_found.id] = user_found.__dict__
                if self.space['speaker_ids'] and user_found.id in self.space['speaker_ids']:
                    self.speakers[user_found.id] = user_found.__dict__

                self.participants[user_found.id] = user_found.__dict__

        self.meta = create_meta(owner=self.owner, data=self.space)

    def minify(self):
        hosts = {}
        speakers = {}
        participants = {}

        for user_id, user in self.participants.items():
            if user_id in self.space['host_ids']:
                store = hosts
            elif user_id in self.space['speaker_ids']:
                store = speakers
            else:
                store = participants
            store[user_id] = {
                "id": user["id"],
                "img": user["img"],
            }

        return {
            "owner": {
                "id": self.owner["owner_id"],
                "img": self.owner["img"],
            },
            "participants": participants,
            "hosts": hosts,
            "speakers": speakers,
            "space": {
                "id": self.tweet["id"],
                "created_at": self.tweet["created_at"],
                "participant_count": len(participants.items()),
            },
            "coordinates": self.owner["coordinates"],

        }
    # create minified object for stream

    # owner -> id - img - geo
    # hosts -> id - img - geo
    # speakers -> id - img - geo
    # participants -> id - img - geo
    # space -> title - participant count - space_id
