from dataclasses import dataclass


@dataclass
class UserEntity:

    def __init__(self, res_data):
        self.id = res_data['id']
        self.name = res_data['name']
        self.username = f"@{res_data['username']}"
        self.img = res_data['profile_image_url']
        self.verified = res_data['verified']
        self.metrics = res_data['public_metrics']
        try:
            self.location = res_data['geo']
            # this is extremely slow, make faster !
        except KeyError:
            self.location = None
