from django.db import models
from django import forms

class User(models.Model):
	'''deatils of the user'''
	uid = models.CharField(max_length=50, unique=True)
	username = models.CharField(max_length=50)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	
	def __unicode__(self):
		return u'%s %s %s %s' % (self.uid, self.username, self.first_name, self.last_name)

class Rack(models.Model):
	'''shows the status of the user as well as any associated ids'''
	status =  models.CharField(max_length=10)
	uid = models.CharField(max_length=50, unique=True)

	def __unicode__(self):
		return u'%s %s %s' % (self.status, self.uid)

class Share(models.Model):
	'''only has entries if there is a shared id'''
	assoc_uid = models.CharField(max_length=100)
	uid = models.CharField(max_length=50)
	time = models.CharField(max_length=50)
	status = models.CharField(max_length=10)

	def __unicode__(self):
		return u'%s %s %s %s' % (self.uid, self.assoc_uid, self.status, self.share)