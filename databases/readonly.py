import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import pymongo

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/(\w+)', WordHandler)
        ]
        # Instantiate a pymongo connection
        conn = pymongo.Connection("localhost", 27017)
        # Creata a db attribute which refers to example database
        self.db = conn["example"]
        tornado.web.Application.__init__(self, handlers, debug=True)

class WordHandler(tornado.web.RequestHandler):
    def get(self, word):
        # access the DB for the get method
        coll = self.application.db.words
        # find the word in the dictionary
        word_doc = coll.find_one({"word": word})
        # if word found, delete the _id key from dict (so json library can serialize)
        if word_doc:
            del word_doc["_id"]
            # write method will serialize the dictionary as JSON
            self.write(word_doc)
        else:
            self.set_status(404)
            self.write({"error": "word not found"})

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()