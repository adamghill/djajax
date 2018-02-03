# djajax
Some helper utilities for building Ajax applications without throwing out all the nicities of Django out the window (or moving wholesale to something like Django REST Framework).

## SerializableMixin
A model mixin that gives an easy way to serialize a model or queryset to JSON.

## Template tags

### jsonify filter
Outputs an empty obj if nothing there and calls safe on the JSON string text.

### djajax_urls tag
Outputs a dictionary of reverse lookups to urls for use in Javascript. Url must not need arguments, and DJAJAX_URL_REVERSE_LOOKUPS needs to be set in settings for security reasons.
