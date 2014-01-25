from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.template import Context, loader, RequestContext

from lock import models as l

from serial import Serial

def index(request):

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
		share = 'success'

	template = loader.get_template('index.html')
 
	# Context is a normal Python dictionary whose keys can be accessed in the template index.html
	context = Context({
		'share': share
	})
 
	return HttpResponse(template.render(context))
		# form = ShareForm(request.POST)
		# if form.is_valid():
		# 	userId = form.cleaned_data['assocID']
		# 	print "testing"
		# 	return HttpResponseRedirect('index.html')
		# else:
		# 	form = ShareForm()

		# return render(request, 'index.html', {'form': form})

def listen(request):
	status = ''
	ser = Serial('/dev/tty.usbmodem411', 115200, timeout=1)
	print("connected to: " + ser.portstr)

	while True:
	# Read a line and convert it from b'xxx\r\n' to xxx
		line = ser.readline().decode('utf-8')[:-2]
		if line:
			print(line)
			break
 
	ser.close()

	user_status = l.User.objects.raw("select * from lock_user where uid = '" + line + "'")

	if len(list(user_status)) > 0:
		check_status = l.Status.objects.raw("select status from lock_status where uid = '" + line + "'")
		if check_status[0] == 'unoccupied': #lock is opened and we can assign a lock signal to it 
			#write to serial that we can assign an id
			status = 'assigned ID'
			l.Status.objects.raw("update lock_status set status = 'occupied'")
		elif check_status[0] == 'occupied':
			#write to serial that we can open lock
			status = 'opened lock'
			l.Status.objects.raw("update lock_status set status = 'unoccupied'")

	template = loader.get_template('index.html')
 
	# Context is a normal Python dictionary whose keys can be accessed in the template index.html
	context = Context({
		'status': share
	})
 
	return HttpResponse(template.render(context))
