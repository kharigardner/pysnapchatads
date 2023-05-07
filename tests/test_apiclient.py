import pytest
import pytest_mock
import requests_mock
import requests

from pysnapchatads.snapchat import SnapchatMarketing
from pysnapchatads.objects.user import User
import typing

# Tests that the method returns a User object. 
def test_get_authenticated_user(requests_mock: requests_mock.Mocker) -> None:
    # Happy path test
    api_client = SnapchatMarketing(access_token='test_token')
    mock_response = {
        'me': 
                {
                    'id': '123', 
                    'updated_at': '2022-01-01T00:00:00.000Z', 
                    'created_at': '2022-01-01T00:00:00.000Z', 
                    'email': 'test@test.com', 
                    'organization_id': '456', 
                    'display_name': 'Test User', 
                    'member_status': 'ACTIVE'
                }
        }
    requests_mock.get('https://adsapi.snapchat.com/v1/me', json=mock_response)

    user = api_client.get_authenticated_user()

    assert isinstance(user, User)
    assert user.id == '123'
    assert user.email == 'test@test.com'
    assert user.display_name == 'Test User'
    assert user.member_status == 'ACTIVE'
    assert user.organization_id == '456'

# Tests that the method returns a list of Organization objects. 
def test_list_organizations(request_mock: requests_mock.Mocker) -> None:
    # Happy path test
    api_client = SnapchatMarketing(access_token='test_token')

    mock_data = {}