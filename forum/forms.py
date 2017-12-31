from django import forms

from forum.models import Article,ArticleComment

class ArticleForm(forms.ModelForm):
	# status = forms.CharField(widget=forms.HiddenInput())
	title = forms.CharField(
		widget=forms.TextInput(attrs={'class':'form-control'}),
		max_length=255)
	content = forms.CharField(
		widget=forms.Textarea(attrs={'class':'form-control'}),
		max_length=4000)

	class Meta:
		model = Article
		fields = ['title','content']


class CommentForm(forms.ModelForm):
	comment = forms.CharField(
		widget = forms.Textarea(attrs={'class':'form-control'}),
		max_length=500)
	class Meta:
		model = ArticleComment
		fields = ['comment']