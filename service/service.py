#!flask/bin/python
from functools import wraps

from flask import Flask, jsonify, redirect, request, current_app
import dnstwist
import json
import mmap
from cymruwhois import Client

from pprint import pprint

app = Flask(__name__)

c=Client()


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
    getAsForDomains(domains)
    getBadactorsForDomains(domains)
    return jsonify({'domains': domains})


def getAsForDomains(domains):
    ips = []

    # get all ips
    for dom in domains:
        if 'ipaddr' in domains[dom] and domains[dom]['ipaddr'] != None:
            theip = domains[dom]['ipaddr']
            ips.append(theip)

    # lookup all ips
    resp = c.lookupmany(ips)

    # omfg is this ugly
    for r in resp:
        for d in domains:
            if domains[d]['ipaddr'] == r.ip:
                domains[d]['cc'] = r.cc
                domains[d]['asn'] = r.asn
                domains[d]['asnowner'] = r.owner


def getBadactorsForDomains(domains):
    f = open('badactors/badactors.txt')
    s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

    for dom in domains:
        if 'ipaddr' in domains[dom] and domains[dom]['ipaddr'] != None:
            if s.find( domains[dom]['ipaddr'] ) != -1:
                domains[dom]['badactor'] = 'badactor'


if __name__ == '__main__':
    app.run(debug=True)
