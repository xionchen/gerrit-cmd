# The MIT License
#
# Copyright 2013 Sony Mobile Communications. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

""" Interface to the Gerrit REST API. """

import json
import logging
import requests

GERRIT_MAGIC_JSON_PREFIX = ")]}\'\n"
GERRIT_AUTH_SUFFIX = "/a"


def _decode_response(response):
    """ Strip off Gerrit's magic prefix and decode a response.

    :returns:
        Decoded JSON content as a dict, or raw text if content could not be
        decoded as JSON.

    :raises:
        requests.HTTPError if the response contains an HTTP error status code.

    """
    content = response.content.strip()
    logging.debug(content[:512])
    response.raise_for_status()
    if content.startswith(GERRIT_MAGIC_JSON_PREFIX):
        content = content[len(GERRIT_MAGIC_JSON_PREFIX):]
    try:
        return json.loads(content)
    except ValueError:
        logging.error('Invalid json content: %s' % content)
        raise

class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance

class GerritRestAPI(Singleton):

    """ Interface to the Gerrit REST API.

    :arg str url: The full URL to the server, including the `http(s)://` prefix.
        If `auth` is given, `url` will be automatically adjusted to include
        Gerrit's authentication suffix.
    :arg auth: (optional) Authentication handler.  Must be derived from
        `requests.auth.AuthBase`.
    :arg boolean verify: (optional) Set to False to disable verification of
        SSL certificates.

    """

    def __init__(self, url, auth=None, verify=True):
        headers = {'Accept': 'application/json',
                   'Accept-Encoding': 'gzip'}
        self.kwargs = {'auth': auth,
                       'verify': verify,
                       'headers': headers}
        self.url = url.rstrip('/')

        if auth:
            if not isinstance(auth, requests.auth.AuthBase):
                raise ValueError('Invalid auth type; must be derived '
                                 'from requests.auth.AuthBase')

            if not self.url.endswith(GERRIT_AUTH_SUFFIX):
                self.url += GERRIT_AUTH_SUFFIX
        else:
            if self.url.endswith(GERRIT_AUTH_SUFFIX):
                self.url = self.url[: - len(GERRIT_AUTH_SUFFIX)]

        if not self.url.endswith('/'):
            self.url += '/'
        logging.debug("url %s", self.url)

    def make_url(self, endpoint):
        """ Make the full url for the endpoint.

        :arg str endpoint: The endpoint.

        :returns:
            The full url.

        """
        endpoint = endpoint.lstrip('/')
        return self.url + endpoint

    def get(self, endpoint, **kwargs):
        """ Send HTTP GET to the endpoint.

        :arg str endpoint: The endpoint to send to.

        :returns:
            JSON decoded result.

        :raises:
            requests.RequestException on timeout or connection error.

        """
        kwargs.update(self.kwargs.copy())
        response = requests.get(self.make_url(endpoint), **kwargs)
        return _decode_response(response)

    def put(self, endpoint, **kwargs):
        """ Send HTTP PUT to the endpoint.

        :arg str endpoint: The endpoint to send to.

        :returns:
            JSON decoded result.

        :raises:
            requests.RequestException on timeout or connection error.

        """
        kwargs.update(self.kwargs.copy())
        if "data" in kwargs:
            kwargs["headers"].update(
                {"Content-Type": "application/json;charset=UTF-8"})
        response = requests.put(self.make_url(endpoint), **kwargs)
        return _decode_response(response)

    def post(self, endpoint, **kwargs):
        """ Send HTTP POST to the endpoint.

        :arg str endpoint: The endpoint to send to.

        :returns:
            JSON decoded result.

        :raises:
            requests.RequestException on timeout or connection error.

        """
        kwargs.update(self.kwargs.copy())
        if "data" in kwargs:
            kwargs["headers"].update(
                {"Content-Type": "application/json;charset=UTF-8"})
        response = requests.post(self.make_url(endpoint), **kwargs)
        return _decode_response(response)

    def delete(self, endpoint ,**kwargs):
        """ Send HTTP DELETE to the endpoint.

        :arg str endpoint: The endpoint to send to.

        :returns:
            JSON decoded result.

        :raises:
            requests.RequestException on timeout or connection error.

        """
        kwargs.update(self.kwargs.copy())
        response = requests.delete(self.make_url(endpoint), **kwargs)
        return _decode_response(response)



