import pythonwhois
from pprint import pprint
from ipwhois.ipwhois import IPDefinedError
from ipwhois import IPWhois

import time
import json
import urllib2
import hmac
import hashlib
import urllib

from decorators import async

def screenshotlayer(access_key, secret_keyword, url, args):
    # encode URL
    query = urllib.urlencode(dict(url=url, **args))

    # generate md5 secret key
    secret_key = hashlib.md5('{}{}'.format(url, secret_keyword)).hexdigest()

    return "https://api.screenshotlayer.com/api/capture?access_key=%s&secret_key=%s&%s" % (access_key, secret_key, query)


def getScreenshot(urltoget):
    print "Trying to get: " + urltoget
    # set optional parameters (leave blank if unused)
    params = {
        'fullpage': '',
        'width': '',
        'viewport': '',
        'format': '',
        'css_url': '',
        'delay': '',
        'ttl': '',
        'force': '',
        'placeholder': '',
        'user_agent': '',
        'accept_lang': '',
        'export': ''
    };

    # set your access key, secret keyword and target URL
    access_key = "176d57aca77221ccd48c92e6328f1539"
    secret_keyword = "shitfuckbooze"
    #url = "http://www.cnn.com"

    url = screenshotlayer (access_key, secret_keyword, urltoget, params)

    response = urllib2.urlopen(url)

    body = response.read()
    return body



def resolveDomainGeo(dom):
    print "... geoinfo"

    i = 0
    while(i < len(dom['ipaddr'])):
        ip = dom['ipaddr'][i]['ipaddr']
        print "... geoinfo: " + ip
        geoinfo = {}
        try:
            response = urllib2.urlopen('http://ip-api.com/json/' + ip)
            json_response = response.read()
            decoded_json = json.loads(json_response)

            # Check for failed response (such as a reserved range)
            if decoded_json['status'].encode('utf-8') == "fail":
                print "geo fail"
            else:
                # Load info into IP object
                if decoded_json['as'].encode('utf-8') is not '':
                    geoinfo['ip_as_number'] = decoded_json['as'].encode('utf-8')
                if decoded_json['country'].encode('utf-8') is not '':
                    geoinfo['ip_country'] = decoded_json['country'].encode('utf-8')
                if decoded_json['countryCode'].encode('utf-8') is not '':
                    geoinfo['ip_country_code'] = decoded_json['countryCode'].encode('utf-8')
                if decoded_json['city'].encode('utf-8') is not '':
                    geoinfo['ip_city'] = decoded_json['city'].encode('utf-8')
                if decoded_json['zip'].encode('utf-8') is not '':
                    geoinfo['ip_zipcode'] = decoded_json['zip'].encode('utf-8')
                if decoded_json['isp'].encode('utf-8') is not '':
                    geoinfo['ip_isp'] = decoded_json['isp'].encode('utf-8')
                if decoded_json['lat'] is not '':
                    geoinfo['ip_latitude'] = str(decoded_json['lat'])
                if decoded_json['lon'] is not '':
                    geoinfo['ip_longitude'] = str(decoded_json['lon'])
                if decoded_json['region'].encode('utf-8') is not '':
                    geoinfo['ip_region_code'] = decoded_json['region'].encode('utf-8')
                if decoded_json['regionName'].encode('utf-8') is not '':
                    geoinfo['ip_region_name'] = decoded_json['regionName'].encode('utf-8')
                if decoded_json['timezone'].encode('utf-8') is not '':
                    geoinfo['ip_timezone'] = decoded_json['timezone'].encode('utf-8')
                if decoded_json['org'].encode('utf-8') is not '':
                    geoinfo['ip_organization'] = decoded_json['org'].encode('utf-8')

                print "  area: " + geoinfo['ip_region_name'] + " / " + geoinfo['ip_country']

            # Sleep is here to make sure we don't go over API limits
            time.sleep(.5)
        except urllib2.URLError:
            print "Error"

        dom['ipaddr'][i]['geoinfo'] = geoinfo

        i+=1


def resolveDomainIpwhois(dom):
    print "... ipwhois"

    i = 0
    while(i < len(dom['ipaddr'])):
        time.sleep(1)

        ip_whois = IPWhois( dom['ipaddr'][i]['ipaddr'] )
        dom['ipaddr'][i]['whois'] = ip_whois.lookup()
        pprint(dom['ipaddr'][i]['whois'])
        i += 1


def resolveDomainDomainwhois(dom):
    time.sleep(1)
    print "... domainwhois"
    whois = pythonwhois.get_whois(dom['domain'])

    if 'contacts' in whois and 'registrant' in whois['contacts'] and not whois['contacts']['registrant'] == None and 'name' in whois['contacts']['registrant']:
        dom['whois'] = { 'name': whois['contacts']['registrant']['name'], 'error': 'false', 'registered': 'true'}
        print "Domain: " + dom['domain'] + "  is registered"
        dom['isFullyResolved'] = True;
        ##mongoDomains.save(dom)
        #mongoDomains.update({'_id': dom['_id'], {"$set": dom)
    else:
        if whois['raw'][0].find('You have exceeded this limit') != -1:
            print "Domain: " + dom['domain'] + " .... waiting"
            time.sleep(20)
        else: # "We do not have an entry in our database matching your query." in whois['raw']
            dom['whois'] = { 'name': "", 'error': 'false', 'registered': 'false' }
            print "Domain: " + dom['domain'] + " is NOT registered"
            dom['isFullyResolved'] = True;
            ##mongoDomains.save(dom)


def getDomainScreenshot(dom):
    if dom['whois']['registered'] == 'true':
        # screenshot
        screenshot = getScreenshot( "http://www." + dom['domain'] )

        # we are - hopefully - in ./service
        f = open('../screenshots/' + str(dom[ '_id' ]), 'w')
        f.write(screenshot)
        f.close()


def resolveDomainsLongImpl(domains):
    if len(domains) == 0:
        return

    key = domains.keys()
    d = 0

    while(d < len(key)):
        dom = domains[ key[d] ]
        print "Testing: " + dom['domain']

        resolveDomainGeo(dom)
        resolveDomainIpwhois(dom)
        resolveDomainDomainwhois(dom)

        # print json.dumps(dom, indent=4)

        d+=1


@async
def resolveDomainsLong(domains, mongoDomains):
    if len(domains) == 0:
        return

    key = domains.keys()
    d = 0

    while(d < len(key)):
        dom = domains[ key[d] ]
        print "Testing: " + dom['domain']

        resolveDomainGeo(dom)
        resolveDomainIpwhois(dom)
        resolveDomainDomainwhois(dom)

        mongoDomains.save(dom)

        if dom['whois']['registered'] == 'true':
            getDomainScreenshot(dom)

        d+=1


#    d = 0
#    while(d < len(key)):
#        dom = domains[ key[d] ]
#        mongoDomains.save(dom)
