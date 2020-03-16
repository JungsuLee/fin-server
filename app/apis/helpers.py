

def to_json_res(list_res):
    from flask import Response
    import json

    res = json.dumps(list_res, ensure_ascii=False, indent=4).encode('utf8')
    return Response(res, content_type='application/json; charset=utf-8')