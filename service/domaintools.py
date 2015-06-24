import mmap
import socket

from cymruwhois import Client
import pythonwhois
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



#def getWhoisForIp(ip):
#        if ip['idx'] == 0:
#            for ip in domains[dom]['ipaddr']:
#                whois = pythonwhois.get_whois(domains[dom]['domain'])
#                domains[dom]['whois'] = whois.registrant


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
                #domain['ipaddr'][ip]
                #domain['ipaddr'][ip]['ipaddr'] = r.ip
                #domain['ipaddr'][ip]['cc'] = r.cc
                #domain['ipaddr'][ip]['asn'] = r.asn
                #domain['ipaddr'][ip]['asnowner'] = r.owner
                ip['ipaddr'] = r.ip
                ip['cc'] = r.cc
                ip['asn'] = r.asn
                ip['asnowner'] = r.owner


def getBadactorsForDomains(domain):
    f = open('badactors/badactors.txt')
    s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

    for ip in domain['ipaddr']:
        if s.find( ip['ipaddr'] ) != -1:
            #domain['ipaddr'][ip]['badactor'] = 'Yes'
            ip['badactor'] = "Yes"
        else:
            #pprint( domain['ipaddr'][ip] )
            ip['badactor'] = "No"
            #domain['ipaddr'][ip]['badactor'] = 'No'





# not used
def get_whoisJsonWhois(dom):
    ret = "";
    response = unirest.get("https://jsonwhois.com/api/v1/whois",

    headers={
        "Accept": "application/json",
        "Authorization": "Token token=0f543295f4fb14ae05032d54d55beb57"
    },

    params={
        "domain": dom
    })

    #response.body # The parsed response
    print response.body
    #json_obj = json.loads(response.body)

    #print(json_obj['registrant_contacts'])
    return jsonify(response.body);