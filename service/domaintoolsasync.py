import pythonwhois
from pprint import pprint

import time


from decorators import async


@async
def resolveDomainsLong(domains, mongoDomains):
    if len(domains) == 0:
        return

    key = domains.keys()
    d = 0

    while(d < len(key)):
    #while(d < 2):
        dom = domains[ key[d] ]

        time.sleep(1)
        whois = pythonwhois.get_whois(dom['domain'])
        print "Testing: " + key[d] + " / " + str(d)

        if 'contacts' in whois and 'registrant' in whois['contacts'] and not whois['contacts']['registrant'] == None and 'name' in whois['contacts']['registrant']:
            dom['whois'] = { 'name': whois['contacts']['registrant']['name'], 'error': 'false', 'registered': 'true'}
            print "Domain: " + dom['domain'] + "  is registered"

            mongoDomains.save(dom)
            #mongoDomains.update({'_id': dom['_id'], {"$set": dom)

            d += 1
        else:
            if whois['raw'][0].find('You have exceeded this limit') != -1:
                print "Domain: " + dom['domain'] + " .... waiting"
                time.sleep(20)
            else: # "We do not have an entry in our database matching your query." in whois['raw']
                dom['whois'] = { 'name': "", 'error': 'false', 'registered': 'false' }
                d += 1
                print "Domain: " + dom['domain'] + " is NOT registered"
                mongoDomains.save(dom)






#def getWhoisForIp(ip):
#        if ip['idx'] == 0:
#            for ip in domains[dom]['ipaddr']:
#                whois = pythonwhois.get_whois(domains[dom]['domain'])
#                domains[dom]['whois'] = whois.registrant