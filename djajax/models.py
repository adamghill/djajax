from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models

import json


class SerializableMixin(models.Model):
    def to_json(self):
        '''
        Default dictionary representation of a model that can later be converted to JSON.
        May be overriden in a model by defining `to_json` in the model.
        '''
        serialized_model_str = serializers.serialize('json', [self, ], cls=serializers.json.DjangoJSONEncoder)
        serialized_model = json.loads(serialized_model_str)[0]

        pk = serialized_model.get('pk')
        serialized_model = serialized_model.get('fields')
        serialized_model['pk'] = pk

        return serialized_model

    @staticmethod
    def serialize(queryset_or_model, page_number=1, limit=None):
        '''
        Serializes a queryset/model into JSONifable dictionary.
        TODO: Add this to queryset methods instead of being a static method.

        Example: ```{
            'user': {
                'models': [{'pk': 1, 'email': '', }, ],
                'count': 1,
                'pageNumber': 1,
                'totalCount': 1,
                'perPage': 10,
                'numberOfPages': 1,
                'firstRecordNumber': 1,
                'lastRecordNumber': 1,
            }
        }
        ```
        }
        '''
        queryset = None
        model = None
        queryset_page = None
        count = 0

        if isinstance(queryset_or_model, models.Model):
            # handle just one model being passed in as a queryset
            model = queryset_or_model
            queryset = [model]
        elif isinstance(queryset_or_model, models.query.QuerySet):
            queryset = queryset_or_model
            model = queryset.model

            if limit and limit > 1:
                paginator = Paginator(queryset, limit)

                try:
                    queryset_page = paginator.page(page_number)
                except PageNotAnInteger:
                    queryset_page = paginator.page(1)
                except EmptyPage:
                    queryset_page = paginator.page(paginator.num_pages)

                queryset = queryset_page.object_list
        else:
            raise NotImplementedError()

        content_type = ContentType.objects.get_for_model(model)
        model_name = content_type.name
        serialized_models = [m.to_json() for m in queryset]
        count = len(serialized_models)

        serialized_value = {
            model_name: {
                'models': serialized_models,
                'count': count,
                'pageNumber': 1,
                'totalCount': count,
                'perPage': count,
                'numberOfPages': 1,
                'firstRecordNumber': 0,
                'lastRecordNumber': count,
            }
        }

        if count == 1:
            serialized_value[model_name]['model'] = serialized_models[0]

        if queryset_page:
            first_record_number = (queryset_page.number - 1) * queryset_page.paginator.per_page + 1

            if queryset_page.paginator.count == 0:
                first_record_number = 0

            last_record_number = queryset_page.number * queryset_page.paginator.per_page

            if last_record_number > queryset_page.paginator.count:
                last_record_number = queryset_page.paginator.count

            serialized_value[model_name].update({
                'pageNumber': queryset_page.number,
                'totalCount': queryset_page.paginator.count,
                'perPage': queryset_page.paginator.per_page,
                'numberOfPages': queryset_page.paginator.num_pages,
                'firstRecordNumber': first_record_number,
                'lastRecordNumber': last_record_number,
            })

        return serialized_value

    class Meta:
        app_label = 'djajax'
        abstract = True
