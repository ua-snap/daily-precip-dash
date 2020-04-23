"""
Responsible for fetching, preprocessing
and caching community data.
"""
# pylint: disable=C0103, E0401

import urllib.parse
import os
import datetime
import logging
import pandas as pd
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

DASH_LOG_LEVEL = os.getenv("DASH_LOG_LEVEL", default="info")
logging.basicConfig(level=getattr(logging, DASH_LOG_LEVEL.upper(), logging.INFO))

API_URL = os.getenv("ACIS_API_URL", default="http://data.rcc-acis.org/StnData?")
logging.info("Using ACIS API url %s", API_URL)

# Set up cache.
CACHE_EXPIRE = int(os.getenv("DASH_CACHE_EXPIRE", default="43200"))
logging.info("Cache expire set to %s seconds", CACHE_EXPIRE)
cache_opts = {"cache.type": "memory"}

cache = CacheManager(**parse_cache_config_options(cache_opts))
data_cache = cache.get_cache("api_data", type="memory", expire=CACHE_EXPIRE)


def fetch_api_data(community):
    """
    Reads data from ACIS API for selected community.
    """
    logging.info("Sending upstream data API request")
    query = urllib.parse.urlencode(
        {
            "sid": community,
            "sdate": "1950-01-01",
            "edate": datetime.date.today().strftime("%Y-%m-%d"),
            "elems": "4,10",  # precip & snow!
            "output": "csv",
        }
    )
    query = API_URL + query
    logging.debug("API query string: %s", query)
    std = pd.read_csv(
        query, names=["date", "pcpt", "snow"], parse_dates=True, skiprows=1
    )

    # Drop missing, switch trace to 0, and assign column types
    std = std.loc[std["pcpt"] != "M"]  # drop missing
    std = std.loc[std["snow"] != "M"]  # drop missing
    std = std.replace("T", 0)  # make T (Trace) = 0
    std["pcpt"] = std["pcpt"].astype("float")
    std["snow"] = std["snow"].astype("float")

    # Remove 0's.
    std = std.loc[(std["pcpt"] > 0) | (std["snow"] > 0)]

    std["date"] = pd.to_datetime(std["date"])
    std["doy"] = std["date"].apply(lambda d: d.strftime("%j")).astype("int")
    std["year"] = std["date"].apply(lambda d: d.strftime("%Y")).astype("int")
    std["total"] = std["pcpt"] + std["snow"]
    return std


def fetch_data(community):
    """
    Fetches preprocessed data from cache,
    or triggers an API request + preprocessing.
    """

    # Wrapper to call lambda (fetch_api_data) with argument
    # within scope here.
    def call_api():
        return fetch_api_data(community)

    return data_cache.get(key=community, createfunc=call_api)
