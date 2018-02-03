from django.http import HttpResponse

import json


def JsonHttpResponse(request, json_text):
    http_accepts = request.META.get('HTTP_ACCEPT', '').split(',')

    if 'application/json' not in http_accepts:
        # TODO: do something here?
        pass

    if isinstance(json_text, dict):
        json_text = json.dumps(json_text)

    response = HttpResponse(json_text, content_type="application/json; charset=utf-8")
    response['Pragma'] = "no cache"
    response['Cache-Control'] = "no-cache, must-revalidate"
    response['content-length'] = len(json_text)

    return response
