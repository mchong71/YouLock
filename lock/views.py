from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.template import Context, loader, RequestContext
import json as simplejson
from django.core import serializers

from lock import models as l

from serial import Serial

def index(request):

	if request.session['0'] == 'admin':
		return HttpResponseRedirect('/listen/')
	else:
		users = l.User.objects.raw("select u.id, u.uid, u.first_name, s.status from lock_user u join lock_status s on s.uid = u.uid")

		template = loader.get_template('index.html')
	 
		# Context is a normal Python dictionary whose keys can be accessed in the template index.html
		context = Context({
			'user_status': users
		})
	 
		return HttpResponse(template.render(context))

def share(request):

	if request.method == 'POST':
		print request.POST
		username = str(request.session['0'])
		assocUser = str(request.POST.get('shareID'))
		time = str(request.POST.get('time'))
		print username
		print assocUser
		print time
		share = 'success'
		userDetails = l.User.objects.raw("select * from lock_user where username = '" + username + "'")
		assocDetails = l.User.objects.raw("select * from lock_user where username = '" + assocUser + "'")

		S = l.Share(uid=userDetails[0].uid, assoc_uid=assocDetails[0].uid, time=time)
		S.save()

	template = loader.get_template('index.html')
 
	# Context is a normal Python dictionary whose keys can be accessed in the template index.html
	context = Context({
		'share': share
	})
 
	return HttpResponse(template.render(context))

def listen(request):
	status = ''
	ser = Serial('/dev/tty.usbmodem411', 115200, timeout=1)
	print("connected to: " + ser.portstr)

	while True:
	# Read a line and convert it from b'xxx\r\n' to xxx
		line = ser.readline().decode('utf-8')[:-2]
		if line and line[0:5] != 'DEBUG' and len(line) == 19:
			print(line)
			print (len(line))
			break

	ser.close()
 
	id_status = l.User.objects.raw("select * from lock_user where uid = '" + line + "'")
	valid = '2'
	if len(list(id_status)) > 0:
		'''Is a valid user'''
		rack_status = l.Rack.objects.raw("select * from lock_rack where uid = '" + line+ "'")
		if len(list(rack_status)) == 0:
			'''no one is assigned to this lock'''
			print("assigning user to rack")
			R = l.Rack(status="occupied", uid=line)
			R.save()
			valid = '0'
		else:
			'''someone is assigned to the lock verify based on shared and current id's'''
			rack_status = l.Rack.objects.raw("select id, uid from lock_rack")[0]
			share_status = l.Share.objects.raw("select id, assoc_uid from lock_share where uid = '" + line + "'")
			if rack_status.uid == line or share_status > 0:
				'''correct uid is used to unlock delete any data on rack'''
				print ("deleteing statuses from rack database")
				l.Rack.objects.filter(uid=line).delete()
				valid = '1'

	print valid
	template = loader.get_template('index.html')
 	
	ser = Serial('/dev/tty.usbmodem411', 115200, timeout=1)
	print("connected to: " + ser.portstr)
	ser.write(valid)

	ser.close()

	return HttpResponseRedirect('/listen/')

def login(request):

	template = loader.get_template('login.html')
 
	# Context is a normal Python dictionary whose keys can be accessed in the template index.html
	context = Context({
		'login': login
	})
 
	return HttpResponse(template.render(context))


def authenticate(request):
	
	if request.method == 'POST':
		request.session[0] = request.POST.get('username')
		print request.POST

	if request.POST.get('username') == 'admin':
		return HttpResponseRedirect('/listen/')
	else:
		template = loader.get_template('index.html')
	 
		# Context is a normal Python dictionary whose keys can be accessed in the template index.html
		context = Context({
			'username': request.POST.get('username')
		})
	 
		return HttpResponse(template.render(context))

def logout(request):
	del request.session['0']
	
	template = loader.get_template('login.html')
 
	# Context is a normal Python dictionary whose keys can be accessed in the template index.html
	context = Context({
		'login': 'login'
	})
 
	return HttpResponse(template.render(context))

	
