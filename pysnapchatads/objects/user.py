from __future__ import annotations

import datetime as dt
from dateutil import parser as dateparser
import pysnapchatads.base as base
import pysnapchatads.snapchat as snap
import typing
import logging

class Bitmoji(typing.TypedDict):
    """
    Represents a Bitmoji account.
    """

    avatar_id: str
    selfie_id: str
    background_id: str
    scene_id: str

    
class User(base.SnapchatMarketingBase):
    """
    This endpoint retrieves information about the Snapchat user that is represented by 
    the access token used, the information includes the snapchat_username.

    More information: https://marketingapi.snapchat.com/docs/#user
    """

    id: str
    updated_at: dt.datetime
    created_at: dt.datetime
    email: str
    organization_id: str
    display_name: str
    member_status: str

    user_bitmoji: typing.Optional[Bitmoji]

    def __init__(
            self,
            api_client: snap.SnapchatMarketing,
            id: str,
            updated_at: dt.datetime,
            created_at: dt.datetime,
            email: str,
            organization_id: str,
            display_name: str,
            member_status: str,
            user_bitmoji: typing.Optional[Bitmoji] = None
    ) -> None:
        super(User, self).__init__()
        self.api_client: snap.SnapchatMarketing = api_client
        self.id = id
        self.updated_at = updated_at
        self.created_at = created_at
        self.email = email
        self.organization_id = organization_id
        self.display_name = display_name
        self.member_status = member_status

        if user_bitmoji:
            self.user_bitmoji = user_bitmoji

    @classmethod
    def from_json(
        cls,
        api_client: snap.SnapchatMarketing,
        json_data: typing.Dict[str, typing.Any]
    ) -> User:
        """
        Deserialize JSON data into a User object.
        
        :api_client: SnapchatMarketing API object
        :json_data: JSON data
        """

        user = User(
            api_client=api_client,
            id=json_data['id'],
            updated_at=dateparser.parse(json_data['updated_at']),
            created_at=dateparser.parse(json_data['created_at']),
            email=json_data['email'],
            organization_id=json_data['organization_id'],
            display_name=json_data['display_name'],
            member_status=json_data['member_status']
        )

        if 'bitmoji' in json_data:
            user.user_bitmoji = Bitmoji(
                            avatar_id=json_data['bitmoji']['avatar_id'],
                            selfie_id=json_data['bitmoji']['selfie_id'],
                            background_id=json_data['bitmoji']['background_id'],
                            scene_id=json_data['bitmoji']['scene_id']
                        )
            
        return user
    
    