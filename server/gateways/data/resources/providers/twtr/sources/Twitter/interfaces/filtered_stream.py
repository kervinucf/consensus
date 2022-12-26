from server.gateways.data.resources.providers.twtr.sources.Twitter.api.resolver import TwitterQuery
from server.lib.utils.database import update_record, get_from_db, delete_record, get_table
from lib.Twitter.api.endpoints.utils.helpers import get_current_time
from flask import Blueprint

stream_rules = Blueprint('stream_rules', __name__)


class StreamRulesProvider:

    def fetch_active_rules():
        api_rules = TwitterQuery(get_stream_rules=True)
        if api_rules:
            if len(api_rules.__dict__['rules_found']) > 0:
                return api_rules.__dict__
            else:
                return None
        else:
            return None

    def add_rules(rule_set_to_add):
        rule_set = rule_set_to_add['rule_set']
        event = rule_set_to_add['event']
        _type = rule_set_to_add['type']
        sample = rule_set_to_add['sample']

        if not sample:
            sample = 1

        def format_rule(rules, tag):
            rules = list(rules)[:20]
            if _type == "CASHTAG":
                rules = '$%s' % ' OR $'.join(rules)
            elif _type == "FROM_USER":
                rules = 'from:%s' % ' OR from:'.join(rules)
            elif _type == "TO_USER":
                rules = 'to:%s' % ' OR to:'.join(rules)
            elif _type == "HASHTAG":
                rules = '%s' % ' OR '.join(rules)
            elif _type == "KEYWORD":
                rules = '%s' % ' OR '.join(rules)

            return [
                {'value': f"sample:{sample} ({rules})",
                 'tag': tag, }
            ]

        api_rules = TwitterQuery(rules_to_set=adding_rule_set)
        if api_rules:
            rules_added = api_rules.rules_found
            update_record(db=db, table="ExpiredAt", column=event,
                          data=get_current_time(future=time_to_live))

            rule_ids_not_in_db = list(rules_added.keys())

            current_rules_in_db = get_from_db(
                db=db, table="StreamingRules", column="Current")

            if not current_rules_in_db:
                current_rules_in_db = {}

            for rule_id in rule_ids_not_in_db:
                update_record(
                    db=db,
                    table='StreamingRules',
                    column=rule_id,
                    data=rules_added[rule_id]
                )

                current_rules_in_db[rule_id] = rules_added[rule_id]

            if rule_ids_not_in_db:
                update_record(db=db, table='StreamingRules',
                              column=event, data=rule_ids_not_in_db)

            update_record(db=db, table='StreamingRules',
                          column="ResetState", data=True)
            return current_rules_in_db
        else:
            return None

    def delete_rules(rule_set_to_delete):
        rule_set = rule_set_to_delete['rule_set']
        event = rule_set_to_delete['event']

        if TwitterAPI(rules_to_delete=rule_set):
            current_rules_in_db = get_from_db(
                db=db, table="StreamingRules", column="Current")
            for rule_id in rule_set:
                delete_record(
                    db=db,
                    table='StreamingRules',
                    field=rule_id
                )
                try:
                    del current_rules_in_db[rule_id]
                except KeyError:
                    pass
            update_record(db=db, table='StreamingRules',
                          column='Current', data=current_rules_in_db)
            delete_record(db=db, table='StreamingRules', field=event)
            delete_record(db=db, table='ExpiredAt', field=event)
            return "success"
        else:
            return None
