from django import forms

class ShareForm(forms.Form):
	uid = models.CharField(max_length=50)
	time = models.CharField(max_length=50)
