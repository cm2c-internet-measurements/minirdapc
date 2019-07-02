#!/usr/bin/env python3.7
#-----------------------------------------------------------------------------
#
# 2019-03-17
#-----------------------------------------------------------------------------

import unittest
from unittest.mock import patch, Mock
import json

class TestRdapC(unittest.TestCase):

    def setUp(self):
        try:
            from minirdapc.rdap_client import rdap_client
            self.rdapc = rdap_client("https://rdap.lacnic.net/rdap")
            self.r = True
        except:
            self.r = False
            raise
    # end setup

    # 
    def tearDown(self):
        # self.rdapc.rdap_cache.close()
        pass
    # end tearDown

    def test_start(self):
        self.assertTrue(self.r)
    # end test

    def test_http_get(self):
        res = self.rdapc.rdap_http_get("/ip/200.7.84.1")
        self.assertTrue(res['rdapConformance'][0] == 'rdap_level_0')
    # end test

    #
    def test_rdap_query_ip_single(self):
        res = self.rdapc.rdap_query("ip", "200.7.84.1")
        self.assertTrue(res['rdapConformance'][0] == 'rdap_level_0')
        self.assertTrue(res['objectClassName'] == 'ip network')
    # end

    #
    def test_rdap_query_ip_network(self):
        res = self.rdapc.rdap_query("ip", "200.7.84.0/24")
        self.assertTrue(res['rdapConformance'][0] == 'rdap_level_0')
        self.assertTrue(res['objectClassName'] == 'ip network')
    # end

    #
    def test_rdap_query_autnum(self):
        res = self.rdapc.rdap_query("autnum", "28001")
        self.assertTrue(res['rdapConformance'][0] == 'rdap_level_0')
        self.assertTrue(res['objectClassName'] == 'autnum')
    # end

    #
    def test_rdap_query_entity(self):
        res = self.rdapc.rdap_query("entity", "UY-LACN-LACNIC")
        self.assertTrue(res['rdapConformance'][0] == 'rdap_level_0')
        self.assertTrue(res['objectClassName'] == 'entity')
    # end

    #
    def test_pyjq_query_response(self):
        res = self.rdapc.rdap_query("ip", "200.7.84.0/24")
        object_class_name = self.rdapc._pyjq('.objectClassName', res)
        self.assertTrue(object_class_name == 'ip network')
    # end

    #
    def test_pyjq_query_response_implicit_json(self):
        res = self.rdapc.rdap_query("ip", "200.7.84.0/24")
        object_class_name = self.rdapc._pyjq('.objectClassName')
        self.assertTrue(object_class_name == 'ip network')
    # end

    #
    def test_get_poc_simple(self):
        res = self.rdapc.rdap_query("ip", "200.7.84.0/24")
        poc = self.rdapc.get_poc('abuse', 0)
        self.assertTrue(poc == "ABL2", msg = "poc: {}".format(poc) )
        poc = self.rdapc.get_poc('technical', 0)
        self.assertTrue(poc == "AIL", msg = "poc: {}".format(poc) )
    # end

    #
    def test_get_poc_deep(self):
        res = self.rdapc.rdap_query("ip", "200.7.84.0/24")
        poc = self.rdapc.get_poc('technical', 1)
        self.assertTrue(poc['handle'] == "AIL", msg = "poc: {}".format(poc) )
        self.assertTrue(poc['email'] == "ipadmin@lacnic.net", msg = "poc: {}".format(poc) )
    # end

    def test_get_poc_deep2(self):
        res = self.rdapc.rdap_query("ip", "200.7.84.0/24")
        poc = self.rdapc.get_poc('abuse', 1)
        self.assertTrue(poc['handle'] == "ABL2", msg = "poc: {}".format(poc) )
        self.assertTrue(poc['email'] == "ipabuse@lacnic.net", msg = "poc: {}".format(poc) )
    # end

# end class TestRdapC

if __name__ == '__main__':
    print("TESTING minirdapc - (c) carlos@xt6.us, March 2019\n")
    unittest.main()

#-----------------------------------------------------------------------------