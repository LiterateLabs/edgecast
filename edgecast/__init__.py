import requests
import json


MEDIA_TYPE_FLASH_MEDIA_STREAMING = 2
"""Flash Media Streaming media type.
"""

MEDIA_TYPE_HTTP_LARGE_OBJECT = 3
"""HTTP Large Object media type.
"""

MEDIA_TYPE_HTTP_SMALL_OBJECT = 8
"""HTTP Small Object media type.
"""

MEDIA_TYPE_APPLICATION_DELIVERY_NETWORK = 14
"""Application Delivery Network media type.
"""

_MEDIA_TYPE_TO_URI_PATH = {
    MEDIA_TYPE_FLASH_MEDIA_STREAMING: 'flash',
    MEDIA_TYPE_HTTP_LARGE_OBJECT: 'httplarge',
    MEDIA_TYPE_HTTP_SMALL_OBJECT: 'httpsmall',
    MEDIA_TYPE_APPLICATION_DELIVERY_NETWORK: 'adn',
}

class EdgeCastError(Exception):
    """EdgeCast communications error.
    """

    pass


class Client(object):
    """EdgeCast CDN client.
    """

    def __init__(self,
                 account_number,
                 token):
        """Initialize an EdgeCast CDN client.

        :param account_number: Account number
        :param token: Token.
        """

        self.account_number = account_number
        self.token = token

        self._session = requests.Session()

    def _request(self,
                 endpoint_method,
                 method,
                 data = None):
        """Perform a request.

        :param endpoint_method: Endpoint method such as ``edge/purge``.
        :param method: Request method.
        :param data: JSON request data.
        """

        response = self._session.request(
            method,
            'https://api.edgecast.com/v2/mcc/customers/%s/%s' % (
                self.account_number,
                endpoint_method,
            ),
            headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': 'TOK:%s' % (self.token),
            },
            data=json.dumps(data) if data else None
        )

        try:
            response.raise_for_status()
        except:
            raise EdgeCastError('unexpected response code %d: %s' % (
                    response.status_code,
                    response.text
                ))

        return response

    def purge(self, media_type, *patterns):
        """Purge one or more resources from the CDN.

        :param media_type: Media type.
        :param \*patterns: CDN URLs or patterns.
        """

        for pattern in patterns:
            self._request('edge/purge',
                          'PUT',
                          {'MediaPath': pattern, 'MediaType': media_type})

    def load(self, media_type, *urls):
        """Load one or more resources into the CDN.

        :param media_type: Media type.
        :param \*urls: URLs from which to load the resources.
        """

        for url in urls:
            self._request('edge/load',
                          'PUT',
                          {'MediaPath': url, 'MediaType': media_type})

    def get_all_customer_origins(self, media_type):
        """This method retrieves all customer origin configurations.

        :param media_type: Media type.
        """

        s_media_type = _MEDIA_TYPE_TO_URI_PATH.get( media_type )
        response = self._request('origins/%s' % s_media_type, 'GET')

        return response.json()

    def add_customer_origin(self, media_type, data):
        """This method adds a customer origin.

        :param media_type: Media type.
        :param data: JSON request data.
        """

        s_media_type = _MEDIA_TYPE_TO_URI_PATH.get( media_type )
        response = self._request('origins/%s' % s_media_type, 'POST', data)

        return response.json()

    def get_all_edge_cnames(self, media_type):
        """This method allows the retrieval of all edge CNAMEs

        :param media_type: Media type.
        """

        s_media_type = _MEDIA_TYPE_TO_URI_PATH.get( media_type )
        response = self._request('cnames/%s' % s_media_type, 'GET')

        return response.json()

    def add_edge_cname(self, media_type, data):
        """This method creates an edge CNAME.

        :param media_type: Media type.
        :param data: JSON request data.
        """

        data['MediaTypeId'] = media_type
        response = self._request('cnames', 'POST', data)

        return response.json()


__all__ = (
    'MEDIA_TYPE_FLASH_MEDIA_STREAMING',
    'MEDIA_TYPE_HTTP_LARGE_OBJECT',
    'MEDIA_TYPE_HTTP_SMALL_OBJECT',
    'MEDIA_TYPE_APPLICATION_DELIVERY_NETWORK',
    'Client',
    'EdgeCastError',
)
