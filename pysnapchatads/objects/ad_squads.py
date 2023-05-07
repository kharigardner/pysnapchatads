from __future__ import annotations

import datetime as dt
from dateutil import parser as dateparser
import pysnapchatads.base as base
import pysnapchatads.snapchat as snap
import typing
import typing_extensions
import logging
import types

class AdSquad(base.SnapchatMarketingBase):
    """
    An Ad Squad is owned by a Campaign and contains one or more Ads.

    More info: https://marketingapi.snapchat.com/docs/#ad-squads
    """

    campaign_id: str
    bid_micro: typing.Union[float, int, str]
    billing_event: str
    child_ad_type: typing.Optional[str]
    forced_view_setting: typing.Optional[str]
    
    daily_budget_micro: typing.Optional[typing.Union[float, int, str]]
    """This or lifetime_budget_micro must be set."""
    lifetime_budget_micro: typing.Optional[typing.Union[float, int, str]]
    """This or daily_budget_micro must be set."""

    end_time: typing.Optional[dt.datetime]
    
    name: str
    optimization_goal: str
    placement_v2: typing.Dict[str, typing.Any]
    
    start_time: typing.Optional[dt.datetime]
    status: typing.Optional[str]

    story_ad_creative_type: typing.Optional[str]

    targeting: typing.Any
    adsquad_type: typing.Optional[str]

    cap_and_exclusion_config: typing.Any
    bid_strategy: typing.Optional[str]
    roas_value_micro: typing.Optional[typing.Union[float, int, str]]
    """Required when bid_strategy is set to MIN_ROAS."""

    pixel_id: typing.Optional[str]
    measurement_provider_names: typing.Optional[typing.Union[str, typing.List[str]]]

    reach_and_frequency_status: typing.Optional[str]
    delivery_constraint: typing.Optional[str]

    reach_goal: typing.Union[float, int, str]
    impression_goal: typing.Union[float, int, str]

    pacing_type: typing.Optional[str]
    event_sources: typing.Optional[typing.List[str]]
    """Required when in SKAdnetwork."""

    skadnetwork_properties: typing.Optional[typing.Dict[str, typing.Any]]
    """Read-only."""
    deleted: typing.Optional[bool]
    """Read-only."""
    separated_types: typing.Optional[typing.Dict[str, typing.Any]]
    """Read-only."""

    def __init__(
        self,
        api_client: snap.SnapchatMarketing,
        **kwargs
    ) -> None:
        super(AdSquad, self).__init__()
        self.api_client: snap.SnapchatMarketing = api_client
        
        for k, v in kwargs.items():
            if k not in self.__class__.__annotations__.keys():
                raise AttributeError(f'{k} is not a valid attribute for {self.__class__.__name__}')
            else:
                setattr(self, k, v)
        
    @classmethod
    def from_json(
        cls,
        api_client: snap.SnapchatMarketing,
        json_data: typing.Dict[str, typing.Any]
    ) -> AdSquad:
        """
        Deserialize a JSON object into a class instance.
        """
        return cls(
                    api_client=api_client,
                    **json_data
                )
    
    def update(
        self,
        bid_strategy: typing.Optional[str] = None,
        bid_micro: typing.Optional[typing.Union[float, int, str]] = None,
        roas_value_micro: typing.Optional[typing.Union[float, int, str]] = None,
        daily_budget_micro: typing.Optional[typing.Union[float, int, str]] = None,
        lifetime_budget_micro: typing.Optional[typing.Union[float, int, str]] = None,
        end_time: typing.Optional[dt.datetime] = None,
        name: typing.Optional[str] = None,
        status: typing.Optional[str] = None,
        targeting: typing.Optional[typing.Dict[str, typing.Any]] = None,
        pixel_id: typing.Optional[str] = None,
        cap_and_exclusion_config: typing.Optional[typing.Dict[str, typing.Any]] = None,
        included_content_types: typing.Optional[typing.List[str]] = None,
        excluded_content_types: typing.Optional[typing.List[str]] = None,
        pacing_type: typing.Optional[str] = None
    ) -> None:
        """
        Update an Ad Squad.
        
        More information: https://marketingapi.snapchat.com/docs/#update-an-ad-squad
        """

        if bid_strategy:
            self.bid_strategy = bid_strategy
        
        if bid_micro:
            self.bid_micro = bid_micro
        
        if roas_value_micro:
            self.roas_value_micro = roas_value_micro
        
        if daily_budget_micro:
            self.daily_budget_micro = daily_budget_micro
        
        if lifetime_budget_micro:
            self.lifetime_budget_micro = lifetime_budget_micro
        
        if end_time:
            self.end_time = end_time
        
        if name:
            self.name = name
        
        if status:
            self.status = status
        
        if targeting:
            self.targeting = targeting

        if pixel_id:
            self.pixel_id = pixel_id
        
        if cap_and_exclusion_config:
            self.cap_and_exclusion_config = cap_and_exclusion_config
        
        if included_content_types:
            self.included_content_types = included_content_types
        
        if excluded_content_types:
            self.excluded_content_types = excluded_content_types
        
        if pacing_type:
            self.pacing_type = pacing_type

        self.api_client._update_entities(
            plural_parent_entity_name='campaigns',
            parent_entity_id=self.campaign_id,
            plural_entity_name='adsquads',
            data=[self.__dict__()]
        )
        
    
    def __dict__(self) -> typing.Dict[str, typing.Any]: # type: ignore
        
        return {
            k: getattr(self, k)
            for k in self.__class__.__annotations__.keys() \
            if k != 'api_client'
        }