import sys
import getopt
import json
import pprint

import dnstwist
from domaintools import resolveDomain
from domaintoolsasync import resolveDomainsLongImpl

def printHelp():
    print "--help this"
    print "--domain/-d  <domain>"

def main():
    # parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:h", ["help", "domain"])
    except getopt.error, msg:
        printHelp()
        sys.exit(0)

    if len(sys.argv) == 1:
        printHelp()
        sys.exit(0)

    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            printHelp()
            sys.exit(0)
        if o in ("-d", "--domain"):
            dom = a

    print "Domain: " + dom

    domains = dnstwist.calcDomains(dom)

    print json.dumps(domains, indent=4)

    for domain in domains:
        resolveDomain(domains[domain])

    resolveDomainsLongImpl(domains)


if __name__ == "__main__":
    main()