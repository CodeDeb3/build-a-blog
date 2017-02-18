#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import webapp2
import jinja2

from google.appengine.ext import db

# set up jinja
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

allowed_routes = [
    "/blog",
    "/newpost",
    "/"
]

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self,template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Blog(db.Model):
    title = db.StringProperty(required = True)
    blog = db.TextProperty(required = True) # > 500 chars
    created = db.DateTimeProperty(auto_now_add = True)

# class User(db.Model):

class MainPage(Handler):

    def render_front(self, title="", blog="", error=""):
        blogz = db.GqlQuery("SELECT * from Blog ORDER BY created DESC LIMIT 5")

        self.render("blogs.html", title=title, blog=blog, error=error, blogz=blogz)
    # #def render_front(self,title="", blog="", error="")



    def get(self):
        # t=jinja_env.get_template("blogs.html")
        # content = t.render(blog= blog)
        # self.response.write(content)

        self.render_front()


    def post(self):
        title = self.request.get("title")
        blog = self.request.get("blog")

        if title and blog:
            b = Blog(title=title, blog=blog)
            b.put()
            self.redirect("/newpost")
        else:
            error= "we need a title and a blog"
            self.render_front(title, blog, error)

class ViewPostHandler(Handler):
    def get(self,id):
        self.response.write()


class BlogList(Handler):

# def render_front(self, title="", blog="", error=""):
#     blogz = db.GqlQuery("SELECT * from Blog ORDER BY created DESC LIMIT 5")
#     self.render("base.html", title=title, blog=blog, error=error, blogz=blogz)

    def get(self):

        blogz = db.GqlQuery("SELECT * from Blog ORDER BY created DESC")

        t=jinja_env.get_template("showblogs.html")
        content = t.render(blogz= blogz)
        self.response.write(content)

# def post(self):
#     title = self.request.get("title")
#     blog = self.request.get("blog")
#
#     if title and blog:
#         b = Blog(title=title, blog=blog)
#         b.put()
#         self.redirect("/blog")
#     else:
#         error= "we need a title and a blog"
#         self.render_front(title, blog, error)

app = webapp2.WSGIApplication([
    ('/',MainPage),
    ('/newpost', MainPage),
    ('/blog', BlogList),
    # ('/newpost', NewPostHandler),

    webapp2.Route('/blog/<id:\d+>',ViewPostHandler),
], debug=True)
