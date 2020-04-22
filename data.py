# import urllib.parse
import pandas as pd
import datetime

def fetch_data(community):
    """
    Reads data from ACIS API for selected community.
    """

    # Placeholder for early dev/explore work.
    # This code works for fetching from the API.
    # TODO we must cache the results for a community here,
    # so that we're at least not hitting the API up twice
    # for every page load / location change.
    # https://beaker.readthedocs.io/en/latest/index.html or similar.

    # query = urllib.parse.urlencode(
    #     {"sid": "26451", "sdate": "1950-01-01", "edate": "2020-04-20", "elems": "4,10", "output": "csv"}
    # )
    # api_url = "http://data.rcc-acis.org/StnData?"
    # std = pd.read_csv(api_url + query, names=["date", "pcpt", "snow"], parse_dates=True, skiprows=1)
    # std = std.loc[std.pcpt != "M"]  # drop missing
    # std = std.loc[std.snow != "M"]  # drop missing
    # std = std.replace("T", 0)  # make T (Trace) = 0
    # std.to_csv("data/anchorage.csv")

    std = pd.read_csv("data/anchorage.csv")
    std = std.loc[std.pcpt > 0]
    std["date"] = pd.to_datetime(std["date"])
    std["doy"] = std["date"].apply(lambda d: d.strftime("%j")).astype("int")
    std["year"] = std["date"].apply(lambda d: d.strftime("%Y")).astype("int")
    std["total"] = std["pcpt"] + std["snow"]
    return std
