
from dataclasses import dataclass


class MatchingRule:
    def __init__(self, res_data):
        # 'id', 'value', 'tag'
        self.id = res_data['id']
        self.value = res_data['value']
        self.tag = res_data['tag']


@dataclass
class RuleEntity:

    def __init__(self, res_data):
        # 'id', 'value', 'tag'
        self.rules_found = {}

        try:
            rule_data_list = res_data["res"]["data"]
        except KeyError:
            rule_data_list = None

        if rule_data_list:
            for rule_data in rule_data_list:
                rule_entity = MatchingRule(res_data=rule_data)
                self.rules_found[rule_entity.id] = rule_entity.__dict__

        self.success = True

        try:
            errors = res_data["res"]["errors"]
            for error in errors:
                title = error["title"]
                if title != "DuplicateRule":
                    self.success = False
        except KeyError:
            errors = None
