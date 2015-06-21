#!flask/bin/python
from functools import wraps

from flask import Flask, jsonify, redirect, request, current_app
import dnstwist
import json
import mmap

from cymruwhois import Client
import pythonwhois
import socket


from pprint import pprint

app = Flask(__name__)




# from: https://gist.github.com/farazdagi/1089923
def support_jsonp(f):
    """Wraps JSONified output for JSONP"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('jsonp', False)
        if callback:
            content = str(callback) + '(' + str(f(*args,**kwargs).data) + ')'
            return current_app.response_class(content, mimetype='application/json')
        else:
            return f(*args, **kwargs)
    return decorated_function


@app.route('/myphish/api/v1.0/domain/<dom>', methods=['GET'])
@support_jsonp
def get_domains(dom):
    domains = dnstwist.calcDomains(dom)

    getIpForDomains(domains)
    getAsForDomains(domains)
    getBadactorsForDomains(domains)

    #getWhoisForDomains(domains)

    # convert ips to array
    for dom in domains:
        domains[dom]['ipaddr'] = domains[dom]['ipaddr'].values()

    # convert domains to array and return
    return jsonify({'domains': domains.values()})


def getIpForDomains(domains):
    for dom in domains:
        domains[dom]['ipaddr'] = {}

        try:
            ips = socket.gethostbyname_ex(domains[dom]['domain'])

            for ip in ips[2]:
                domains[dom]['ipaddr'][ip] = {}
        except:
            domains[dom]['ipaddr'] = {}


def getWhoisForDomains(domains):
    for dom in domains:
        for ip in domains[dom]['ipaddr']:
            whois = pythonwhois.get_whois(domains[dom]['domain'])
            domains[dom]['whois'] = whois.registrant


def getAsForDomains(domains):
    ips = []

    # get all ips
    for dom in domains:
        for ip in domains[dom]['ipaddr']:
            theip = ip
            ips.append(theip)

    # lookup all ips
    c=Client()
    resp = c.lookupmany(ips)

    # find original ip again
    for r in resp:
        for d in domains:
            for ip in domains[d]['ipaddr']:
                if ip == r.ip:
                    domains[d]['ipaddr'][ip]

                    domains[d]['ipaddr'][ip]['ipaddr'] = r.ip
                    domains[d]['ipaddr'][ip]['cc'] = r.cc
                    domains[d]['ipaddr'][ip]['asn'] = r.asn
                    domains[d]['ipaddr'][ip]['asnowner'] = r.owner


def getBadactorsForDomains(domains):
    f = open('badactors/badactors.txt')
    s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

    for dom in domains:
        for ip in domains[dom]['ipaddr']:
            print ip

            if s.find( ip ) != -1:
                domains[dom]['ipaddr'][ip]['badactor'] = 'Yes'
            else:
                domains[dom]['ipaddr'][ip]['badactor'] = 'No'


if __name__ == '__main__':
    app.run(debug=True)
