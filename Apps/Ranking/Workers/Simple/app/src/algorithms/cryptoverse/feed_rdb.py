"""
Cryptoverse feed with replies and likes
=======================================

Version: 0.1.0

Example:

`ranking/cryptoverse_feed <https://api.userfeeds.io/ranking/cryptoverse_feed>`_

"""

from algorithms.utils import tokenPattern, assetPattern, addressPattern
from algorithms.cryptoverse import root_rdb
from algorithms.kuba import replies_rdb, reactions_rdb


def run(conn_mgr, input, **params):
    result = root_rdb.run(conn_mgr, input, **params)
    result = replies_rdb.run(conn_mgr, result)
    result = reactions_rdb.run(conn_mgr, result)
    set_types(result["items"])
    return result


def set_types(items):
    for i in items:
        if tokenPattern.match(i["target"]) or addressPattern.match(i["target"]):
            i["type"] = "boost"
        elif i["about"]:
            if tokenPattern.match(i["about"]):
                i["type"] = "post_to"
            elif addressPattern.match(i["about"]):
                i["type"] = "post_to_simple"
            elif assetPattern.match(i["about"]):
                i["type"] = "post_club"
            else:
                i["type"] = "post_about"
        else:
            i["type"] = "regular"