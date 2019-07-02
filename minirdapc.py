#!/usr/bin/env python3.7
#----------------------------------------------------------------------------------
# minirdapc
#
# (c) carlos@xt6.us
# 
# Changed: 2019-03-14
#----------------------------------------------------------------------------------

import click
import requests
import shelve
import datetime
import time
import pyjq
import json
import logging

from rdap_client import rdap_client

logging.basicConfig(level=logging.DEBUG)

def print_banner(short=False):
    print("")
    print("MINI RDAP CLIENT: (c) Carlos Martinez, carlos@xt6.us")
    if not short:
        print(" Version 0.2 2019-05-26")
        print("")
        print(" Use --help for usage information.")
        print("")
    else:
        print(" ")
## END print_banner

# cli #######################################################################################
@click.command()
@click.option("--query", help="String to query RDAP for.")
@click.option("--type", default=None, help="RDAP query type, one of autnum, ip or entity")
@click.option("--host", default="https://rdap.lacnic.net/rdap", help="RDAP server to query. Optional, defaults to LACNIC")
@click.option("--advquery", default=None, help="Get ORGID of given prefix.")
@click.option("--apikey", default=None, help="Optional: API Key for LACNIC, used to bypass rate limits.")
def cli(query, type, host, advquery, apikey):
        rdapc = rdap_client(host, apikey)
        if type in ['ip', 'autnum', 'entity']:
            print_banner(True)
            res = rdapc.rdap_query(type, query)
            print( json.dumps(res, indent=3, sort_keys=True) )
        elif advquery in ['prefixToOrgid'] :
            print_banner(True)
            res = rdapc.prefixToOrgid(query)
            out = "{prefix},{orgid}".format(prefix=query, orgid=res)
            print(out)
        else:
            print_banner()
            print("Wrong combination of query and advquery. Plase use: ")
            print("\ttype = ip | autnum | entity")
            print(" OR ")
            print("\tadvquery = prefixToOrgid")

        # print (str(res))
## end cli ##################################################################################

if __name__ == "__main__":
    cli()

#--END-----------------------------------------------------------------------------