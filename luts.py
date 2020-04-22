# pylint: disable=C0103
"""
Common shared text strings and lookup tables.
"""

from datetime import date
import pandas as pd

title = "Alaska Community Daily Precipitation"
url = "http://snap.uaf.edu/tools/demo"
preview = "http://snap.uaf.edu/tools/demo/assets/preview.png"
description = "This app lets you explore historical precipitation for places in Alaska."

communities = pd.read_csv("data/stations.csv")

def get_doy(month, day):
    """ Return DOY from month/day """
    return int(date(date.today().year, month, day).strftime("%j"))


default_date_range = [get_doy(4, 1), get_doy(9, 16)]

default_style = {"color": "rgba(0, 0, 0, 0.25)", "width": 1}

important_years = [2004, 2005, 2009, 2010, 2013, 2015, 2019, 2020]
years_lines_styles = {
    "2004": {"color": "rgba(100, 143, 255, 1)", "width": "2"},
    "2005": {"color": "rgba(120, 94, 240, 1)", "width": "2"},
    "2006": default_style,
    "2007": default_style,
    "2008": default_style,
    "2009": {"color": "rgba(220, 38, 127, 1)", "width": "2"},
    "2010": {"color": "rgba(10, 128, 64, 1)", "width": "2"},
    "2011": default_style,
    "2012": default_style,
    "2013": {"color": "rgba(254, 97, 0, 1)", "width": "2"},
    "2014": default_style,
    "2015": {"color": "rgba(255, 176, 0, 1)", "width": "2"},
    "2016": default_style,
    "2017": default_style,
    "2018": default_style,
    "2019": {"color": "rgba(10, 255, 128, 1)", "width": "2"},
    "2020": {"color": "rgba(10, 25, 0, .85)", "width": "4"},
}

zones = {
    "ALL": "Statewide",
    "MID": "Military Zone",
    "DAS": "Delta Area",
    "FAS": "Fairbanks Area",
    "MSS": "Mat-Su Area",
    "CRS": "Copper River Area",
    "UYD": "Upper Yukon Zone",
    "KKS": "Kenai/Kodiak Area",
    "SWS": "Southwest Area",
    "CGF": "Chugach National Forest",
    "GAD": "Galena Zone",
    "TAS": "Tok Area",
    "HNS": "Haines Area",
    "TAD": "Tanana Zone",
    "TNF": "Tongass National Forest",
}
