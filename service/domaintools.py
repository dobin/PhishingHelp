import mmap
import socket

from cymruwhois import Client

import whois

from pprint import pprint

# Optimize:
# - mmap
# - dns resolving

def resolveDomain(domain):
    print "ResolveDomains:" + domain['domain']
    getIpForDomains(domain)

    # get badactorflag for each ip
    getBadactorsForDomains(domain)

    ## slow stuff

    # get as for each ip
    # we do all at once for performance reasons
    getAsForDomains(domain)
    #getWhoisForDomains(domains)



def getIpForDomains(domain):
    domain['ipaddr'] = []

    try:
        ips = socket.gethostbyname_ex(domain['domain'])

        for ip in ips[2]:
            domain['ipaddr'].append({'ipaddr': ip})
    except:
        domain['ipaddr'] = []



def getAsForDomains(domain):
    ips = []

    # get all ips
    for ip in domain['ipaddr']:
        theip = ip['ipaddr']
        ips.append(theip)

    # lookup all ips
    c=Client()

    resp = c.lookupmany(ips)

    # find original ip again
    for r in resp:
        for ip in domain['ipaddr']:
            if ip['ipaddr'] == r.ip:
                ip['ipaddr'] = r.ip
                ip['cc'] = r.cc
                ip['asn'] = r.asn
                ip['asnowner'] = r.owner



def getBadactorsForDomains(domain):
    f = open('badactors/badactors.txt')
    s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

    for ip in domain['ipaddr']:
        if s.find( ip['ipaddr'] ) != -1:
            ip['badactor'] = "Yes"
        else:
            ip['badactor'] = "No"



