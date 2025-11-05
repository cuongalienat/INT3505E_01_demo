import json
from datetime import date, datetime
from flask.json.provider import DefaultJSONProvider


class JSONEncoder(json.JSONEncoder):
    """Custom JSON Encoder compatible with Connexion 3.x and Flask 3."""

    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


class CustomJSONProvider(DefaultJSONProvider):
    """Custom JSON Provider to use our JSONEncoder."""

    def dumps(self, obj, **kwargs):
        kwargs.setdefault("cls", JSONEncoder)
        return json.dumps(obj, **kwargs)

    def loads(self, s, **kwargs):
        return json.loads(s, **kwargs)
