from __future__ import unicode_literals

from django import template
from django.conf import settings

try:
    from django.urls import reverse
except ImportError:
    # < django 1.10
    from django.core.urlresolvers import reverse

import json

register = template.Library()


@register.filter
def jsonify(val):
    if not val:
        return '{}'

    if not isinstance(val, str):
        val = json.dumps(val)

    return _make_safe(val)


@register.simple_tag(takes_context=True)
def djajax_urls(context):
    # TODO: Cache djajax_urls?
    urls = {
        'requestUrlAndPath': context['request'].get_full_path(),
        'requestPath': context['request'].path,
        'requestMethod': context['request'].method,
    }

    djajax_url_reverse_lookups = []

    if hasattr(settings, 'DJAJAX_URL_REVERSE_LOOKUPS'):
        djajax_url_reverse_lookups = settings.DJAJAX_URL_REVERSE_LOOKUPS

    for reverse_lookup in djajax_url_reverse_lookups:
        url = reverse(reverse_lookup)

        urls.update({
            reverse_lookup: url,
        })

    string_of_urls = json.dumps(urls)

    return _make_safe(string_of_urls)


def _make_safe(val):
    val = template.defaultfilters.safe(val)
    return val
