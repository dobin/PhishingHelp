from threading import Thread
import json
from functools import wraps
from flask import Flask, jsonify, redirect, request, current_app, abort


# from: http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xi-email-support
def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper



### Helper


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