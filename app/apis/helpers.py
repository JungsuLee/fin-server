

def to_json_res(list_res):
    from flask import Response
    import json

    res = json.dumps(list_res, ensure_ascii=False, indent=4).encode('utf8')
    return Response(res, content_type='application/json; charset=utf-8')
    


def get_start_end_dates(year):
    import datetime
    start_date = datetime.datetime.strptime(
            '01-01-' + year + ' 00:00:00', '%m-%d-%Y %H:%M:%S')
    end_date = datetime.datetime.strptime(
        '12-31-' + year + ' 23:59:59', '%m-%d-%Y %H:%M:%S')
    return start_date, end_date