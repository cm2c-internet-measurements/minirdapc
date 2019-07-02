#!/usr/bin/env python3.7
#----------------------------------------------------------------------------------
# minirdapc
#
# (c) carlos@xt6.us
# 
# Changed: 2019-03-14
#----------------------------------------------------------------------------------

import click
import csv
import ipaddr

from minirdapc import *

if __name__ == "__main__":
    print("Enriching CSV file")

    csvfile = open("input.csv", "r")
    outfile = open("output.csv", "w")

    csvin = csv.DictReader(csvfile, dialect="excel", delimiter="|")

    rdapc = rdap_client("https://rdap.lacnic.net/rdapt2/", \
            w_apikey="1d72e332-ed44-4234-bc45-6bde980d2705-a09732ff-0746-4d95-986a-a5111890c6ba"
            )

    header = next(csvin, None)
    newheader = []
    ouput_array = []
    # csvout.writerow(header)
    for line in csvin:
        # print(line)
        newline = {}
        newheader = []
        # print(line)
        cprefixes = 0
        for key in line:
            k = key # this is needed because the type of line being OrderedDict
            v = line[key]
            # print("\tk={}, v={}".format(k,v))
            try:
                n4 = ipaddr.IPv4Network(v)
                orgid = rdapc.prefixToOrgid(v)
                newline[k] = v
                newheader.append(k)
                # newline.append(orgid)
                newline['orgid'+str(cprefixes)] = orgid
                newheader.append('orgid'+str(cprefixes))
                cprefixes = cprefixes + 1 
            except ipaddr.AddressValueError:
                # raise
                newline[k] = v 
                newheader.append(k)
                next
            except Exception as err:
                print("Unexpected error {0}".format(err))
                print("Current RDAP JSON: {0}".format(rdapc.last_response))
                raise
        ## end for
        # print(newline)
        ouput_array.append(newline)
    ## end for

    ## write output to file
    print("Now writing CSV output to disk. Headers are {}".format(newheader))
    csvout = csv.DictWriter(outfile, dialect='excel', delimiter='|', fieldnames=newheader)
    csvout.writeheader()
    for x in ouput_array:
        try:
            csvout.writerow(x)
        except ValueError:
            print("Wrong fields in row.")
            print("\tLine contains: {}".format(x))
            print("\tField names: {}".format(newheader))
            csvfile.close()
            raise
        except:
            csvfile.close()
            raise
    print("END!")

    csvfile.close()
    outfile.close()

# END SCRIPT ######################################################################