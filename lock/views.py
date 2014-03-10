from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.template import Context, loader, RequestContext
import json as simplejson
from django.core import serializers

import time
from lock import models as l

from serial import Serial

ser = Serial()
SERVER_STARTED = False

def index(request):

	if request.session['0'] == 'admin':
		context = Context({
				'username': request.session['0'],
			})
		template = loader.get_template('admin.html')
		# print "user"
	 	# print len(givenAccess)
		# Context is a normal Python dictionary whose keys can be accessed in the template index.html
		return HttpResponse(template.render(context))
	else:
		users = l.User.objects.raw("select u.id, u.uid, u.first_name, s.status from lock_user u join lock_status s on s.uid = u.uid")
		count = l.User.objects.raw("select count(id) as count, id from lock_user where uid in (select s.assoc_uid from lock_user u join lock_share s on s.uid = u.uid where u.username = '" + request.session['0'] + "')")
		currUser = l.User.objects.raw("select * from lock_user where username = '" + request.session['0'] + "'")
		
		notifications = l.User.objects.raw("select * from lock_share where assoc_uid = '" + currUser[0].uid + "' and status = 'pending'")
		shareID = l.User.objects.raw("select * from lock_user join lock_share on lock_user.uid = lock_share.uid where lock_share.assoc_uid = '" + currUser[0].uid + "'")
		if len(list(notifications)) > 0:
			hasNotifications = 'enabled'
			shareUser = shareID[0].username
		else:
			hasNotifications = 'disabled'
			shareUser = ''

		if count[0].count > 0:
			print len(list(count))
			access = l.User.objects.raw("select id, first_name, last_name from lock_user where uid in (select s.assoc_uid from lock_user u join lock_share s on s.uid = u.uid where u.username = '" + request.session['0'] + "')")
			givenAccess = l.User.objects.raw("select lock_user.uid, lock_share.status, lock_share.time, lock_user.id from lock_user join lock_share on lock_user.uid = lock_share.assoc_uid where lock_share.assoc_uid = '" + access[0].uid + "'")
			# status = l.User.objects.raw("select * from lock")
			print (givenAccess)
			context = Context({
				'username': request.session['0'],
				'givenAccess': givenAccess,
				'hasNotifications': hasNotifications,
				'shareUser': shareUser
			})
		else:
			context = Context({
				'username': request.session['0'],
				'hasNotifications': hasNotifications,
				'shareUser': shareUser
			})
		template = loader.get_template('index.html')
		# print "user"
	 	# print len(givenAccess)
		# Context is a normal Python dictionary whose keys can be accessed in the template index.html
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

		S = l.Share(uid=userDetails[0].uid, assoc_uid=assocDetails[0].uid, time=time, status='pending')
		S.save()

	return HttpResponseRedirect('/')

def toggle(request):


	context = Context({
				'username': request.session['0'],
			})
	template = loader.get_template('admin.html')
	return HttpResponse(template.render(context))

def delete(request):
	print "deleteing"
	if request.method == 'POST':
		uid = l.User.objects.raw("select id, uid from lock_user where username = '" + request.session['0'] + "'")
		uidToDelete = l.User.objects.raw("select id, uid from lock_user where username = '" + request.POST.get('username') + "'")
		l.Share.objects.filter(assoc_uid=uidToDelete[0].uid, uid=uid[0].uid).delete()

	return HttpResponseRedirect('/')

def listen(request):
	status = ''
	SERVER_STARTED = False
	if request.method == 'POST':
		ser = Serial('/dev/tty.usbmodem411', 115200, timeout=1)
		if request.POST.get('toggle') == 'start':
			print("connected to: " + ser.portstr)
			SERVER_STARTED = True
		else:
			ser.close()
			SERVER_STARTED = False

	while SERVER_STARTED:
		while True:
		# Read a line and convert it from b'xxx\r\n' to xxx
			try:
				inLockingCycle = False
				line = ser.readline().decode('utf-8')[:-2]
				if line and line[0:5] != 'DEBUG' and len(line) == 19:
					print(line)
					break
				elif line[0:10] == "SENSOR_ERR":
					print(line)
					inLockingCycle = True
					break
			except Exception, e:
				print e
			
	 	if not inLockingCycle:
			id_status = l.User.objects.raw("select * from lock_user where uid = '" + line + "'")

			if len(list(id_status)) == 0:
				line = '*'
			valid = '2'
			'''Is a valid user'''
			rack_status = l.Rack.objects.raw("select * from lock_rack")
			if len(list(rack_status)) == 0:
				'''no one is assigned to this lock'''
				print("rack is locked by: " + line)
				R = l.Rack(status="occupied", uid=line)
				R.save()
				valid = '0'
			else:
				'''someone is assigned to the lock verify based on shared and current id's'''
				rack_status = l.Rack.objects.raw("select id, uid from lock_rack")[0]
				share_status = l.Share.objects.raw("select * from lock_share where (assoc_uid = '" + line + "' and uid = '" + rack_status.uid + "') or (assoc_uid = '" + rack_status.uid + "' and uid = '" + line + "') and status = 'shared'")
				if rack_status.uid == line or len(list(share_status)) > 0:
					if len(list(share_status)) > 0:
						print("rack is unlocked by shared ID: " + line)
					else:
						print("rack is unlocked by ID: " + line)
					'''correct uid is used to unlock delete any data on rack'''
					print ("deleteing statuses from rack database")
					l.Rack.objects.all().delete()
					valid = '1'
				else:
					print("invalid id card")

			print valid
			template = loader.get_template('index.html')
		 	
			# ser = Serial('/dev/tty.usbmodem411', 115200, timeout=1)
			# print("connected to: " + ser.portstr)
			ser.write(valid)
		else:
			print ("SENSOR_ERR: deleteing statuses from rack database")
			l.Rack.objects.all().delete()
			template = loader.get_template('index.html')

	if SERVER_STARTED == False:
		context = Context({
				'username': request.session['0'],
			})
		template = loader.get_template('admin.html')

		return HttpResponse(template.render(context))
	else:

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
		template = loader.get_template('admin.html')

		# Context is a normal Python dictionary whose keys can be accessed in the template index.html
		context = Context({
		'username': request.POST.get('username')
		})
 
		return HttpResponse(template.render(context))
	else:
		return HttpResponseRedirect('/')
def logout(request):
	del request.session['0']
	
	template = loader.get_template('login.html')
 
	# Context is a normal Python dictionary whose keys can be accessed in the template index.html
	context = Context({
		'login': 'login'
	})
 
	return HttpResponse(template.render(context))

def shareAccept(request):
	if request.method == 'POST':
		print request.POST
		currUser = l.User.objects.raw("select * from lock_user where username = '" + request.session['0'] + "'")
		l.Share.objects.filter(assoc_uid=currUser[0].uid).update(status=('shared'))
		# query = l.User.objects.raw("update lock_share set status = 'shared' where assoc_uid = '" + currUser[0].uid + "'")


	return HttpResponseRedirect('/')

	
