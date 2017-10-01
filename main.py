import tornado.ioloop
import tornado.web
import os
import uuid

from parser import parse

__UPLOADS__ = "uploads/"


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('static/index.html')


class Upload(tornado.web.RequestHandler):

    def post(self):
        fileinfo = self.request.files['filearg'][0]

        ical = parse(fileinfo['body'].decode("utf-8"))
        print(ical)

        self.set_header('Content-type', 'text/calendar')
        self.set_header('Content-Disposition',
                        'attachment; filename="my-bham-timetable.ics"')
        self.write(ical)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/upload", Upload),
        (r"/(.*)",
         tornado.web.StaticFileHandler,
         {"path": r"./static/"})
    ], debug=True)

if __name__ == "__main__":
    app = make_app()
    app.listen(8000, address="0.0.0.0")
    print('App server started.')
    tornado.ioloop.IOLoop.current().start()
