#!flask/bin/python
from flask import Flask, jsonify, redirect, request, current_app, abort
from pprint import pprint
import unirest
import json
from decorators import support_jsonp, JSONEncoder

from bson.json_util import dumps
from bson import Binary, Code

from datetime import datetime

from pymongo import MongoClient

import dnstwist
from domaintools import resolveDomain
from domaintoolsasync import resolveDomainsLong


mongoClient = MongoClient('localhost')
mongoDB = mongoClient.phishing_help

app = Flask(__name__)


@app.route('/myphish/api/v1.0/domain/<dom>', methods=['GET'])
@support_jsonp
def get_domains(dom):
    # get all mutations of initial domain
    # id 0 is original
    domains = dnstwist.calcDomains(dom)

    mongoDomains = mongoDB.domains
    unresolvedDomains = []

    # check if already exists in db
    for domain in domains:
        mongoDomain = mongoDomains.find_one({"domain": domain})

        if not mongoDomain is None:
            # get from db
            domains[domain] = mongoDomain
            domains[domain]['_id'] = str(domains[domain]['_id'])
        else:
            # resolve by our self and insert into db
            domains[domain]['resolveDate'] = datetime.now()
            resolveDomain(domains[domain])
            mongoDomains.insert(domains[domain])

            # mark for further processing
            unresolvedDomains.append(domains[domain])


    # start long lived resolver
    resolveDomainsLong(domains, mongoDomains)


    # convert id so jsonify works
    for domain in domains:
        domains[domain]['_id'] = str(domains[domain]['_id'])

    # convert domains to array and return to client
    return jsonify({'domains': domains.values()})
    #return JSONEncoder().encode({'domains': domains.values()})
    #return dumps({'domains': domains.values()})



if __name__ == '__main__':
    app.run(debug=True)


