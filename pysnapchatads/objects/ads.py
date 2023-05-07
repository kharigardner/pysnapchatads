from __future__ import annotations

import datetime as dt
from dateutil import parser as dateparser
import pysnapchatads.base as base
import pysnapchatads.snapchat as snap
import typing
import typing_extensions
import logging
import types

class Ad(base.SnapchatMarketingBase):
    """
    Ad is a light weight entity that contains all the information needed to display the ad. 
    It also contains a third party measurement URL if needed.

    More information: https://marketingapi.snapchat.com/docs/#ads
    """

    ad_squad_id: str
    creative_id: str
    name: str

    paying_advertiser_name: typing.Optional[str]
    """Inherited & Immutable"""

    review_status: typing.Optional[str]
    """Read only."""
    review_status_reasons: typing.Optional[typing.Any]
    """Read only."""

    status: str
    ad_type: str
    delivery_status: typing.Any
    """Read only."""
    deleted: typing.Optional[bool]
    """Read only."""