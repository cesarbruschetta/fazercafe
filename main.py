# coding: utf-8
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
import webapp2
from models import RegistraCafe
from google.appengine.ext.webapp import template

from google.appengine.api import users
from datetime import datetime, timedelta

from google.appengine.api import mail

import os

# HOrario de verão
#timezone = 2

#Horario Normal
timezone = 3


def doRender(handler, tname='index.html', values={}):
    temp = os.path.join(os.path.dirname(__file__),'templates/' + tname)
    if not os.path.isfile(temp):
        return False

    # Make a copy of the dictionary and add the path
    newval = dict(values)
    newval['path'] = handler.request.path

    outstr = template.render(temp, newval)
    handler.response.out.write(outstr)
    return True

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('Hello world!')
        
class Logout(webapp2.RequestHandler):
    def get(self):
        self.redirect(users.create_logout_url('/'))        

class HomePageHandler(webapp2.RequestHandler):
    def get(self):
        context = {}
        context['user'] = users.get_current_user()
        context['fezcafe'] = RegistraCafe.getJaFez()
        context['dados'] = RegistraCafe.getAll().fetch(5)
        context['quantidade'] = RegistraCafe.getQuantidadeCafe()
        
        doRender(self,'homepage.pt',context)
        
    def post(self):
        user_logado = users.get_current_user()
        date = datetime.now() - timedelta(hours=timezone)
        
        if not RegistraCafe.getJaFez() and\
			  (date.hour >= 9 and date.hour < 18) and\
              (date.weekday() != 5 and date.weekday() != 6):
            fez = RegistraCafe(user = user_logado,
                               date_creation = date)
            fez.save()
        
            todos_usuarios = RegistraCafe.getQuantidadeCafe()
            for item in todos_usuarios:
                user = item.get('user','')
                self.sendMail(user.email(), date, user_logado.email())
            
        self.redirect('/')
        
    def sendMail(self,send_to,date,user):
        msg = """   O Usuario %s Fez o cafe as %s .

              """ %(user,date.strftime('%d/%m/%Y %H:%M'))
        
        
        message = mail.EmailMessage()
        message.sender = 'cesaraugusto@liberiun.com'
        message.to = send_to
        message.subject = '** AVISO - QUEM FEZ CAFE **'
        message.body = msg.decode( 'utf-8', 'ignore')
        message.send()        
        
        

L = [('/', HomePageHandler),
     ('/hello', MainHandler),
     ('/logout', Logout),
     ]

DEBUG = False
app = webapp2.WSGIApplication(L,debug=DEBUG)
