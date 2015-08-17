import webapp2

class LoginPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World 2')

app = webapp2.WSGIApplication([
    ('/login/', LoginPage),
], debug=True)
