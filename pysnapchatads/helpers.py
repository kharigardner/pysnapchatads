from urllib.parse import urljoin
import typing
import requests
def build_url(base_url: str, endpoint: str, path: typing.Optional[str] = None ) -> str:
    
    url_result: str = urljoin(base_url, endpoint)

    if path:
        # Ensure the endpoint has a trailing slash
        if not url_result.endswith('/'):
            url_result += '/'

        # Ensure the path doesn't have a leading slash
        if path.startswith('/'):
            path = path[1:]

        url_result: str = urljoin(url_result, path) # type: ignore

    return url_result

def refresh_access_token(
        client_id: str,
        client_secret: str,
        refresh_token: str
) -> str:
    """
    Helper function to refresh an access token.
    """

    URL = 'https://accounts.snapchat.com/login/oauth2/access_token'
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }

    response = requests.post(url=URL, data=data)

    return response.json()['access_token']