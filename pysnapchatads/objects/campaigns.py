from __future__ import annotations

import datetime as dt
from dateutil import parser as dateparser
import pysnapchatads.base as base
import pysnapchatads.snapchat as snap
import pysnapchatads.objects.ad_squads as ad_squads
import typing
import typing_extensions
import logging
import types

class Campaign(base.SnapchatMarketingBase):
    """
    A campaign represents a Snap campaign.
    """
    
    ad_account_id: str
    daily_budget_micro: typing.Optional[typing.Union[int, float]]
    end_time: dt.datetime
    name: str
    start_time: dt.datetime
    status: str
    lifetime_spend_cap_micro: typing.Optional[typing.Union[int, float]]
    measurement_spec: typing.Optional[typing.Dict[str, typing.Any]]
    objective: typing.Optional[str]
    buy_model: typing.Optional[str]
    regulations: typing.Optional[typing.Dict[str, typing.Any]]
    delivery_status: typing.Optional[str]
    """Read only."""
    deleted: typing.Optional[bool]

    def __init__(
        self,
        api_client: snap.SnapchatMarketing,
        **kwargs
    ) -> None:
        super(Campaign, self).__init__()
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
        json_data: typing.Dict[str, typing.Any],
        **kwargs
    ) -> Campaign:
        """
        Deserialize a JSON into a campaign object.
        
        :param api_client: SnapchatMarketing API object
        :param json_data: JSON data

        :return: Campaign
        """

        return Campaign(api_client=api_client, **json_data)
    
    def update(
            self,
            name: typing.Optional[str] = None,
            status: typing.Optional[str] = None,
            start_time: typing.Optional[typing.Union[str, dt.datetime]] = None,
            lifetime_spend_cap_micro: typing.Optional[typing.Union[int, float, str]] = None,
            daily_budget_micro: typing.Optional[typing.Union[int, float, str]] = None,
            end_time: typing.Optional[typing.Union[str, dt.datetime]] = None
    ) -> None:
        """
        Update a campaign.
        
        More information: https://marketingapi.snapchat.com/docs/#update-a-campaign
        """

        if name:
            self.name = name
        if status:
            self.status = status
        if start_time:
            self.start_time = dateparser.parse(start_time) if isinstance(start_time, str) else start_time
        if lifetime_spend_cap_micro:
            self.lifetime_spend_cap_micro = float(lifetime_spend_cap_micro)
        if daily_budget_micro:
            self.daily_budget_micro = float(daily_budget_micro)
        if end_time:
            self.end_time = dateparser.parse(end_time) if isinstance(end_time, str) else end_time
        
        self.api_client._update_entities(
            plural_parent_entity_name='adaccounts',
            parent_entity_id=self.ad_account_id,
            plural_entity_name='campaigns',
            data=[self.__dict__()]
        )
    
    def delete(self) -> None:
        """
        Delete a campaign.
        """
        self.api_client._delete_entity(
            plural_entity_name='campaigns',
            entity_id=self.ad_account_id
        )

    #################
    # Ad Squads
    #################

    def list_ad_squads(
            self,
            return_placement_v2: typing.Optional[bool] = True
    ) -> typing.List[ad_squads.AdSquad]:
        """
        List ad squads under this campaign.
        """
        data_response: typing.List[typing.Dict[str, typing.Any]] = self.api_client._get_many_entities(
            plural_parent_entity_name='campaigns',
            parent_entity_id=str(self.id),
            plural_entity_name='adsquads',
            return_placement_v2=return_placement_v2
        )

        return [ad_squads.AdSquad.from_json(self.api_client, x) for x in data_response]
    
    def create_ad_squad(
            self,
            bid_micro: typing.Union[float, str, int],
            billing_event: str,
            name: str,
            optimization_goal: str,
            placement_v2: typing.Dict[str, typing.Any],
            targeting: typing.Dict[str, typing.Any],
            ad_squad_type: str,
            bid_strategy: str,
            reach_goal: typing.Any,
            impression_goal: typing.Any,
            reach_and_frequency_status: str = 'PENDING',
            roas_value_micro: typing.Optional[typing.Union[float, str, int]] = None,
            daily_budget_micro: typing.Optional[typing.Union[float, str, int]] = None,
            lifetime_budget_micro: typing.Optional[typing.Union[float, str, int]] = None,
            **kwargs
    ) -> ad_squads.AdSquad:
        """
        Create an ad squad under this campaign.
        """
        VALID_KWARGS: typing.List[str] = [
            'child_ad_type',
            'forced_view_setting',
            'end_time',
            'start_time',
            'status',
            'story_ad_creative_type',
            'cap_and_exclusion_config',
            'ad_scheduling_config',
            'pixel_id',
            'measurement_provider_names',
            'pacing_type',
            'event_sources'
        ]
        
        post_data: typing.Dict[str, typing.Any] = {
            'campaign_id': self.id,
            'bid_micro': bid_micro,
            'billing_event': billing_event,
            'name': name,
            'optimization_goal': optimization_goal,
            'placement_v2': placement_v2,
            'targeting': targeting,
            'ad_squad_type': ad_squad_type,
            'bid_strategy': bid_strategy,
            'reach_goal': reach_goal,
            'impression_goal': impression_goal,
            'reach_and_frequency_status': reach_and_frequency_status,
            'roas_value_micro': roas_value_micro,
            'daily_budget_micro': daily_budget_micro,
            'lifetime_budget_micro': lifetime_budget_micro
        }

        for k,v in kwargs.items():
            if k not in VALID_KWARGS:
                logging.warn(f'{k} is not a valid attribute to create an ad squad. Skipping.')
                continue
            else:
                post_data[k] = v

        response_data: typing.List[typing.Dict[str, typing.Any]] = self.api_client._create_entities(
            plural_parent_entity_name='campaigns',
            parent_entity_id=str(self.id),
            plural_entity_name='adsquads',
            data=[post_data]
        )

        return ad_squads.AdSquad.from_json(self.api_client, response_data[0])
    

    ################
    # General
    ################

    def __dict__(self) -> typing.Dict[str, typing.Any]: # type: ignore
        return {
            'ad_account_id': self.ad_account_id,
            'daily_budget_micro': self.daily_budget_micro,
            'end_time': self.end_time,
            'name': self.name,
            'start_time': self.start_time,
            'status': self.status,
            'lifetime_spend_cap_micro': self.lifetime_spend_cap_micro,
            'measurement_spec': self.measurement_spec,
            'objective': self.objective,
            'buy_model': self.buy_model,
            'regulations': self.regulations,
            'delivery_status': self.delivery_status,
            'deleted': self.deleted
        }
    
    