from server.lib.objects.cache import redis_cache
from server.lib.objects.database import DatabaseObject
from server.lib.adapters.MongoDB import MongoDB


class ConsensusResponse:
    status_code = 200
    message = None
    error = None
    data = None
    mongo_db = DatabaseObject(database_adapter=MongoDB())

    cache_key = None
    db_key = None
    api_endpoint = None

    def __init__(self):
        pass

    def return_bad_request(self, req):
        response_body = req.response

        self.status_code = response_body["code"]
        self.message = response_body["message"]
        self.error = response_body["error"]

        return self.create_response()

    def fufill_request(self, req):
        cache_key = self.cache_key(req)
        db_key = self.db_key(req)

        if cache_key and redis_cache.exists(key=cache_key):
            cached_data = redis_cache.get(cache_key)
            if cached_data is not None:
                self.status_code = 200
                self.message = "Success"
                self.data = cached_data
                return self.create_response()

        elif self.mongo_db.entry_exists(db_key):

            db_data = self.mongo_db.get(db_key)
            if db_data is not None:
                self.status_code = 200
                self.message = "Success"
                self.data = db_data
                return self.create_response()

        else:

            fufilled_request = self.api_endpoint(req)
            if fufilled_request.expected_status_code != 200:
                return self.return_bad_request(req=fufilled_request)

            else:
                if cache_key:
                    redis_cache.set(key=cache_key, value=fufilled_request.data)
                if db_key:
                    self.mongo_db.set(db_key, fufilled_request.data)

                self.status_code = 200
                self.message = "Success"
                self.data = fufilled_request.data
                return self.create_response()

    def create_response(self):

        if self.status_code != 200:

            return {
                "status": self.status_code,
                "message": self.message,
                "error": self.error,
            }

        else:

            return {
                "status": self.status_code,
                "message": self.message,
                "data": self.data,
            }
