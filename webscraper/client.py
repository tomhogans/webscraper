#

import urllib
import urllib2
import cookielib
import mimetypes

_USERAGENT_FF3 = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.8) Gecko/20100722 Firefox/3.6.8'

class Session(object):
    """ Implements a web session that handles proxies, cookies, etc. """
    def __init__(self):
        self.cookies = cookielib.FileCookieJar()
        self.cookie_handler = urllib2.HTTPCookieProcessor(self.cookies)
        self.proxy_handler = urllib2.ProxyHandler({})
        self.timeout = 10
        self._build_opener()

    def _build_opener(self):
        handlers = [urllib2.HTTPRedirectHandler(), self.cookie_handler]
        handlers.append(self.proxy_handler)
        self.opener = urllib2.build_opener(*handlers)
        headers = [('User-Agent', _USERAGENT_FF3)]
        self.opener.addheaders = headers

    def set_timeout(self, seconds):
        self.timeout = int(seconds)

    def set_proxy(self, host, port, username=None, password=None):
        if username:
            #TODO: Add proxy auth
            print 'No proxy auth supported'
        proxy_addr = '%s:%s' % (host, port)
        proxy_protocols = {'http': proxy_addr, 'https': proxy_addr}
        self.proxy_handler = urllib2.ProxyHandler(proxy_protocols)
        self._build_opener()

    def get(self, url):
        """ Sends a GET request for the specified URL """
        request = urllib2.Request(url)
        response = self.opener.open(request, timeout=self.timeout)
        return response

    def post(self, url, params):
        """ Sends a POST request to specified URL with included params 

        params: either a URL encoded string or a dictionary """
        if type(params) is not str:
            params = urllib.urlencode(params)
        request = urllib2.Request(url, params)
        response = self.opener.open(request, timeout=self.timeout)
        return response

    def post_multipart(self, url, params, files=None):
        """ Sends a multipart POST request to specified URL 

        params: dictionary or list of names and values
        files: list of (name, filename, value) tuples """
        content_type, params = encode_multipart_formdata(params, files)
        headers = {'Content-Type': content_type}
        request = urllib2.Request(url, params, headers)
        response = self.opener.open(request, timeout=self.timeout)
        return response


def encode_multipart_formdata(fields, files=None):
    """ Encodes data for multipart form POST

    fields: list of (name,value) tuples or dict
    files: optional list of (name, filename, data) tuples 
    
    Taken from: http://code.activestate.com/recipes/146306/ """

    BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
    L = []
    if type(fields) == dict:
        fields = fields.items()
    for (key, value) in fields:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(value)
    if files:
        for (key, filename, value) in files:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
            L.append('Content-Type: %s' % (mimetypes.guess_type(filename)[0] or 'application/octet-stream'))
            L.append('')
            L.append(value)
            L.append('--' + BOUNDARY + '--')
            L.append('')
    body = '\r\n'.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body


if __name__ == '__main__':
    pass
