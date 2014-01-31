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
		count = l.User.objects.raw("select count(id) as count, id from lock_user where uid in (select s.assoc_uid from lock_user u join lock_share s on s.uid = u.uid where u.username = '" + request.session['0'] + "')")
		if count[0].count > 0:
			print len(list(count))
			access = l.User.objects.raw("select id, first_name, last_name from lock_user where uid in (select s.assoc_uid from lock_user u join lock_share s on s.uid = u.uid where u.username = '" + request.session['0'] + "')")
			givenAccess = l.User.objects.raw("select * from lock_user where uid = '" + access[0].uid + "'")
			print (givenAccess)
			context = Context({
				'username': request.session['0'],
				'givenAccess': givenAccess
			})
		else:
			context = Context({
				'username': request.session['0'],
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

		S = l.Share(uid=userDetails[0].uid, assoc_uid=assocDetails[0].uid, time=time)
		S.save()

	return HttpResponseRedirect('/')

def delete(request):
	print "deleteing"
	if request.method == 'POST':
		uid = l.User.objects.raw("select id, uid from lock_user where username = '" + request.session['0'] + "'")
		uidToDelete = l.User.objects.raw("select id, uid from lock_user where username = '" + request.POST.get('username') + "'")
		l.Share.objects.filter(assoc_uid=uidToDelete[0].uid, uid=uid[0].uid).delete()

	return HttpResponseRedirect('/')

def listen(request):
	status = ''
	ser = Serial('/dev/tty.usbmodem411', 115200, timeout=1)
	print("connected to: " + ser.portstr)

	while True:
	# Read a line and convert it from b'xxx\r\n' to xxx
		try:
			line = ser.readline().decode('utf-8')[:-2]
			if line and line[0:5] != 'DEBUG' and len(line) == 19:
				print(line)
				print (len(line))
				break
		except Exception, e:
			print e
		

	ser.close()
 
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
		share_status = l.Share.objects.raw("select * from lock_share where assoc_uid = '" + line + "' and uid = '" + rack_status.uid + "'")
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
		return HttpResponseRedirect('/')
def logout(request):
	del request.session['0']
	
	template = loader.get_template('login.html')
 
	# Context is a normal Python dictionary whose keys can be accessed in the template index.html
	context = Context({
		'login': 'login'
	})
 
	return HttpResponse(template.render(context))

	
