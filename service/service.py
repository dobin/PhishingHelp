#!flask/bin/python
from flask import Flask, jsonify, redirect, request, current_app, abort
from functools import wraps
from pprint import pprint
import unirest
import json

from pymongo import MongoClient

import dnstwist
from domaintools import resolveDomain


mongoClient = MongoClient('localhost')
mongoDB = mongoClient.phishing_help

app = Flask(__name__)

# from: http://stackoverflow.com/questions/16586180/typeerror-objectid-is-not-json-serializable
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


# from: https://gist.github.com/farazdagi/1089923
# used to annonate another function to return JSONP
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
    # get all mutations of initial domain
    # id 0 is original
    domains = dnstwist.calcDomains(dom)

    mongoDomains = mongoDB.domains

    # check if already exists in db
    for domain in domains:
        mongoDomain = mongoDomains.find_one({"domain": domain})

        if not mongoDomain is None:
            domains[domain] = mongoDomain
            domains[domain]['_id'] = str(domains[domain]['_id'])
        else:
            # resolve by our self
            resolveDomain(domains[domain])
            mongoDomains.insert(domains[domain])
            domains[domain]['_id'] = str(domains[domain]['_id'])

    # convert ips to array
    #for dom in domains:
    #    domains[dom]['ipaddr'] = domains[dom]['ipaddr'].values()

    # convert domains to array and return
    return jsonify({'domains': domains.values()})


@app.route('/myphish/api/v1.0/whois/<dom>', methods=['GET'])
def get_whois(dom):
    ret = "";

    whois = pythonwhois.get_whois(dom)

    if 'contacts' in whois and 'registrant' in whois['contacts'] and not whois['contacts']['registrant'] == None and 'name' in whois['contacts']['registrant']:
        ret = { 'name': whois['contacts']['registrant']['name'], 'error': 'false'}
        return jsonify(ret)
    else:
        #ret = { 'error': 'true' }
       abort(404);


if __name__ == '__main__':
    app.run(debug=True)


