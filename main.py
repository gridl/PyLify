#! /usr/bin/python
from requests import post
from linkedin import linkedin
from settings import config
from sys import exit
import os
import json
import pickle
import argparse
import webbrowser
import BaseHTTPServer

resp = False
at = ''     # auth token
st = ''     # state
http = {}


def auth_token():
    """
        Fetch Authentication token
    """
    auth_url = config.AUTH_URL + "?response_type=code&client_id=" + \
        config.CLIENT_ID + "&redirect_uri=" + config.REDIRECT_URL + \
        "&state=" + config.STATE + "&scope=" + config.SCOPE
    webbrowser.open(auth_url)
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((config.HOST, config.PORT), authTokenHandler)
    http[1] = httpd
    try:
        httpd.serve_forever()
    except:
        pass
    if not resp:
        httpd.server_close()
    return


class authTokenHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def __init__(self):
        pass

    def do_GET(s):
        global at, st
        url = s.requestline
        if 'code' in url:                           # parse the code params
            code = url.split('=')[1].split('&')[0]
            state = url.split('=')[2].split()
            resp = True
            if http[1]:
                http[1].server_close()
            at, st = code, state[0]
        else:
            print url.error, url.error_description
        print "Fetching access token...Go ahead and close the browser tab!"

    def do_POST(s):
        pass


class OAuth(object):
    def __init__(self):
        try:
            f = open('token', 'r')
        except IOError:
            f = open('token', 'wb')
            pickle.dump([], f)
            f.close()
            f = open('token', 'r')
        tk = pickle.load(f)
        f.close()
        if not tk:
            auth_token()            # fetch authorization token
            if st != config.STATE:
                print "CSRF Attack! Aborting.."
                exit(1)
            data = {
                    'grant_type': 'authorization_code',
                    'code': at,
                    'redirect_uri': config.REDIRECT_URL,
                    'client_id': config.CLIENT_ID,
                    'client_secret': config.CLIENT_SECRET
                    }
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            r = post(config.ACCESS_URL, data=data,
                     headers=headers).text  # fetch access token
            r = json.loads(r)
            token = r['access_token']
            tk = list(token)
            f = open('token', 'wb')
            pickle.dump(tk, f)
            f.close()
        else:
            token = ''.join(tk)
        self.app = linkedin.LinkedInApplication(token=token)


def main():
    user = OAuth()
    user = user.app
    print user.get_profile(selectors=['id', 'first-name', 'last-name',
                                      'location', 'distance',
                                      'num-connections',
                                      'skills', 'educations'
                                      ])


if __name__ == "__main__":
    main()
