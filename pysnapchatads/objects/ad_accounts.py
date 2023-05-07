from __future__ import annotations

import datetime as dt
from dateutil import parser as dateparser
import pysnapchatads.base as base
import pysnapchatads.snapchat as snap
import pysnapchatads.objects.campaigns as campaigns
import pysnapchatads.objects.ad_squads as ad_squads
import typing
import typing_extensions
import logging
import types

class AdAccount(base.SnapchatMarketingBase):
    """
    An Ad Account is owned by an Organization and contains Ad Campaigns.
    Ad Accounts have one or more Funding Sources(Credit card, Paypal, Lines of Credit etc).

    More information: https://marketingapi.snapchat.com/docs/#ad-accounts
    """

    advertiser: str
    currency: str
    funding_source_ids: typing.List[str]
    billing_type: str
    name: str
    organization_id: str
    
    test: typing.Optional[bool]
    timezone: typing.Union[dt.tzinfo, str]
    account_type: str
    
    lifetime_spend_cap_micro: typing.Optional[typing.Union[int, float]]
    advertiser_organization_id: typing.Optional[str]
    """Read only."""
    paying_advertiser_name: typing.Optional[str]
    regulations: typing.Optional[types.MappingProxyType[str, typing.Union[str, bool]]]
    """Immutable once set."""  # dont you wish there was a fucking frozen dict like that wasnt this?!
    agency_representing_client: bool
    client_based_in_country: typing.Optional[str]
    client_paying_invoices: typing.Optional[bool]
    agency_client_metadata: typing.Optional[typing.Dict[typing.Any, typing.Any]]
    delivery_status: typing.Optional[typing.Any]

    def __init__(
        self,
        api_client: snap.SnapchatMarketing,
        **kwargs
    ) -> None:
        super(AdAccount, self).__init__()
        self.api_client: snap.SnapchatMarketing = api_client
        
        # validate kwargs
        for k,v in kwargs.items():
            if k not in self.__class__.__annotations__.keys():
                raise AttributeError(f'{k} is not a valid attribute for {self.__class__.__name__}')
            else:
                setattr(self, k, v)

    @classmethod
    def from_json(
        cls,
        api_client: snap.SnapchatMarketing,
        json_data: typing.Dict[str, typing.Any]
    ) -> AdAccount:
        """
        Deserialize JSON data into a Ad Account object.
        
        :api_client: SnapchatMarketing API object
        :json_data: JSON data
        """
        json_data['account_type'] = json_data.pop('type')

        # make sure the type key was removed
        if 'type' in json_data:
            del json_data['type']
        
        return AdAccount(api_client=api_client, **json_data)
    

    def update(
        self,
        **kwargs
    ) -> None:
        """
        Update the Ad Account.
        """

        UPDATABLE_FIELDS = [
            'name',
            'advertiser',
            'billing_center_id',
            'lifetime_spend_cap_micro',
            'agency_representing_client',
            'paying_advertiser_name',
            'client_paying_invoices',
            'client_based_in_country',
            'agency_client_metadata'
        ]

        for k,v in kwargs.items():
            if k not in UPDATABLE_FIELDS:
                raise AttributeError(f'{k} is not a valid attribute for {self.__class__.__name__}')
            else:
                setattr(self, k, v)

        self.api_client._update_entities(
            plural_parent_entity_name = 'organizations',
            parent_entity_id = self.organization_id,
            plural_entity_name ='adaccounts',
            data = [super(AdAccount, self).__dict__()]
        )

    
    ###############
    # Campaigns
    ###############

    def list_campaigns(
            self,
            read_deleted_entities: typing.Optional[bool] = True
    ) -> typing.List[campaigns.Campaign]:
        """
        List all Ad Campaigns for an Ad Account.
        """

        response_data: typing.List[typing.Dict[str, typing.Any]] = self.api_client._get_many_entities(
            plural_parent_entity_name='adaccounts',
            parent_entity_id=str(self.id),
            plural_entity_name='campaigns',
            read_deleted_entities=read_deleted_entities
        )

        return [campaigns.Campaign.from_json(self.api_client, d) for d in response_data]
    
    def create_campaign(
            self,
            name: str,
            ad_account_id: str,
            start_time: typing.Union[dt.datetime, str],
            status: str,
            **kwargs
    ) -> campaigns.Campaign:
        """
        Create a campaign.
        """
        VALID_KWARGS = [
            "daily_budget_micro",
            "end_time",
            "lifetime_spend_cap_micro",
            "measurement_spec",
            "objective",
            "buy_model",
            "regulations"
        ]
        
        campaign_post_body = {
            'name': name,
            'ad_account_id': ad_account_id,
            'start_time': start_time.isoformat() if isinstance(start_time, dt.datetime) else start_time,
            'status': status
        }

        for k,v in kwargs.items():
            if k not in VALID_KWARGS:
                logging.warn(f'{k} is not a valid attribute for a Campaign object. Skipping to avoid exception.')
                continue
            else:
                campaign_post_body[k] = v
        
        return_data = self.api_client._create_entities(
            plural_parent_entity_name='adaccounts',
            parent_entity_id=str(self.id),
            plural_entity_name='campaigns',
            data = [campaign_post_body]
        )

        return campaigns.Campaign.from_json(self.api_client, return_data[0])
    
    
    ##############
    # Ad Squads
    ##############

    def list_ad_squads(
            self,
            return_placement_v2: typing.Optional[bool] = True,
            read_deleted_entities: typing.Optional[bool] = True
    ) -> typing.List[ad_squads.AdSquad]:
        """
        List all Ad Squads for an Ad Account.
        """

        response_data: typing.List[typing.Dict[str, typing.Any]] = self.api_client._get_many_entities(
            plural_parent_entity_name='adaccounts',
            parent_entity_id=str(self.id),
            plural_entity_name='adsquads',
            read_deleted_entities=read_deleted_entities,
            return_placement_v2=return_placement_v2
        )

        return [ad_squads.AdSquad.from_json(self.api_client, d) for d in response_data]