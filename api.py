#!/usr/bin/python
#
# DON'T FORGET TO SET THE API KEY/SECRET.
import six
import base64
import json
import sys
from encodings.utf_8 import encode
from six.moves.urllib.parse import urlencode 
from six.moves.http_client import HTTPSConnection
from six.moves.urllib.parse import urlparse as parse


def apihit(host,conntype,authtoken,queryurl,reqbody,prox):
    retdata = ''
    if (prox['host'] != '') and (prox['port'] != ''):
        useproxy = True
    else:
        useproxy = False

    if useproxy == True:
        connection = HTTPSConnection(prox['host'], prox['port'])
        connection.set_tunnel(host, 443)
    else:
        connection = HTTPSConnection(host)
    tokenheader = {"Authorization": 'Bearer ' + authtoken, "Content-type": "application/json", "Accept": "text/plain"}
    if conntype == "GET":
        connection.request(conntype, queryurl, '', tokenheader)
    else:
        connection.request(conntype, queryurl, json.dumps(reqbody), tokenheader)
    response = connection.getresponse()
    respbody = response.read().decode('ascii', 'ignore')
    try:
        jsondata = respbody.decode()
        retdata = json.loads(jsondata)
    except AttributeError:
        retdata = json.loads(respbody)
    except:
        raise
    connection.close()
    return retdata

def get_auth_token(host,clientid,clientsecret,prox):
    queryurl = '/oauth/access_token'
    if (prox['host'] != '') and (prox['port'] != ''):
        useproxy = True
    else:
        useproxy = False
    if useproxy == True:
        connection = HTTPSConnection(prox['host'], prox['port'])
        connection.set_tunnel(host, 443)
    else:
        connection = HTTPSConnection(host)
    authtoken = base64.b64encode(six.b('{0}:{1}'.format(clientid, clientsecret)))
    authstring = b"Basic %s" % (authtoken,)

    header = {"Authorization": authstring}
    params = urlencode({'grant_type': 'client_credentials'})
    connection.request("POST", queryurl, params, header)
    response = connection.getresponse()
    jsondata = bytes(response.read()).decode('utf-8')
    data = json.loads(str(jsondata))
    try:
        if  data['access_token']:
            pass
    except:
        print("We're having trouble getting a session token.  Please check your API key.")
        print("Error output: ")
        print(data)
        sys.exit()
    key = data['access_token']
    connection.close()
    return key
