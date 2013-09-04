# Create your views here.
# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.cache import cache as memcache

from datetime import datetime, timedelta

from quemfezcafe.app.models import RegistraCafe

DEBUG = False

# HOrario de verão
#timezone = 2

#Horario Normal
timezone = 3

# Create your views here.
@login_required
def home(request):
	template = 'homepage.html'
	
	user_logado = request.user

	context = memcache.get('context_home')
	if not context:
	    context = {}
	    context['fezcafe'] = RegistraCafe.getJaFez()

	    L = []
	    for item in RegistraCafe.getAll()[:5]:
	        L.append({'username': item.userName,
	                   'dateTimeText': item.dateTimeText})

	    context['dados'] = L
	    context['quantidade'] = RegistraCafe.getQuantidadeCafe()

	    memcache.add('context_home',context, 21600)

	context['user'] = user_logado #.get_current_user()

	#Criação de novo Cafe        
	if request.method == 'POST':
		date = datetime.now() - timedelta(hours=timezone)

		if not RegistraCafe.getJaFez() and\
			(date.hour >= 9 and date.hour < 18) and\
			(date.weekday() != 5 and date.weekday() != 6) or DEBUG == True:

			fez = RegistraCafe(user = user_logado,
							   date_creation = date)
			fez.save()
			memcache.delete('context_home')

		todos_usuarios = RegistraCafe.getQuantidadeCafe()
		for item in todos_usuarios:
			user = item.get('email_user','')
			
			# self.sendMail(user, date, user_logado.email())

		return HttpResponseRedirect('/')

	return render_to_response(template, context,
							  context_instance=RequestContext(request))
