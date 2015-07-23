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

RESP = False
AT = ''     # auth token
ST = ''     # state
HTTP = {}


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
    HTTP[1] = httpd
    try:
        httpd.serve_forever()
    except:
        pass
    if not RESP:
        httpd.server_close()
    return


class authTokenHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def __init__(self):
        pass

    def do_GET(s):
        global AT, ST
        url = s.requestline
        if 'code' in url:                           # parse the code params
            code = url.split('=')[1].split('&')[0]
            state = url.split('=')[2].split()
            RESP = True
            if HTTP[1]:
                HTTP[1].server_close()
            AT, ST = code, state[0]
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
            if ST != config.STATE:
                print "CSRF Attack! Aborting.."
                exit(1)
            data = {
                    'grant_type': 'authorization_code',
                    'code': AT,
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
    parser = argparse.ArgumentParser(description=" \
             Run LinkedIn operations from your Terminal. --help to know more")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-m", "--me", help="Know about yourself",
                       action="store_true")
    group.add_argument("-j", "--job", help="Job description", type=str)
    group.add_argument("-C", "--company", help="Company description", type=str)
    group.add_argument("-p", "--people",
                       help="Name of the user to search", type=str)
    group.add_argument("-c", "--connection", help="Name of the user whose \
        connections are to be known", action="store_true")
    group.add_argument("-s", "--share", help="Share stuffs", type=str)
    group.add_argument("-i", "--invite", help="Send invitations", type=str)
    group.add_argument("-g", "--group", help="Group posts", type=str)
    group.add_argument("-b", "--bookmarks", help="Fetch your job bookmarks",
                       type=str)
    args = parser.parse_args()  # parse the arguments
    user = OAuth()
    user = user.app
    if args.me:
        print user.get_profile(selectors=['id', 'first-name', 'last-name',
                                          'location', 'distance',
                                          'num-connections',
                                          'skills', 'educations'
                                          ])
    elif args.job:
        pass
    elif args.company:
        pass
    elif args.people:
        pass
    elif args.connection:
        pass
    elif args.share:
        pass
    elif args.invite:
        pass
    elif args.group:
        pass
    elif args.bookmarks:
        pass


if __name__ == "__main__":
    main()
