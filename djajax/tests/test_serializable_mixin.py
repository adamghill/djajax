from __future__ import unicode_literals

from django.db import models
from django.test import SimpleTestCase, TestCase

from ..models import SerializableMixin


class FakeModel(SerializableMixin):
    name = models.CharField(max_length=10)


class SerializableMixinTestCase(TestCase):
    def setUp(self):
        pass

    def test_model_serialize_model(self):
        model = FakeModel(pk=1, name='fake')

        expected = {
            u'fake model': {
                u'count': 1,
                u'firstRecordNumber': 0,
                u'lastRecordNumber': 1,
                u'model': {
                    u'name': u'fake', u'pk': 1
                },
                u'models': [{
                    u'name': u'fake', u'pk': 1
                }, ],
                u'numberOfPages': 1,
                u'pageNumber': 1,
                u'perPage': 1,
                u'totalCount': 1
            }
        }
        self.assertEqual(expected, model.serialize(model))

    def test_model_serialize_queryset(self):
        self.maxDiff = None
        model_one = FakeModel(name='fake 1')
        model_one.save()

        model_two = FakeModel(name='fake 2')
        model_two.save()

        all_models = FakeModel.objects.filter()

        expected = {
            u'fake model': {
                u'count': 2,
                u'firstRecordNumber': 0,
                u'lastRecordNumber': 2,
                u'models': [{
                    u'name': u'fake 1', u'pk': model_one.pk
                }, {
                    u'name': u'fake 2', u'pk': model_two.pk
                }, ],
                u'numberOfPages': 1,
                u'pageNumber': 1,
                u'perPage': 2,
                u'totalCount': 2
            }
        }
        self.assertEqual(expected, FakeModel.serialize(all_models))


class SerializableMixinSimpleTestCase(SimpleTestCase):
    def setUp(self):
        pass

    def test_model_to_json(self):
        model = FakeModel(pk=1, name='fake')
        expected = {
            u'name': u'fake',
            u'pk': 1
        }
        self.assertEqual(expected, model.to_json())
