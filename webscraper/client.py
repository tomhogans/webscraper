#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Provides functionality to mimic HTTP session """

import urllib
import urllib2
import cookielib
import mimetypes

_USERAGENT_FF3 = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.' \
        '1.8) Gecko/20100722 Firefox/3.6.8'


class Session(object):
    """ Implements a web session that handles proxies, cookies, etc. """
    def __init__(self):
        self.cookies = cookielib.FileCookieJar()
        self.cookie_handler = urllib2.HTTPCookieProcessor(self.cookies)
        self.proxy_handler = None
        self.proxy_auth = None
        self.timeout = 10
        self._build_opener()

    def _build_opener(self):
        handlers = [urllib2.HTTPRedirectHandler(), self.cookie_handler]
        if self.proxy_handler:
            handlers.append(self.proxy_handler)
        if self.proxy_auth:
            handlers.append(self.proxy_auth)
        self.opener = urllib2.build_opener(*handlers)
        headers = [('User-Agent', _USERAGENT_FF3)]
        self.opener.addheaders = headers

    def set_timeout(self, seconds):
        self.timeout = int(seconds)

    def set_proxy(self, host, port, username=None, password=None):
        proxy_addr = '{0}:{1}'.format(host, port)
        proxy_protocols = {'http': proxy_addr, 'https': proxy_addr}
        if not host:
            self.proxy_handler = None
            self.proxy_auth = None
            return
        if username:
            passmgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
            passmgr.add_password(None, 'http://{0}'.format(proxy_addr), 
                    username, password)
            self.proxy_auth = urllib2.ProxyBasicAuthHandler(passmgr)
        else:
            self.proxy_auth = False
        self.proxy_handler = urllib2.ProxyHandler(proxy_protocols)
        self._build_opener()

    def get(self, url, headers=None):
        """ Sends a GET request for the specified URL 
        
        headers: a list of (key, value) tuples of one-time headers """
        request = urllib2.Request(url)
        if headers:
            for header, value in headers:
                request.add_header(header, value)
        response = self.opener.open(request, timeout=self.timeout)
        return response

    def post(self, url, params, headers=None):
        """ Sends a POST request to specified URL with included params

        params: either a URL encoded string or a dictionary 
        headers: a list of (key, value) tuples of one-time headers """
        if type(params) is not str:
            params = urllib.urlencode(params)
        request = urllib2.Request(url, params)
        if headers:
            for header, value in headers:
                request.add_header(header, value)
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

    def generate_boundary():
        return '----------DjshEfhAcVyueShrAltuN'

    boundary = generate_boundary()
    L = [ ]
    if type(fields) == dict:
        fields = fields.items()
    for (key, value) in fields:
        L.append('--{0}'.format(boundary))
        L.append('Content-Disposition: form-data; name="{0}"'.format(key))
        L.append('')
        L.append(value)
    if files:
        for (key, filename, value) in files:
            L.append('--%s' % boundary)
            header = 'Content-Disposition: form-data; name="{0}"; filename' \
                    '="{1}"'.format(key, filename)
            L.append(header)
            t = mimetypes.guess_type(filename)[0]
            L.append('Content-Type: {0}'.format(
                (t or 'application/octet-stream')))
            L.append('')
            L.append(value)
    L.append('--{0}--'.format(boundary))
    L.append('')
    body = '\r\n'.join(L)
    content_type = 'multipart/form-data; boundary={0}'.format(boundary)
    return content_type, body


