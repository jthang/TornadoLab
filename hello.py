# 4 basic libraries to get this application running
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)
'''
For reading options from the command parse_command_line
Library to specify which port will our application will listen to
'''

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        # Get an argument greeting from the query string
        greeting = self.get_argument('greeting', 'Hello')
        # takes the string as a parameter, write that string into HTTP response
        self.write(greeting + ', cool user!')
'''
Tornado request handler class
When handling a request, Tornado instantiates this class and
calls the method corresponding to the HTTP method of the request
Has a number of useful built-in methods (GET, WRITE, etc)
'''

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
    '''
    handlers parameters most important
    should be a list of tuples (immutable)
    each tuple contacts a regex to match first member and
    RequestHandler class as 2nd member
    '''
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

