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
from principal.views import get_id_usuario, get_statistics
#login de usuario
def ingresar(request):
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            user = request.POST['username']
            pas = request.POST['password']
            access = authenticate(username = user, password = pas)
            if access is not None:
                if access.is_active:
                    login(request, access)
                    usuario = get_object_or_404(User, username = user)
                    request.session['member_id'] = usuario.id
                    request.session.set_expiry(1800)#30 minutos
                    return HttpResponseRedirect('/usuario/')
                else:
                    return render_to_response('index.html',{'formulario':formulario, 'errorNoActivo':'True'},
                        context_instance=RequestContext(request))
            else:
                return render_to_response('index.html',{'formulario':formulario, 'errorUsuario':'True'},
                    context_instance=RequestContext(request))
    else:
        allBonsais = Bonsai.objects.filter(imagePath__contains='http').order_by('?')
        rangeVar = 0
        if allBonsais.count() >=30:
            rangeVar = 30
        else:
            rangeVar = allBonsais.count()
        lista = []
        for i in range(rangeVar):        
            bonsai = allBonsais[i]
            usuario = get_object_or_404(User, pk = bonsai.usuario.id)
            lista.append([bonsai, usuario.first_name + ' ' + usuario.last_name])
        formulario = AuthenticationForm()
    return render_to_response('index.html', {'formulario':formulario, 'lista':lista},
        context_instance=RequestContext(request))

#Genera una password aleatoriamente
def gen_passwd(length=8, chars=string.letters + string.digits):
    return ''.join([choice(chars) for i in range(length)])

#Envía el usuario y una nueva clave
def envio_pass(request):
	if request.method == 'POST':
 		form_email = sendPassword(request.POST)
 		if form_email.is_valid():
 			email = request.POST['email']
 			new_pass = gen_passwd()
 			usuario = get_object_or_404(User, email = email)
 			usuario.set_password(new_pass)
 			usuario.save()
 			to = [email]
 			cuerpo_mail = "Estimado/a " + usuario.first_name + ":\n "
 			cuerpo_mail = cuerpo_mail + "Desde el sitio MisBonsais.com.ar se ha solicitado el blanqueo de clave.\n"
 			cuerpo_mail = cuerpo_mail + "Su nueva clave para el ingreso al sitio es la siguiente: \n\n"
 			cuerpo_mail = cuerpo_mail + "Su usuario es: " + usuario.username + "\n"
 			cuerpo_mail = cuerpo_mail + "Y su nueva clave es: " + new_pass + "\n\n\n"
 			# send_mail('www.misbonsais.com.ar: Re-envio de usuario y contrasena',
 			# 	cuerpo_mail, 'no-responder@misbonsais.com.ar', to)
			send_mail('www.misbonsais.com.ar: Blaqueo de clave',
 				cuerpo_mail, 'no-responder@misbonsais.com.ar', to)
			return HttpResponseRedirect('/')
 	else:
 		form_email = sendPassword()
 		return render_to_response('index.html', {'form_email':form_email},
			context_instance=RequestContext(request))

#Cierra sesión
@login_required(login_url='/')
def logout(request):
    try:
        del request.session['member_id']
    except KeyError:
        pass
    return HttpResponseRedirect('/')

#permite editar la info del usuario
@login_required(login_url='/')
def editar_usuario(request):
	try:
		id_usuario = get_id_usuario(request)
	except:
		return render_to_response('error.html', {},
			context_instance=RequestContext(request))
	usuario = get_object_or_404(User, pk = id_usuario)
	cant_bonsais = Bonsai.objects.filter(usuario=id_usuario).count()

	if request.method == 'POST':
		form = UserEditForm(request.POST, instance=usuario)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/usuario/editar/')
		else:
			form = UserEditForm(instance=usuario)
	   		return render_to_response('editarUsuario.html',
	                             {'form':form, 'error_info':'True', 'usuario':usuario, 'statistics':get_statistics(),
	                             'cant_bonsais': cant_bonsais},
	                             context_instance=RequestContext(request))
	else:
	   	form = UserEditForm(instance=usuario)
	   	return render_to_response('editarUsuario.html',
	                             {'form':form, 'usuario':usuario, 'statistics':get_statistics(),
	                             'cant_bonsais': cant_bonsais},
	                             context_instance=RequestContext(request))

#permite cambiar la contraseña
@login_required(login_url='/')
def cambiar_contr(request):
	try:
		id_usuario = get_id_usuario(request)
	except:
		return render_to_response('error.html', {},
			context_instance=RequestContext(request))
	usuario = get_object_or_404(User, pk = id_usuario)
	cant_bonsais = Bonsai.objects.filter(usuario=id_usuario).count()
	if request.method == 'POST':
		form_pass = PasswordChangeForm(request.user, data=request.POST)
		if form_pass.is_valid():
			form_pass.save()
			return HttpResponseRedirect('/usuario/cambiar_contr/')
		else:
			return render_to_response('editarUsuario.html',
	                             {'form_pass':form_pass, 'usuario':usuario, 'statistics':get_statistics(),
	                             'cant_bonsais': cant_bonsais},
	                             context_instance=RequestContext(request))
	else:
	   	form_pass = PasswordChangeForm(request.user)
	   	return render_to_response('editarUsuario.html',
	                             {'form_pass':form_pass, 'usuario':usuario, 'statistics':get_statistics(),
	                             'cant_bonsais': cant_bonsais},
	                             context_instance=RequestContext(request))
