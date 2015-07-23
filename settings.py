from random import randint


class config():
    CLIENT_ID = '75e82w7gbp82nr'
    CLIENT_SECRET = 'QQhpeWSTUiflDFnY'
    AUTH_URL = "https://www.linkedin.com/uas/oauth2/authorization"
    ACCESS_URL = "https://www.linkedin.com/uas/oauth2/accessToken"
    REDIRECT_URL = "http://localhost:8080/auth/linkedin/callback"
    STATE = str(randint(10000, 99999))
    SCOPE = "r_basicprofile+r_emailaddress"
    HOST = ''
    PORT = 8080
