__author__ = 'marc'

import httplib
import urlparse

def unshorten_url(url):
    try:
        parsed = urlparse.urlparse(url)
        h = httplib.HTTPConnection(parsed.netloc)
        h.request('HEAD', parsed.path)
        response = h.getresponse()
        if response.status/100 == 3 and response.getheader('Location'):
            redirected = response.getheader('Location')
            if not(redirected.startswith('http')):
                redirected = "%s://%s%s" % (parsed[0], parsed[1], redirected)
            return redirected
        else:
            return url
    except:
        return url
