# djajax
Some helper utilities for building Ajax applications without throwing out all the nicities of Django out the window (or moving wholesale to something like Django REST Framework).

## Models

### SerializableMixin
A model mixin that gives an easy way to serialize a model or queryset to JSON.

#### to_json
Default dictionary representation of a model that can later be converted to JSON. May be overriden in a model by defining `to_json` in the model.

#### serialize (static method)
Serializes a queryset/model into a JSON-ifable dictionary. Will paginate a queryset if necessary.

## Template tags

### jsonify filter
Outputs a dictionary input a JSON object. Returns an empty obj if the template variable is empty.

```html
<script type="text/javascript">
window.onload = function() {
    (function() {
        var djajaxJsonData = {{ json|jsonify }};
        console.log('djajaxJsonData', djajaxJsonData);
    })();
}();
</script>
```

### djajax_urls tag
Outputs a dictionary of reverse lookups to urls for use in Javascript. Urls must be specified in DJAJAX_URL_REVERSE_LOOKUPS and must not need arguments.

settings.py
```python
DJAJAX_URL_REVERSE_LOOKUPS = [
    'login',
    'www:index',
]
```

index.html
```html
<script src="{% static 'js/djajax.js' %}"></script>

<script type="text/javascript">
window.onload = function() {
    (function() {
        var djajaxUrls = {% djajax_urls %};
        console.log('djajaxUrls', djajaxUrls);
    })();
}();
</script>
```

## HTTP responses

### JsonHttpResponse
Returns a JSON response with the correct headers set.

## View helpers

### is_idempotent
Returns whether the request is idempotent (changes state on the server) or not.

### response
Returns an appropriate AJAX response for an AJAX request.

### get_from_post_or_get
Attempts to first get a value from the POST query dictionary, and if that fails, to look at the GET querystring.
