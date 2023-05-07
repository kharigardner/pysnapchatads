from __future__ import annotations

import datetime as dt
from dateutil import parser as dateparser
import pysnapchatads.base as base
import pysnapchatads.snapchat as snap
import pysnapchatads.objects.ad_accounts as ad_accounts
import typing
import logging

class Organization(base.SnapchatMarketingBase):
    """
    An Organization represents an brand, partner, or ad agency.
    Creation happens via Snap Business Manager UI.

    More information: https://marketingapi.snapchat.com/docs/#organizations
    """

    id: str
    updated_at: dt.datetime
    created_at: dt.datetime
    name: str
    address_line_1: str
    locality: str
    administration_district_level_1: str
    country: str
    postal_code: str
    org_type: str

    def __init__(
        self,
        api_client: snap.SnapchatMarketing,
        id: str,
        updated_at: dt.datetime,
        created_at: dt.datetime,
        name: str,
        address_line_1: str,
        locality: str,
        administration_district_level_1: str,
        country: str,
        postal_code: str,
        org_type: str
    ) -> None:
        super(Organization, self).__init__()
        self.api_client: snap.SnapchatMarketing = api_client
        self.id = id
        self.updated_at = updated_at
        self.created_at = created_at
        self.name = name
        self.address_line_1 = address_line_1
        self.locality = locality
        self.administration_district_level_1 = administration_district_level_1
        self.country = country
        self.postal_code = postal_code
        self.org_type = org_type

    @classmethod
    def from_json(
        cls,
        api_client: snap.SnapchatMarketing,
        json_data: typing.Dict[str, typing.Any]
    ) -> Organization:
        """
        Deserialize JSON data into a Organization object.
        
        :api_client: SnapchatMarketing API object
        :json_data: JSON data
        """
        json_data = json_data['organization']
        logging.info(json_data)

        return Organization(
            api_client=api_client,
            id=json_data['id'],
            updated_at=dateparser.parse(json_data['updated_at']),
            created_at=dateparser.parse(json_data['created_at']),
            name=json_data['name'],
            address_line_1=json_data['address_line_1'],
            locality=json_data['locality'],
            administration_district_level_1=json_data['administration_district_level_1'],
            country=json_data['country'],
            postal_code=json_data['postal_code'],
            org_type=json_data['type']
        )
    
    ################
    # Ad Accounts
    ################

    def list_ad_accounts(self) -> typing.List[ad_accounts.AdAccount]:
        """
        List all ad accounts for this organization.
        """
        response: typing.List[typing.Dict[str, typing.Any]] = self.api_client._get_many_entities(
            plural_parent_entity_name='organizations',
            parent_entity_id=self.id,
            plural_entity_name='adaccounts'
        )

        return [
            ad_accounts.AdAccount.from_json(
                api_client=self.api_client,
                json_data=ad_account
            )
            for ad_account in response
        ]
    
    def create_ad_accounts(
            self,
            json_lists: typing.Optional[typing.List[typing.Dict[str, typing.Any]]] = None,
            **kwargs
    ) -> typing.List[ad_accounts.AdAccount]:
        """
        Create ad accounts for this organization.
        """
        
        if json_lists is None and not kwargs:
            raise ValueError('Must provide either json_lists or keyword attributes of a single AdAccount')
        if json_lists and kwargs:
            raise ValueError('Must provide either json_lists or keyword attributes of a single AdAccount')
        

        if json_lists is not None:
            responze = self.api_client._create_entities(
                plural_parent_entity_name='organizations',
                parent_entity_id=self.id,
                plural_entity_name='adaccounts',
                data=json_lists
            )
        
        else:
            responze = self.api_client._create_entities(
                plural_parent_entity_name='organizations',
                parent_entity_id=self.id,
                plural_entity_name='adaccounts',
                data=[kwargs]
            )
        
        return [
                ad_accounts.AdAccount.from_json(
                    api_client=self.api_client,
                    json_data=ad_account
                ) for ad_account in responze
            ]