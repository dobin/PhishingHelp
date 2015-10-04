import sys
import getopt
import json
import pprint

import dnstwist
from domaintools import resolveDomain
from domaintoolsasync import resolveDomainsLongImpl

def main():
    # parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)

    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            print __doc__
            sys.exit(0)

    # process arguments
    for arg in args:
        process(arg) # process() is defined elsewhere


    dom = "dobin.ch"
    print "Domain: " + dom
    domains = dnstwist.calcDomains(dom)

    print json.dumps(domains, indent=4)

    for domain in domains:
        resolveDomain(domains[domain])

    resolveDomainsLongImpl(domains)


if __name__ == "__main__":
    main()