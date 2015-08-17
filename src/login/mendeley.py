import webapp2
import urllib
import urllib2
import json
import logging

APP_ID=2096
APP_SECRET="d0ehxzEWsqnACUw0"


class MendeleyAuth(webapp2.RequestHandler):
    def get(self):
        pass
        
class MendeleyLogin(webapp2.RequestHandler):
    def get(self):
        sourceUrl = "https://api.mendeley.com/oauth/authorize"
        params = {
            'client_id': APP_ID,
            'redirect_uri': 'http://cite4all.appspot.com/login/mendeley/loginredirect',
            'response_type': 'code',
            'scope': 'all'
        }
        # ADD state? 
        self.redirect(sourceUrl + "?" + urllib.urlencode(params))
    
class MendeleyLoginRedirect(webapp2.RequestHandler):
    def get(self):
        if self.request.get('code'):
            code = self.request.get('code')
            
            # You need the replace to handle encodestring adding a trailing newline 
            # (https://docs.python.org/2/library/base64.html#base64.encodestring)
            url = "https://api.mendeley.com/oauth/token"
            params = {
                'grant_type': "authorization_code",
                'redirect_uri': 'http://cite4all.appspot.com/login/mendeley/loginredirect',
                'code': code,
                'client_id': APP_ID,
                'client_secret': APP_SECRET
            }
            request = urllib2.Request(url, urllib.urlencode(params))
            result = urllib2.urlopen(request)
            tokens = json.loads(result.read())
            logging.info(tokens)
            credentials = {
                "refresh_token": tokens["refresh_token"],
                "token_type": tokens["token_type"]
            }
            
            self.redirect("/login/mendeley/loginsuccess?access_token=%s&token_type=%s" % (tokens["access_token"], tokens["token_type"]))
            return
        self.redirect("/login/mendeley/login")
        
class MendeleyLoginSuccess(webapp2.RequestHandler):
    def get(self):
        pass
        
class MendeleyRenewAuthToken(webapp2.RequestHandler):
    def get(self):
        pass
        
        
app = webapp2.WSGIApplication([
    ('/login/mendeley', MendeleyAuth),
    ('/login/mendeley/login', MendeleyLogin),
    ('/login/mendeley/loginredirect', MendeleyLoginRedirect),
    ('/login/mendeley/loginsuccess', MendeleyLoginSuccess),
    ('/login/mendeley/renewauthtoken', MendeleyRenewAuthToken),
], debug=True)
