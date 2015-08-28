#!flask/bin/python
from flask import Flask, jsonify, redirect, request, current_app, abort
from pprint import pprint
import unirest
import json
from decorators import support_jsonp, JSONEncoder

from bson.json_util import dumps
from bson import Binary, Code

from datetime import datetime
from bson import ObjectId
import simplejson
from flask import Response
from datetime import datetime

from pymongo import MongoClient

import dnstwist
from domaintools import resolveDomain
from domaintoolsasync import resolveDomainsLong


mongoClient = MongoClient('localhost')
mongoDB = mongoClient.phishing_help

app = Flask(__name__)

class MongoDocumentEncoder(simplejson.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        elif isinstance(o, ObjectId):
            return str(o)
        return simplejson.JSONEncoder(self, o)


def mongodoc_jsonify(*args, **kwargs):
    return Response(simplejson.dumps(dict(*args, **kwargs), cls=MongoDocumentEncoder), mimetype='application/json')

@app.route('/myphish/api/v1.0/domainInfo/<dom>', methods=['GET'])
@support_jsonp
def get_domain(dom):
    mongoDomains = mongoDB.domains

    domain = mongoDomains.find_one({ 'domain': dom });
    return mongodoc_jsonify(domain)


@app.route('/myphish/api/v1.0/domain/<dom>', methods=['GET'])
@support_jsonp
def get_domains(dom):
    print "Start"
    ui = 0

    # get all mutations of initial domain
    # id 0 is original
    domains = dnstwist.calcDomains(dom)

    mongoDomains = mongoDB.domains
    unresolvedDomains = {}

    # check if already exists in db
    for domain in domains:
        mongoDomain = mongoDomains.find_one({"domain": domain})

        if not mongoDomain is None:
            # get from db
            domains[domain] = mongoDomain
        else:
            # resolve by our self and insert into db
            domains[domain]['resolveDate'] = datetime.now()
            resolveDomain(domains[domain])
            domains[domain]['isFullyResolved'] = False;
            mongoDomains.insert(domains[domain])

            # mark for further processing
            unresolvedDomains[domain] = domains[domain]


    # start long lived resolver
    resolveDomainsLong(unresolvedDomains, mongoDomains)

    # convert domains to array and return to client
    return mongodoc_jsonify({'domains': domains.values()})
    #return JSONEncoder().encode({'domains': domains.values()})
    #return dumps({'domains': domains.values()})


if __name__ == '__main__':
    app.run(debug=True)


