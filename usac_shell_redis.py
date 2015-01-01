from libusac3.util import RIDER_TRANSFORMS, CLUB_TEAM_TRANSFORMS

from attrdict import AttrDict
from redis import Redis
import argparse

parser = argparse.ArgumentParser(description='Open the USAC database Redis ORM in a Python shell')
parser.add_argument('--host', type=str, help='hostname to connect to', default="localhost")
parser.add_argument('--port', type=int, help='port on host to connect to', default=6379)
args = parser.parse_args()

rds = Redis(host=args.host, port=args.port)


def get_club(cid):
    rdata = rds.hgetall("club:%d" % int(cid))
    if not rdata:
        return None
    ad = AttrDict()
    for key, func in CLUB_TEAM_TRANSFORMS:
        if key is None:
            continue
        bkey = key.encode('utf-8')
        ad[key] = func(rdata[bkey].decode())
    return ad


def get_team(tid):
    rdata = rds.hgetall("team:%d" % int(tid))
    if not rdata:
        return None
    ad = AttrDict()
    for key, func in CLUB_TEAM_TRANSFORMS:
        if key is None:
            continue
        bkey = key.encode('utf-8')
        ad[key] = func(rdata[bkey].decode())
    ad["club"] = get_club(ad["club_id"])
    return ad


def get_rider(lic):
    rdata = rds.hgetall("rider:%d" % int(lic))
    if not rdata:
        return None
    ad = AttrDict()
    for key, func in RIDER_TRANSFORMS:
        if key is None:
            continue
        bkey = key.encode('utf-8')
        ad[key] = func(rdata[bkey].decode())
        if "club_id" in key and ad[key] is not None:
            ad[key[:-3]] = get_club(ad[key])
        if "team_id" in key and ad[key] is not None:
            ad[key[:-3]] = get_team(ad[key])
    return ad


import bpython
bpython.embed(locals_=locals())