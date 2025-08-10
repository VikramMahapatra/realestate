
def pformat(obj):
    try:
        import json
        return json.dumps(obj, indent=2, default=str)
    except Exception:
        return str(obj)
