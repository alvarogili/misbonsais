# -*- encoding: utf-8 -*-
from principal.models import Bonsai, Labor
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.template import RequestContext
from principal.forms import BonsaiForm, LaborForm, RegistrationForm, sendPassword, UserEditForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from random import choice
import datetime
import string
from django.utils.translation import ugettext

def get_id_usuario(request):
	'''
	returns the user session
	'''
	id_usuario = request.session['member_id']	
	request.session.set_expiry(3600)#30 minutos
	return id_usuario

def get_statistics():
	'''
	Gets the site's statistics
	'''
	statistics = {}
	statistics['usuarios'] = User.objects.count()
	statistics['bonsais'] = Bonsai.objects.count()
	statistics['ultimo_registrado'] = User.objects.order_by('date_joined').reverse()[0]
	# usuarios_online = 0
	# usuarios = User.objects.all()
	# now = datetime.datetime.now()
	# for usuario in usuarios:		
	# 	if usuario.is_authenticated:
	# 		usuarios_online = usuarios_online + 1
	# statistics['usuarios_online'] = usuarios_online
	return statistics


@login_required(login_url='/')
def detalle_bonsai(request, id_bonsai):	
	'''
	muestra un bonsai
	'''
	try:
		id_usuario = get_id_usuario(request)
	except KeyError, e:
		return render_to_response('error.html', {}, 
			context_instance=RequestContext(request))
	
	dato = get_object_or_404(Bonsai, pk = id_bonsai)
	usuario = get_object_or_404(User, pk = id_usuario)
	#verifico que sea el usuario del elemento
	if not usuario.id == id_usuario:
		return HttpResponseRedirect('/usuario/')

	labores = Labor.objects.filter(bonsai = dato).order_by('date').reverse()
	born = dato.birth_date
	now = datetime.date.today()

	born_temp=born.replace(year=now.year)
	if born_temp>now:
		now=now.replace(year=now.year-1)
	age =now.year - born.year

	return render_to_response('bonsai.html', {'bonsai':dato, 'age': age, 'labores':labores, 
		'usuario':usuario, 'statistics':get_statistics()}, context_instance=RequestContext(request))

@login_required(login_url='/')
def nuevo_bonsai(request):
	'''
	agrega un bonsai
	'''
	try:
		id_usuario = get_id_usuario(request)
	except:
		return render_to_response('error.html', {}, 
			context_instance=RequestContext(request))
	usuario = get_object_or_404(User, pk = id_usuario)
	if request.method =='POST':
		formulario = BonsaiForm(request.POST)
		if formulario.is_valid():
			formulario.save()
			return HttpResponseRedirect('/usuario/')
		else:
			print formulario.errors
			return render_to_response('nuevoBonsai.html', {'formulario': formulario, 'error':'True', 
				'usuario':usuario, 'statistics':get_statistics()}, 
			context_instance=RequestContext(request))
	else:
		formulario = BonsaiForm()
		return render_to_response('nuevoBonsai.html', {'formulario': formulario, 'usuario':usuario, 'statistics':get_statistics()}, 
			context_instance=RequestContext(request))

@login_required(login_url='/')
def editar_bonsai(request, id_bonsai):
	'''
	edita un bonsai guardado
	'''
	try:
		id_usuario = get_id_usuario(request)
	except:
		return render_to_response('error.html', {}, 
			context_instance=RequestContext(request))
	dato = get_object_or_404(Bonsai, pk = id_bonsai)	
	usuario = get_object_or_404(User, pk = id_usuario)
	#verifico que sea el usuario del elemento
	if not dato.usuario.id == id_usuario:
		return HttpResponseRedirect('/usuario/')

	if request.method =='POST':
		formulario = BonsaiForm(request.POST, instance=dato)
		if formulario.is_valid():
			formulario.save()
			return detalle_bonsai(request, id_bonsai)
		else:
			return render_to_response('editarBonsai.html', {'formulario': formulario, 
				'error':'True', 'usuario':usuario, 'statistics':get_statistics()}, context_instance=RequestContext(request))
	else:
		formulario = BonsaiForm(instance=dato)
		return render_to_response('editarBonsai.html', {'formulario': formulario, 'usuario':usuario, 'statistics':get_statistics()}, 
			context_instance=RequestContext(request))

@login_required(login_url='/')
def nueva_labor(request, id_bonsai):
	'''
	Agrega una labor a un bonsai especifico
	'''
	try:
		id_usuario = get_id_usuario(request)
	except:
		return render_to_response('error.html', {}, 
			context_instance=RequestContext(request))
	dato = get_object_or_404(Bonsai, pk = id_bonsai)
	usuario = get_object_or_404(User, pk = id_usuario)
	#verifico que sea el usuario del elemento
	if not dato.usuario.id == id_usuario:
		return HttpResponseRedirect('/usuario/')

	labores = Labor.objects.filter(bonsai = dato).order_by('date').reverse()
	if request.method =='POST':
		formulario = LaborForm(request.POST)
		if formulario.is_valid():
			formulario.save()
		else:
			return render_to_response('nuevaLabor.html', {'formulario': formulario, 'bonsai':dato, 
			'labores':labores, 'tasks': Labor.task_type_of_labor, 'error': 'True', 
			'usuario':usuario, 'statistics':get_statistics()}, 
			context_instance=RequestContext(request))	
	formulario = LaborForm()		
	return render_to_response('nuevaLabor.html', {'formulario': formulario, 'bonsai':dato, 
			'labores':labores, 'tasks': Labor.task_type_of_labor, 'usuario':usuario, 'statistics':get_statistics()}, 
			context_instance=RequestContext(request))


@login_required(login_url='/')
def borrar_labor(request, id_labor):
	try:
		id_usuario = get_id_usuario(request)
	except:
		return render_to_response('error.html', {}, 
			context_instance=RequestContext(request))	
	labor = get_object_or_404(Labor, pk = id_labor)
	id_bonsai = labor.bonsai_id
	bonsai = get_object_or_404(Bonsai, pk = id_bonsai)
	#verifico que sea el usuario del elemento
	if bonsai.usuario.id == id_usuario:
		labor.delete()
	return HttpResponseRedirect('/bonsai/nuevaLabor/'+str(id_bonsai))

@login_required(login_url='/')
def borrar_bonsai(request, id_bonsai):
	try:
		id_usuario = get_id_usuario(request)
	except:
		return render_to_response('error.html', {}, 
			context_instance=RequestContext(request))
	bonsai = get_object_or_404(Bonsai, pk = id_bonsai)
	id_usuario_in_bonsai = bonsai.usuario.id
	#verifico que sea el usuario del elemento
	if id_usuario_in_bonsai == id_usuario:
		bonsai.delete()
	return HttpResponseRedirect('/usuario/')

#gestion de usuarios
@login_required(login_url='/')
def main_usuario(request):
	try:
		id_usuario = get_id_usuario(request)
	except:
		return render_to_response('error.html', {}, 
			context_instance=RequestContext(request))
	bonsais = Bonsai.objects.filter(usuario=id_usuario).order_by('common_name')	
	usuario = get_object_or_404(User, pk = id_usuario)
	return render_to_response('bonsais.html', {'datos': bonsais, 'usuario':usuario, 'statistics':get_statistics()}, 
		context_instance=RequestContext(request))	

def nuevo_usuario(request):
	if request.method == 'POST':
		form_reg = RegistrationForm(request.POST)
		if form_reg.is_valid():
			#verificar si no existe el mail
			if not User.objects.filter(email=request.POST['email']):
				new_user = form_reg.save();
				username = request.POST['username']
				new_user = authenticate(username=username, password=request.POST['password1'])
				login(request, new_user)
				usuario = get_object_or_404(User, username = username)
				request.session['member_id'] = usuario.id
				request.session.set_expiry(1800)#30 minutos
				return HttpResponseRedirect('/usuario/')
			else:
				return render_to_response('index.html', {'form_reg':form_reg, 'errorMail':'True'}, 
		 			context_instance=RequestContext(request))				
		else:
			return render_to_response('index.html', {'form_reg':form_reg, 'error':form_reg.errors}, 
		 		context_instance=RequestContext(request))
	else:
		form_reg = RegistrationForm()
		return render_to_response('index.html', {'form_reg':form_reg}, 
		 context_instance=RequestContext(request))

#mostrar guia
def guia(request):
	return render_to_response('guia.html', context_instance=RequestContext(request))

