from django import forms

from forum.models import Forum

class ForumForm(forms.ModelForm):
	status = forms.CharField(widget=forms.HiddenInput())
	title = forms.CharField(
		widget=forms.TextInput(attrs={'class':'form-control'}),
		max_length=255)
	content = forms.CharField(
		widget=forms.Textarea(attrs={'class':'form-control'}),
		max_length=4000)

	class Meta:
		model = Forum
		fields = ['title','content','status']