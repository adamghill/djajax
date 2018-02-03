from django.contrib.contenttypes.models import ContentType

from .http import JsonHttpResponse

import json


def is_idempotent(request):
    if request.method == 'POST' and request.body:
        json_body = {}

        try:
            json_body = json.loads(request.body)
        except:
            pass

        if json_body:
            create_json = json_body.get('create')
            update_json = json_body.get('update')
            delete_json = json_body.get('delete')

            if create_json or update_json or delete_json:
                return False

    return True


def response(request, extra={}):
    if request.is_ajax():
        if request.method == 'GET':
            return get(request, extra=extra)
        elif request.method == 'POST':
            return post(request, extra=extra)
        else:
            raise NotImplementedError('Only GET and POST are supported')


def get(request, extra={}):
    res = {}

    if extra:
        res.update(extra)

    return JsonHttpResponse(request, res)


def _explode_fields(model, model_json):
    '''
    Handles traversing relationships if there are `__` in the JSON key
    '''
    json_dict = {}

    for field in model_json.keys():
        if '__' in field:
            val = model_json[field]
            related_model_field_name = field.split('__')[0]
            RelatedModel = model._meta.get_field(related_model_field_name).related_model

            related_filter = field.replace(related_model_field_name + '__', '')
            related_model = RelatedModel.objects.get(**{related_filter: val})
            json_dict[related_model_field_name] = related_model
        else:
            json_dict[field] = model_json[field]

    return json_dict


def post(request, extra={}):
    res = {}

    if request.body:
        json_body = json.loads(request.body)

        if json_body:
            model_json = json_body.get('model')
            model = _get_model_from_json(model_json)

            create_json = json_body.get('create')
            update_json = json_body.get('update')
            delete_json = json_body.get('delete')

            if create_json:
                create_dict = _explode_fields(model, create_json)
                obj = model(**create_dict)
                obj.save()
            elif update_json:
                filters = model_json.get('filters')
                obj = model.objects.filter(**filters)

                update_dict = _explode_fields(model, update_json)
                obj.update(**update_dict)
            elif delete_json:
                raise NotImplementedError()

            res = {
                'status': 'ok',
            }

    if extra:
        res.update(extra)

    return JsonHttpResponse(request, res)


def _get_model_from_json(model_json):
    app_label = model_json.get('appLabel')
    model_name = model_json.get('name')
    assert app_label is not None, 'App label could not be found'
    assert model_name is not None, 'Model name could not be found'

    content_type = ContentType.objects.get_by_natural_key(app_label, model_name)
    assert content_type is not None, 'Model content type could not be found'

    model = content_type.model_class()
    return model


def get_from_post_or_get(request, key):
    '''
    Helper to get a key from the POST, and if that fails, to look in the GET.
    '''
    return request.POST.get(key, request.GET.get(key))
