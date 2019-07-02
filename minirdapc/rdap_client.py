#######################################################################################################
# RDAP CLIENT MODULE
#
# (c) Carlos Martinez, carlos@xt6.us
# 2019-05-26
#######################################################################################################

import requests
import shelve
import datetime
import time
import pyjq
import json
import logging

class rdap_client:

    # Default constructor
    def __init__(self, w_base_url, w_apikey=None ,w_cache_file='var/rdap_cache.db'):
        """Class constructor.

        This is the default class constructor. Expected parameters are:

        
         
        """
        self.base_url = w_base_url
        self.apikey = w_apikey
        self.rdap_cache = shelve.open(w_cache_file)
        self.max_cache_time = 60*3600 # cache validity in seconds
        self.last_response = None
    # end default constructor

    # destructor
    def __del__(self):
        self.rdap_cache.close()
    # end

    # http_get
    def rdap_http_get(self, w_uri):
        """
        Simple HTTP get to be used as part of the RDAP client. It expects the return of the GET method
        to be valid JSON.
        """
        try:
            rdap_url = self.base_url + w_uri
            print(rdap_url)
            r = requests.get(rdap_url)
            if r.status_code == 200:
                return r.json()
            else:
                return "{'status code': '%s', 'response': %s}" % (str(r.status_code), repr(r) )
        except:
            raise
    # end http_get

    # pyjq interface
    def _pyjq(self, w_query, w_json = None):
        """
        Runs a jq query against a json structure
        """

        if w_json == None:
            q_json = self.last_response
        else:
            q_json = w_json

        try:
            r = pyjq.first(w_query, q_json)
        except:
            raise
        #
        return r
    # end pyjq

    # get_poc ##############################################################################################
    def get_poc(self, w_role, w_depth=0, w_json = None):
        """
        get_poc() retrieves the handles for different roles (abuse, technical, registrant). Can be used
        in 'simple' or 'deep' mode. In simple mode only the handle is returned, in deep mode an additional
        RDAP query is made and detailed contact information is returned.
        """
        if w_json == None:
            q_json = self.last_response
        else:
            q_json = w_json
        #
        if w_role not in ['abuse', 'technical', 'registrant']:
            raise ValueError("Unknown POC role")
        #
        # jq = '.entities[] | select (.roles[0] == "{}") | .handle + " , " + .roles[0]'.format(w_role)
        jq = '.entities[] | select (.roles[0] == "{}") | .handle'.format(w_role)
        # print("jq string={}".format(jq))
        r = self._pyjq(jq)
        #
        if w_depth == 0:
            return r
        elif w_depth == 1:
            # further query rdap to get email addresses
            r2 = self.rdap_query("entity", r)
            email = self._pyjq('.vcardArray[1] | .[]  | select ( .[0] == "email") | .[3]', r2)
            jr = {'handle': r, 'email': email}
            return jr
    # end get_poc ##########################################################################################

    # bgn prefixToOrgid ####################################################################################
    def prefixToOrgid(self, w_prefix):
        # jq query: .entities[0].handle
        self.res = self.rdap_query("ip", w_prefix)
        jq = ".entities[0].handle"
        try:
            res = self._pyjq(jq, self.last_response)
        except pyjq._pyjq.ScriptRuntimeError:
            res = "ORGID-NOTFOUND"
            logging.debug("ORGID for prefix {} not found, current JSON is {}" \
                .format(w_prefix, self.last_response))
        except:
            raise
        return res
    # end prefixToOrgid ####################################################################################

    # rdap query ###########################################################################################
    def rdap_query(self, w_type, w_query):

        if w_type not in ['ip', 'autnum', 'entity']:
            raise ValueError("Wrong query type")

        try:
            if self.apikey:
                # rdap_uri = "/"+w_type+"/"+w_query+"?apikey="+self.apikey
                rdap_uri = "/{type}/{query}?apikey={apikey}" \
                    .format(type=w_type, query=w_query, apikey=self.apikey)
            else:
                rdap_uri = "/"+w_type+"/"+w_query
            logging.debug("rdap_uri={}".format(rdap_uri))
            # first check if answer is available in local cache and fresh enough
            cached_r = self.rdap_cache.get(rdap_uri, { 'json': None, 'timestamp': 0, 'hits': 0})
            if cached_r['json'] == None or (cached_r['timestamp'] - time.time()) > self.max_cache_time:
                # if not, do an http query
                r = self.rdap_http_get(rdap_uri)
                # TODO: No guardar en el cache cosas que no sirven!!
                # store result in cache
                cached_r = { 'json': r, 'timestamp': int(time.time()), 'hits': 0}
                self.rdap_cache[rdap_uri] = cached_r
            else: 
                # return the result available in cache
                r = cached_r['json']
                pass
        except:
            r = False
            raise
        self.last_response = r
        return r
    # end rdap query #######################################################################################

# end class rdap_client

if __name__ == "__main__":
    print("Not to be run directly!")

# END MODULE