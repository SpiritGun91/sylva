import json
import re
from typing import Dict, List

import pandas as pd
import requests

from ..__init__ import __user_agent__
from ..config import config
from ..helpers.helpers import RequestError, IncompatibleQueryType
from ..collector import Collector
from .intelxapi import IntelX_API


class IntelX:
    def __init__(self, collector:Collector):
        self.__api_url:str = 'https://3.intelx.io'
        self.__debug_disable_tag:str = 'intelx'
        self.__base_headers:Dict[str, str] = {
            'X-Key': config['Keys']['intelx-key'],
            'User-Agent': __user_agent__,
        }
        self.source_obtain_keys_url:str = 'https://intelx.io/account?tab=developer'
        self.source_name:str = 'IntelX'
        self.collector:Collector = collector
    def search(self, query:str, limit:int=2, buckets=["leaks.public", "leaks.private", "pastes", "darknet"], timeout:int=5, datefrom:str=None, dateto:str=None, sort:int=2, media:int=24, terminate=[]) -> pd.DataFrame:
        if (
            self.__debug_disable_tag in config['Debug']['disabled_modules']
            or not config['Keys']['intelx-key']
        ):
            return
        intelxapi = IntelX_API(key=config['Keys']['intelx-key'], ua=__user_agent__)
        capabilities = intelxapi.GET_CAPABILITIES()
        queried_buckets:List[str] = []
        for permitted_bucket in capabilities['buckets']:
            if any(permitted_bucket in bucket for bucket in buckets):
                queried_buckets.append(permitted_bucket)
        results = intelxapi.search(term=query, maxresults=limit, buckets=buckets, timeout=timeout, datefrom=datefrom, dateto=dateto, sort=sort, media=media, terminate=terminate)
        for record in results['records']:
            print(f"Found media type {record['media']} in {record['bucket']}\n\n{record}\n\n########")
        # TODO add handling for discovered data
