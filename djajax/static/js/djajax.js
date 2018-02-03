function djajaxInit(djajaxUrls) {
  // Set a nicer `getUrl` function on the djajaxUrls object
  if (djajaxUrls != undefined) {
    djajaxUrls['getUrl'] = function(lookup) {
      if (this[lookup] == undefined) {
        var err = 'Invalid url reverse lookup: "' + lookup + '"';
        throw err
      }

      return this[lookup];
    }
  }
}

function getCsrfValue() {
  var csrfValue = document.getElementsByName('csrfmiddlewaretoken')[0].value;

  if (!csrfValue) {
    throw Error('Missing CSRF input')
  }

  return csrfValue;
}

function print(str, obj) {
  if (obj != undefined) {
    console.log(str, obj);
  } else {
    console.log(str);
  }
}

function getCurrentUrl() {
  var url = window.location.href;
  return url;
}
